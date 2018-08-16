"""

"""

import math

__author__ = "Clément Besnier"


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, autre_point):
        return math.sqrt((self.x - autre_point.x)**2 + (self.y - autre_point.y)**2)


class PointGroup:
    """
    Point cluster
    """
    def __init__(self):
        self.points_cluster = []
        self.points_number = 0
        self.barycenter = None
        self.line = None
        self.center = None

    def attribute(self, points_group: list):
        self.points_cluster = points_group
        self.points_number = len(points_group)

    def append_point(self, point: Point):
        self.points_cluster.append(point)
        self.points_number += 1

    def calculate_barycenter(self):
        sum_x = 0
        sum_y = 0
        for point in self.points_cluster:
            sum_x += point.x
            sum_y += point.y
        self.barycenter = Point(sum_x / self.points_number, sum_y / self.points_number)

    def calculate_minimal_distance(self, point: Point):
        minimal_distance = 999999
        for other_point in self.points_cluster:
            distance = point.distance(other_point)
            if distance < minimal_distance:
                minimal_distance = distance
        return minimal_distance

    def is_close_enough(self, other_points_group, maximal_distance):
        assert isinstance(other_points_group, PointGroup)
        near = False
        for point in self.points_cluster:
            for other_point in other_points_group.points_cluster:
                if point.distance(other_point) < maximal_distance:
                    near = True
                    break
        return near

    def consult(self, i):
        return self.points_cluster[i]

    def remove_point(self, i):
        if len(self.points_cluster) > 0 and 0 <= i < len(self.points_cluster):
            point = self.points_cluster[i]
            del self.points_cluster[i]
            self.points_number -= 1
            return point
        else:
            return None

    def calculate_min_x(self):
        min_x = 9999999
        for point in self.points_cluster:
            if point.x < min_x:
                min_x = point.x
        return min_x

    def calculate_max_x(self):
        max_x = -9999999
        for point in self.points_cluster:
            max_x = point.x
        return max_x

    def calculate_min_y(self):
        min_y = 99999999
        for point in self.points_cluster:
            if point.y < min_y:
                min_y = point.y
        return min_y

    def calculate_max_y(self):
        max_y = -99999999
        for point in self.points_cluster:
            if max_y < point.y:
                max_y = point.y
        return max_y

    def calculate_center(self):
        min_x, min_y, max_x, max_y = self.calculate_min_x(), self.calculate_min_y(), self.calculate_max_x(), \
                                     self.calculate_max_y()
        self.center = Point((max_x - min_x)/2. + min_x, (max_y - min_y)/2. + min_y)
        return self.center

    def is_on_the_same_line(self, other_pg, threshold):
        return abs(self.center.y - other_pg.center.y) < threshold
