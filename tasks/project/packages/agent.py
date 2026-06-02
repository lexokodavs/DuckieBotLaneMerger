import time
from bot_state import BotState
from adjacent_lanes import AdjacentLane
from lane_state_decider import areEmptyLanesUntil
from outgoing_lane_decider import decide_outgoing_lane
from is_in_front_decider import is_in_front
from convoy import convoy
from ObjectDetector import ObjectDetector

from _aux import set_all_leds


def main(camera, wheels, leds, stop_event):
    print('[ProjectAgent] started main loop')

    bot_state = BotState.convoying
    set_all_leds(leds, 1, 0, 0)
    outgoing_lane = None
    object_detector = ObjectDetector(config_path="config/object_detection_config.yaml", model_path="tasks/object_detection/models/best.onnx")


    while not stop_event.is_set():
        ok, frame = camera.read()
        if not ok:
            time.sleep(0.05)
            continue

        print(f"Current bot state: {bot_state}")

        if bot_state == BotState.convoying:
            if is_in_front(frame):
                print("Bot is in front of the lane, now waiting")
                bot_state = BotState.waiting
                outgoing_lane = decide_outgoing_lane(frame, object_detector)
                set_all_leds(leds, 0, 1, 0)
            else:
                convoy(frame, wheels, leds)

        elif bot_state == BotState.waiting:
            detected_objects = object_detector.detect(frame)
            can_go = areEmptyLanesUntil(outgoing_lane, frame, detected_objects)

            if can_go:
                print("Right lanes are clear, starting to turn")
                bot_state = BotState.turning
                set_all_leds(leds, 0, 0, 1)

        elif bot_state == BotState.turning:
            pass # TODO

        elif bot_state == BotState.finishing:
            pass # TODO

        else:
            raise ValueError(f"Invalid bot state: {bot_state}")

        time.sleep(0.01)