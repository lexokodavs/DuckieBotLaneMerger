from adjacent_lanes import AdjacentLane
from ObjectDetector import ObjectDetector
import cv2

def decide_outgoing_lane(frame, object_detector) -> AdjacentLane:
    detected_objects = object_detector.detect(frame)
    duck_counter = 0

    if detected_objects is None:
        return AdjacentLane.east

    for detected_object in detected_objects:
        bbox, score, cls_id = detected_object

        if cls_id == 0:
            duck_counter += 1

    if duck_counter == 0:
        return AdjacentLane.west
    
    elif duck_counter == 1:
        xmin, ymin, xmax, ymax = bbox

        if xmax < 240:
            return AdjacentLane.north
        else:
            return AdjacentLane.east
    
    else:
        raise ValueError("Too many ducks")