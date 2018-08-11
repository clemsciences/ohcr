"""

"""

import os

import numpy as np

import point_group as gpoints

import skimage.io as skio
import skimage.feature as skf
import skimage.transform as sktr


__author__ = 'Clément Besnier'


class ProximitySegmentation:
    """
    Segmentation class
    """
    def __init__(self, edge_points: gpoints.PointGroup, maximum_distance):
        """

        :param edge_points: list of gpoints.Point
        :param maximum_distance: Maximum distance below which a Point and a PointGroup are considered close enough
        """
        self.edge_points = edge_points
        self.maximum_distance = maximum_distance
        self.tags = []

    def segment(self):
        """

        :return: list of PointGroup
        """
        current_label = 0
        self.tags.append(gpoints.PointGroup())
        self.tags[current_label].append_point(self.edge_points.remove_point(0))
        while self.edge_points.points_number > 0:

            while self.tags[current_label].is_close_enough(self.edge_points, self.maximum_distance):
                i = 0
                number = self.edge_points.points_cluster
                while i < number:
                    if self.tags[current_label].calculate_minimal_distance(self.edge_points.points_cluster[i]) \
                            < self.maximum_distance:
                        self.tags[current_label].append_point(self.edge_points.remove_point(i))
                        number -= 1
                    else:
                        i += 1
            current_label += 1
            self.tags.append(gpoints.PointGroup())
            self.tags[current_label].append_point(self.edge_points.remove_point(0))
        aze = 0
        n_eti = len(self.tags)
        while aze < n_eti:
            if self.tags[aze].points_number < 10:
                del self.tags[aze]
                n_eti -= 1
            else:
                aze += 1
        return self.tags

    def segment_lines(self):
        assert len(self.tags) > 1

        # TODO find PointGroup with approximately common height on a sheet
        pass


def script_segmentation():
    """
    Retrieves the picture
    Transforms it in the wantd format
    The image is segmented into several frames
    The result is stored
    :return:
    """
    gray_image = skio.imread("entree\\papier_lettre.jpg", as_grey=True)
    # image = sktr.rotate(image, 3.1415/2.)
    tt = 300
    uu = 500
    image_resize = sktr.resize(gray_image, (tt, uu))
    # print(image_resize[10:20, 10:20])
    # image_gris = skc.rgb2gray(image_resize)
    # print(image_resize[10:20, 10:20])
    # skio.imsave("entree\\gris.jpg", image_resize)
    # image_gau = skfi.gaussian(image_resize, 0.1)
    # image_sobel = skfi.sobel(image_gau)
    # print(image_sobel[10:20, 10:20])
    # skio.imsave("entree\\sobel.jpg", image_sobel)
    # a = image_sobel > 0.005*np.ones(image_sobel.shape)
    image_canny = np.uint8(skf.canny(image_resize))*255
    # print(image_canny[10:20, 100:150])
    skio.imsave("entree\\canny.jpg", image_canny)
    # n_points_choisis = int(tt*uu*0.1)
    # l_points = []
    # yy = 0
    # while yy < n_points_choisis:
    #    point = gp.Point(int(random()*tt), int(random()*uu))
    #    if image_canny[point.y, point.x] == 255:
    #        l_points.append(point)
    #   yy += 1
    pc = gpoints.PointGroup()
    for i in range(uu):
        for j in range(tt):
            if image_canny[j, i] == 255:
                pc.append_point(gpoints.Point(i, j))
    spp = ProximitySegmentation(pc, 3)
    tags = spp.segment()
    hh = 0
    print(tags)
    for gp in tags:
        if gp.calculate_min_y() - 5 >= 0 and gp.calculate_max_y()+5 < tt and \
                gp.calculate_min_x()-5 >= 0 and gp.calculate_max_x()+5 < uu:
            skio.imsave(os.path.join("lettres", str(hh) + ".jpg"),
                        image_resize[gp.calculate_min_y() - 5:gp.calculate_max_y() + 5,
                        gp.calculate_min_x() - 5:gp.calculate_max_x() + 5])
            hh += 1


def script_binarise_normalise():
    main_folder_name = "lettres"
    characters_folder = os.listdir(main_folder_name)
    for characters_folder_name in characters_folder:
        character_folder = os.listdir(os.path.join(main_folder_name, characters_folder_name))
        for character_folder_name in character_folder:
            im = skio.imread(os.path.join(main_folder_name, characters_folder_name, character_folder_name), as_grey=True)
            im_resize = sktr.resize(im, (20, 20))
            im_resize = sktr.rotate(im_resize, 3.1415/2.)
            skio.imsave(os.path.join(main_folder_name, characters_folder_name, "norm_"+character_folder_name), im_resize)


def remove_too_much():
    main_folder_name = "lettres"
    characters_folder = os.listdir(main_folder_name)
    for characters_folder_name in characters_folder:
        character_folder = os.listdir(os.path.join(main_folder_name, characters_folder_name))
        for character_folder_name in character_folder:
            if "norm_norm" in character_folder_name:
                os.remove(os.path.join(main_folder_name, characters_folder_name, character_folder_name))


if __name__ == "__main__":
    # script_segmentation()
    remove_too_much()
