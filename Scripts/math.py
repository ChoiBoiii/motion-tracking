
## Returns the distance between two 3D points
def get_dist_3D(p1: tuple[float, float, float], p2: tuple[float, float, float]) -> float:
    return (((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2) + ((p1[2] - p2[2]) ** 2)) ** 0.5
