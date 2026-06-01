import logging
import sys
import os
import argparse

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')
sys.path.insert(0, project_root)

from flask import Flask, Response, render_template_string
import cv2
import numpy as np

from duckiebot.camera_driver import CameraDriver
from launcher.ports import find_available_port
from servers.common import make_frame_generator, shutdown_cleanup

logger = logging.getLogger(__name__)
app = Flask(__name__)

camera = None

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Duckiebot Camera</title>
    <style>
        body { margin: 0; background: #111; display: flex; justify-content: center; align-items: center; height: 100vh; }
        img  { max-width: 100%; max-height: 100vh; }
    </style>
</head>
<body>
    <img src="/video" />
</body>
</html>"""


def _visualize(frame):
    if frame is None:
        blank = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(blank, "Waiting for camera...", (160, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (80, 80, 80), 2)
        return blank

    # Red channel (BGR format)
    red = frame[:, :, 2]
    green = frame[:, :, 1]
    blue = frame[:, :, 0]

    # Threshold: 150 <= R <= 255
    mask = ((red >= 150) & (red <= 255) & (green <= 110) & (blue <= 110)).astype(np.uint8) * 255

    # --- Noise removal ---
    kernel = np.ones((3, 3), np.uint8)

    # Remove small noise
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Fill small holes (optional but usually helpful)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Convert to 3-channel black/white image
    output = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    return output


generate_frames = make_frame_generator(lambda: camera, _visualize, quality=70, rgb=False)


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
    global camera

    ap = argparse.ArgumentParser(description="Camera-only Real Hardware Server")
    ap.add_argument("--port", type=int, default=5000)
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format='%(levelname)s %(message)s',
        stream=sys.stdout,
    )

    logger.info("[1/1] Initializing camera driver...")
    camera = CameraDriver()
    camera.start()
    logger.info("  Camera: initialized!")

    web_port = find_available_port(args.port)
    if web_port != args.port:
        logger.info(f"  Port {args.port} busy, using {web_port}")

    print(f"Web Interface: http://<bot-ip>:{web_port}")
    print("Press Ctrl+C to stop")

    try:
        app.run(host='0.0.0.0', port=web_port, debug=False, threaded=True)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        shutdown_cleanup(None, camera, None)


if __name__ == "__main__":
    sys.exit(main())