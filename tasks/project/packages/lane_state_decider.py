from .adjacent_lanes import AdjacentLane

def isEmptyLaneNorth(frame, detected_objects) -> bool:
    for detected_object in detected_objects:
        bbox, score, cls_id = detected_object
        xmin, ymin, xmax, ymax = bbox
        xmid = (xmax + xmin)/2

        if cls_id == 1 and xmid < 320:
            return False
        
    return True
    
def isEmptyLaneEast(frame, detected_objects) -> bool:
    for detected_object in detected_objects:
        bbox, score, cls_id = detected_object
        xmin, ymin, xmax, ymax = bbox
        xmid = (xmax + xmin)/2

        if cls_id == 1 and xmid >= 320:
            return False
        
    return True

def areEmptyLanesUntil(outgoing_lane: AdjacentLane, frame, detected_objects) -> bool:
    if detected_objects is None:
        return False
    
    if outgoing_lane == AdjacentLane.east:
        return True
    
    elif outgoing_lane == AdjacentLane.north:
        return isEmptyLaneEast(frame, detected_objects)
    
    elif outgoing_lane == AdjacentLane.west:
        return isEmptyLaneEast(frame, detected_objects) and isEmptyLaneNorth(frame, detected_objects)
    
    else:
        raise ValueError("Invalid outgoing lane for areEmptyLanesUntil")