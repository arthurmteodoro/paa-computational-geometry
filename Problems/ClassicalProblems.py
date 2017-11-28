from Representations.Point import Point
from Representations.Line import Line
from Representations.Circle import Circle
from Representations.Polygon import Polygon
from Representations.LineSegment import LineSegment
from Sets.Set import Set
import math
import copy


def distance_between_two_points(pa: Point, pb: Point):
    """
    Get a distance between two points
    :param pa - Point A
    :param pb - Point B
    :return distance between point A and B
    """
    return math.sqrt(pow(pb.get_x() - pa.get_x(), 2) + pow(pb.get_y() - pa.get_y(), 2))


def distance_between_one_line_and_one_point(p: Point, l: Line):
    return (math.fabs(l.get_a() * p.get_x() + l.get_a() * p.get_y() + l.get_c())) / \
           math.sqrt(pow(l.get_a(), 2) + pow(l.get_b(), 2))


def area_of_a_circle(c: Circle):
    return math.pi * pow(c.get_radius(), 2)


def polygon_sort(poly: Polygon):
    corners = poly.get_list_points()
    n = len(corners)
    cx = 0
    cy = 0

    for i in corners:
        cx += i.get_x()
        cy += i.get_y()

    cx = cx / float(n)
    cy = cy / float(n)

    corners_with_angles = []
    for i in corners:
        dx = i.get_x() - cx
        dy = i.get_y() - cy
        an = (math.atan2(dy, dx) + 2.0 * math.pi) % (2.0 * math.pi)
        corners_with_angles.append((dx, dy, an))

    corners_with_angles.sort(key=lambda tup: tup[2])
    return corners_with_angles


def polygon_area(poly: Polygon):
    corners = polygon_sort(poly)
    n = len(corners)
    area = 0.0

    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0

    return area


def convex_polygon(poly: Polygon):
    if len(poly.get_list_points()) < 3:
        return False

    list_points = poly.get_list_points()

    res = 0
    for i in range(len(list_points)):
        p = list_points[i]
        tmp = list_points[((i+1) % len(list_points))]
        vx = tmp.get_x() - p.get_x()
        vy = tmp.get_y() - p.get_y()
        v = Point(vx, vy)
        u = list_points[((i+2) % len(list_points))]

        if i == 0:
            res = u.get_x() * v.get_y() - u.get_y() * v.get_x() + v.get_x() * p.get_y() - v.get_y() * p.get_x()
        else:
            new_res = u.get_x() * v.get_y() - u.get_y() * v.get_x() + v.get_x() * p.get_y() - v.get_y() * p.get_x()
            if (new_res > 0 and res < 0) or (new_res < 0 and res > 0):
                return False

    return True


def side_of_circle(a: Point, b: Point, c: Point, d: Point):
    ax = a.get_x()
    ay = a.get_y()

    bx = b.get_x() - ax
    by = b.get_y() - ay
    bw = bx ** 2 + by ** 2

    cx = c.get_x() - ax
    cy = c.get_y() - ay
    cw = cx ** 2 + cy ** 2

    dx = d.get_x() - ax
    dy = d.get_y() - ay

    d1 = cy * bw - by * cw
    d2 = bx * cw - cx * bw
    d3 = by * cx - bx * cy

    d = d1 * dx + d2 * dy + d3 * (dx ** 2 + dy ** 2)

    if d != 0:
        if d > 0:
            return 1
        else:
            return -1
    else:
        return 0


def __nearest_distance(seg: LineSegment, p: Point):
    a = p.get_x() - seg.get_a().get_x()
    b = p.get_y() - seg.get_a().get_y()
    c = seg.get_b().get_x() - seg.get_a().get_x()
    d = seg.get_b().get_x() - seg.get_a().get_y()

    dot = a * c + b * d
    q = c ** 2 + d ** 2
    param = -1

    if q != 0:
        param = dot / q

    if param < 0:
        xx = seg.get_a().get_x()
        yy = seg.get_a().get_y()
    elif param > 1:
        xx = seg.get_b().get_x()
        yy = seg.get_b().get_y()
    else:
        xx = seg.get_a().get_x() + param * c
        yy = seg.get_a().get_y() + param * d

    dx = p.get_x() - xx
    dy = p.get_y() - yy
    return math.sqrt(dx ** 2 + dy ** 2)


def closest_point(seg: LineSegment, points: Set):
    distance = math.inf
    point = None

    for i in points.get_iterator():
        value = __nearest_distance(seg, i)
        if value < distance:
            distance = value
            point = Point(i.get_x(), i.get_y())

    return point


def orient_2d(a: Point, b: Point, c: Point):
    first = (b.get_y() - a.get_y()) * (c.get_x() - b.get_x())
    second = (c.get_y() - b.get_y()) * (b.get_x() - a.get_x())
    det = first - second

    if det == 0:
        return 0
    elif det > 0:
        return 1
    else:
        return -1


