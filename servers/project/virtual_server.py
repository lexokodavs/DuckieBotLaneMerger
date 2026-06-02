import sys
import os
import threading
import time
import queue
import socket

script_dir   = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')
sys.path.insert(0, project_root)

import cv2
from flask import Flask, Response, render_template_string, jsonify, request
import numpy as np

from servers.templates.project import get_template as PROJECT_TEMPLATE
from tasks.project.packages import agent as project_agent

from duckiebot.camera_driver.godot_camera_driver import GodotCameraDriver, GodotCameraConfig
from duckiebot.wheel_driver.godot_wheels_driver import GodotWheelsDriver
from duckiebot.wheel_driver.wheels_driver_abs import WheelPWMConfiguration
from launcher.ports import find_available_port
from servers.common import make_frame_generator, shutdown_cleanup, suppress_http_logs


app = Flask(__name__)
camera = None
wheels = None
running = False
stop_event = threading.Event()

# Simple config for color thresholds (BGR) used by count_lanes
_config_lock = threading.Lock()
_lower_bgr = [0, 0, 200]
_upper_bgr = [80, 80, 255]
_last_lane_count = 0


def visualize(frame_rgb):
    global _last_lane_count
    # Prefer frame produced by the project agent if available.
    agent_frame = None
    try:
        agent_frame = None
        #agent_frame = project_agent.get_last_frame() CHANGE
    except Exception:
        agent_frame = None

    use_frame = agent_frame if agent_frame is not None else frame_rgb

    if use_frame is None:
        blank = (255 * np.ones((480, 640, 3), dtype='uint8'))
        cv2.putText(blank, 'Waiting for camera/agent...', (100, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (80, 80, 80), 2)
        return blank

    # frame from Godot/agent is RGB — convert to BGR for OpenCV overlays
    bgr = cv2.cvtColor(use_frame, cv2.COLOR_RGB2BGR)

    with _config_lock:
        lower = list(_lower_bgr)
        upper = list(_upper_bgr)

    try:
        lanes = 0
    except Exception:
        lanes = 0

    _last_lane_count = int(lanes)

    # Overlay text
    text = f'Lanes: {lanes}'
    cv2.putText(bgr, text, (12, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # draw small boxes showing thresholds (top-left) — colors shown as BGR
    cv2.rectangle(bgr, (8, 40), (48, 80), tuple(int(x) for x in lower), -1)
    cv2.rectangle(bgr, (56, 40), (96, 80), tuple(int(x) for x in upper), -1)

    return bgr


generate_frames = make_frame_generator(lambda: camera, visualize, quality=60)


@app.route('/')
def index():
    html = PROJECT_TEMPLATE(title='Project', subtitle='Virtual Duckiebot')
    return render_template_string(html)


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/status')
def status():
    with _config_lock:
        lb = list(_lower_bgr)
        ub = list(_upper_bgr)
    agent_status = {}
    try:
        agent_status = {} #agent_status = project_agent.get_status() CHANGE
    except Exception:
        agent_status = {}

    return jsonify({
        'running': running,
        'lane_count': _last_lane_count,
        'lower_bgr': lb,
        'upper_bgr': ub,
        'agent': agent_status,
    })


@app.route('/command', methods=['POST'])
def command():
    data = request.json or {}
    key = data.get('key')
    value = data.get('value')
    if not key:
        return jsonify({'status': 'error', 'message': 'missing key'}), 400

    with _config_lock:
        if key in ('lower', 'lower_bgr', 'lower_b'):
            try:
                parts = [int(x.strip()) for x in value.split(',')]
                if len(parts) == 3:
                    _lower_bgr[0], _lower_bgr[1], _lower_bgr[2] = parts
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)}), 400
        elif key in ('upper', 'upper_bgr', 'upper_b'):
            try:
                parts = [int(x.strip()) for x in value.split(',')]
                if len(parts) == 3:
                    _upper_bgr[0], _upper_bgr[1], _upper_bgr[2] = parts
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)}), 400
        else:
            # store arbitrary config keys if needed in the future
            pass

    return jsonify({'status': 'ok'})


def main():
    global camera, wheels, running

    import argparse
    ap = argparse.ArgumentParser(description='Project Server — Virtual')
    ap.add_argument('--port', type=int, default=5000)
    ap.add_argument('--frame-port', type=int, default=5001)
    ap.add_argument('--wheel-port', type=int, default=5002)
    ap.add_argument('--godot-host', type=str, default='localhost')
    args = ap.parse_args()

    suppress_http_logs()
    print('=' * 60)
    print('PROJECT SERVER — VIRTUAL')
    print('=' * 60)

    # Initialize wheels (simulation)
    wheels = GodotWheelsDriver(
        WheelPWMConfiguration(),
        WheelPWMConfiguration(),
        godot_host=args.godot_host, godot_port=args.wheel_port,
    )

    # Initialize camera
    camera = GodotCameraDriver(godot_config=GodotCameraConfig(host='0.0.0.0', port=args.frame_port))
    camera.start()

    # Start the project agent in background so it can expose processed frames
    stop_event.clear()
    try:
        threading.Thread(target=project_agent.main, args=(camera, wheels, None, stop_event), daemon=True, name='ProjectAgent').start()
        print('  project.agent.main() running')
    except Exception as e:
        print(f'  Could not start project agent: {e}')

    running = True

    web_port = find_available_port(args.port)
    print(f'\nWeb Interface: http://localhost:{web_port}')
    print('=' * 60 + '\n')

    try:
        app.run(host='127.0.0.1', port=web_port, debug=False, threaded=True)
    except KeyboardInterrupt:
        print('\nShutting down...')
    finally:
        shutdown_cleanup(wheels, camera, stop_event)


if __name__ == '__main__':
    sys.exit(main())
