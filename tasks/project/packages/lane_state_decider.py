from adjacent_lanes import AdjacentLane

def isEmptyLaneNorth(frame) -> bool:
    raise NotImplementedError("isEmptyLaneNorth is not implemented yet")

def isEmptyLaneEast(frame) -> bool:
    raise NotImplementedError("isEmptyLaneEast is not implemented yet")

def areEmptyLanesUntil(outgoing_lane: AdjacentLane, frame) -> bool:
    if outgoing_lane == AdjacentLane.east:
        return True
    
    elif outgoing_lane == AdjacentLane.north:
        return isEmptyLaneEast(frame)
    
    elif outgoing_lane == AdjacentLane.west:
        return isEmptyLaneEast(frame) and isEmptyLaneNorth(frame)
    
    else:
        raise ValueError("Invalid outgoing lane for areEmptyLanesUntil")