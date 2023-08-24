from Scripts.hands import HandMesh

def pinching_index(handMesh: HandMesh) -> bool:
    ## Click
    # minX = min(x for x, _, _ in rightHand.palm)
    # minY = min(y for _, y, _ in rightHand.palm)
    # minZ = max(z for _, _, z in rightHand.palm)
    # maxX = max(x for x, _, _ in rightHand.palm)
    # maxY = max(y for _, y, _ in rightHand.palm)
    # maxZ = max(z for _, _, z in rightHand.palm)
    # diffX = maxX - minX
    # diffY = maxY - minY
    # diffZ = maxZ - minZ
    x1, y1, z1 = handMesh.index[2]
    x2, y2, z2 = handMesh.thumb[2]
    # dx, dy, dz = (x1 - x2) / diffX, (y1 - y2) * diffY, (z1 - z2) * diffZ
    dx, dy, dz = (x1 - x2), (y1 - y2), (z1 - z2)
    dist = (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5
    
    ##
    return dist < 0.04

def pinching_middle():
    pass

def pinching_ring():
    pass

def pinching_pinky():
    pass