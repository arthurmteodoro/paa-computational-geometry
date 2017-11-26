from Problems.ClassicalProblems import distance_between_two_points
from Representations.Point import Point
from Utils.Utils import cmp_to_key
import math


class Points:
    def __init__(self):
        self.minDistance = math.inf
        self.point_1 = None
        self.point_2 = None

    def change(self, p1, p2):
        if distance_between_two_points(p1, p2) < self.minDistance:
            self.point_1 = p1
            self.point_2 = p2
            self.minDistance = distance_between_two_points(p1, p2)


def compare_x(p1: Point, p2: Point):
    return p1.get_x() - p2.get_x()


def compare_y(p1: Point, p2: Point):
    return p1.get_y() - p2.get_y()


def brute_force(p: list, n: int, points: Points):
    min_value = math.inf

    for i in range(n):
        for j in range(i+1, n):
            if distance_between_two_points(p[i], p[j]) < min_value:
                min_value = distance_between_two_points(p[i], p[j])
                points.change(p[i], p[j])

    return min_value


def strip_closest(strip: list, size: int, d: float, points: Points):
    min_value = d

    strip.sort(key=cmp_to_key(compare_y))

    for i in range(size):
        j = i+1
        while j < size and (strip[j].get_y() - strip[i].get_y()) < min_value:
            if distance_between_two_points(strip[i], strip[j]):
                min_value = distance_between_two_points(strip[i], strip[j])
                points.change(strip[i], strip[j])

    return min_value


def closest_util(p: list, n: int, points: Points):
    if n <= 3:
        return brute_force(p, n, points)

    mid = int(n/2)
    mid_point = p[mid]

    dl = closest_util(p, mid, points)
    dr = closest_util(p[mid:], n-mid, points)

    d = min(dl, dr)

    strip = []
    for i in range(n):
        if math.fabs(p[i].get_x() - mid_point.get_x()) < d:
            strip.append(p[i])

    return min(d, strip_closest(strip, len(strip), d, points))


def closest(p: list):
    points = Points()
    p.sort(key=cmp_to_key(compare_x))
    closest_util(p, len(p), points)
    return (points.minDistance, points.point_1, points.point_2)


if __name__ == '__main__':
    a = []
    a.append(Point(2, 3))
    a.append(Point(12, 30))
    a.append(Point(40, 50))
    a.append(Point(5, 1))
    a.append(Point(12, 10))
    a.append(Point(3, 4))

    print(closest(a))
