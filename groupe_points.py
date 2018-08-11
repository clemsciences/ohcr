
import skimage as sk
import math
import sys

__author__ = "Clément Besnier"


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, autre_point):
        return math.sqrt((self.x - autre_point.x)**2 + (self.y - autre_point.y)**2)


class GroupePoint:
    """
    Point cluster
    Groupe de points
    """
    def __init__(self):
        self.groupe_points = []
        self.nombre_points = 0

    def attribuer(self, groupe_point):
        self.groupe_points = groupe_point
        self.nombre_points = len(groupe_point)

    def ajouter_point(self, point):
        self.groupe_points.append(point)
        self.nombre_points += 1

    def calculer_barycentre(self):
        somme_x = 0
        somme_y = 0
        for point in self.groupe_points:
            somme_x += point.x
            somme_y += point.y
        return Point(somme_x/self.nombre_points, somme_y/self.nombre_points)

    def calculer_distance_minimale(self, point):
        distance_minimale = 999999
        for autre_point in self.groupe_points:
            distance = point.distance(autre_point)
            if distance < distance_minimale:
                distance_minimale = distance
        return distance_minimale

    def est_suffisamment_proche(self, autre_groupe_point, distance_maximale):
        proche = False
        for point in self.groupe_points:
            for autre_point in autre_groupe_point.groupe_points:
                if point.distance(autre_point) < distance_maximale:
                    proche = True
                    break
        return proche

    def consulter(self, i):
        return self.groupe_points[i]

    def retirer_point(self, i):
        if len(self.groupe_points) > 0 and 0 <= i < len(self.groupe_points):
            point = self.groupe_points[i]
            del self.groupe_points[i]
            self.nombre_points -= 1
            return point
        else:
            return None

    def calculer_min_x(self):
        min_x = 9999999
        for point in self.groupe_points:
            if point.x < min_x:
                min_x = point.x
        return min_x

    def calculer_max_x(self):
        max_x = -9999999
        for point in self.groupe_points:
            max_x = point.x
        return max_x

    def calculer_min_y(self):
        min_y = 99999999
        for point in self.groupe_points:
            if point.y < min_y:
                min_y = point.y
        return min_y

    def calculer_max_y(self):
        max_y = -99999999
        for point in self.groupe_points:
            if max_y < point.y:
                max_y = point.y
        return max_y