def __point_in_segment(p: Point, s: LineSegment):
    px = p.get_x()
    py = p.get_y()

    sa_x = s.get_a().get_x()
    sa_y = s.get_a().get_y()
    sb_x = s.get_b().get_x()
    sb_y = s.get_b().get_y()

    if px <= max(sa_x, sb_x) and px >= min(sa_x, sb_x) and \
                    py <= max(sa_y, sb_y) and py >= min(sa_y, sb_y):
        return True
    else:
        return False


def __points_orientation(p: Point, q: Point, r: Point):
    value = (q.get_y() - p.get_y()) * (r.get_x() - q.get_x()) - (q.get_x() - p.get_x()) * (r.get_y() - q.get_y())

    if value == 0:
        return 0
    elif value > 0:
        return 1
    else:
        return 2


def intersection_two_lines_segments(seg1: LineSegment, seg2: LineSegment):
    o1 = __points_orientation(seg1.get_a(), seg1.get_b(), seg2.get_a())
    o2 = __points_orientation(seg1.get_a(), seg1.get_b(), seg2.get_b())
    o3 = __points_orientation(seg2.get_a(), seg2.get_b(), seg1.get_a())
    o4 = __points_orientation(seg2.get_a(), seg2.get_b(), seg1.get_b())

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and __point_in_segment(seg2.get_a(), seg1):
        return True
    if o2 == 0 and __point_in_segment(seg2.get_b(), seg1):
        return True
    if o3 == 0 and __point_in_segment(seg1.get_a(), seg2):
        return True
    if o4 == 0 and __point_in_segment(seg1.get_b(), seg2):
        return True

    return False


def point_in_polygon(p: Point, polygon: Polygon):
    cn = 0
    v = copy.deepcopy(polygon.get_list_points())
    v.append(v[0])

    for i in range(len(v)-1):
        if (v[i].get_y() <= p.get_y() and v[i+1].get_y() > p.get_y()) or \
           (v[i].get_y() > p.get_y() and v[i+1].get_y() <= p.get_y()):

            vt = (p.get_y() - v[i].get_y()) / float(v[i+1].get_y() - v[i].get_y())
            if p.get_x() < (v[i].get_x() + vt * (v[i+1].get_x() - v[i].get_x())):
                cn += 1

    return True if (cn % 2) == 1 else False


def is_convex(a: Point, b: Point, c: Point):
    crossp = (b.get_x() - a.get_x()) * (c.get_y() - a.get_y()) - (b.get_y() - a.get_y()) * (c.get_x() - a.get_x())
    if crossp >= 0:
        return True
    return False


def in_triangle(a: Point, b: Point, c: Point, p: Point):
    L = [0, 0, 0]
    eps = 0.000000000001
    L[0] = ((b.get_y() - c.get_y()) * (p.get_x() - c.get_x()) + (c.get_x() - b.get_x()) * (p.get_y() - c.get_y())) / \
           (((b.get_y() - c.get_y()) * (a.get_x() - c.get_x()) + (c.get_x() - b.get_x()) * (a.get_y() - c.get_y())) + eps)
    L[1] = ((c.get_y() - a.get_y()) * (p.get_x() - c.get_x()) + (a.get_x() - c.get_x()) * (p.get_y() - c.get_y())) / \
           (((b.get_y() - c.get_y()) * (a.get_x() - c.get_x()) + (c.get_x() - b.get_x()) * (a.get_y() - c.get_y())) + eps)
    L[2] = 1 - L[0]

    for x in L:
        if x >= 1 or x <= 0:
            return False
    return True


def is_clockwise(poly: Polygon):
    points = poly.get_list_points()
    sum_p = (points[0].get_x() - points[len(points)-1].get_x()) * (points[0].get_y() + points[len(points)-1].get_y())
    for i in range(len(points)-1):
        sum_p += (points[i+1].get_x() - points[i].get_x()) * (points[i+1].get_y() + points[i].get_y())
    if sum_p > 0:
        return True
    return False


def get_ear(poly: list):
    size = len(poly)

    if size < 3:
        return []
    if size == 3:
        tri = (poly[0], poly[1], poly[2])
        for i in poly:
            del poly[:]
            return tri

    for i in range(size):
        tritest = False
        p1 = poly[(i-1) % size]
        p2 = poly[i % size]
        p3 = poly[(i+1) % size]

        if is_convex(p1, p2, p3):
            for x in poly:
                if not (x in (p1, p2, p3)) and in_triangle(p1, p2, p3, x):
                    tritest = True
            if not tritest:
                del poly[i % size]
                return (p1, p2, p3)
    return []


if __name__ == '__main__':
    # test point in polygon
    p = Polygon()
    p.add_segment(LineSegment(Point(0, 0), Point(5, 0)))
    p.add_segment(LineSegment(Point(5, 0), Point(5, 5)))
    p.add_segment(LineSegment(Point(5, 5), Point(0, 5)))
    p.add_segment(LineSegment(Point(0, 5), Point(0, 0)))

    convex_polygon(copy.deepcopy(p))

    tri = []
    pts = copy.deepcopy(p.get_list_points())
    plist = pts[::-1] if is_clockwise(p) else pts[:]
    while len(plist) >= 3:
        a = get_ear(plist)
        if a == []:
            break
        tri.append(a)

    print('aaa')