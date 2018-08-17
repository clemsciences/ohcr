"""

"""

import os

import numpy as np
import scipy.ndimage

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
                number = self.edge_points.points_number
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

    def calculate_sorted_tags(self):
        assert len(self.tags) > 1
        sorted_tags = []
        for i, tag in enumerate(self.tags):
            tag.calculate_center()
        for i, tag in enumerate(self.tags):
            if i < len(self.tags) - 1:
                next_gp = self.tags[i]
                for j, tagj in enumerate(self.tags[i+1:]):
                    if self.tags[j].center.x < next_gp.center.xx:
                        next_gp = self.tags[j]
                    elif self.tags[j].center.x == next_gp.center.x:
                        if self.tags[j].center.y < next_gp.center.y:
                            next_gp = self.tags[j]
                sorted_tags.append(next_gp)
        return sorted_tags

    def segment_lines(self, threshold):
        # width, height, angle_step, n_most_briliant

        assert len(self.tags) > 1
        # TODO find PointGroup with approximately common height on a sheet
        for i, tag in enumerate(self.tags):
            tag.calculate_center()
            tag.line = i
        categories = list(range(len(self.tags)))
        for i in range(len(self.tags)):
            if i < len(self.tags)-1:
                for j in range(i+1, len(self.tags)):
                    if self.tags[i].is_on_the_same_line(self.tags[j], threshold):
                        categories[j] = categories[i]
                        self.tags[j].line = categories[i]

        return categories

        # print(barycenters_points)
        # barycenters_xy = [(point.x, point.y) for point in barycenters_points]

        # thetas = np.deg2rad(np.arange(-90., 90., angle_step))
        # diag_len = int(round(np.math.sqrt(width ** 2 + height ** 2)))
        # rhos = np.linspace(-diag_len, diag_len, 2*diag_len)
        #
        # cos_t = np.cos(thetas)
        # sin_t = np.sin(thetas)
        # num_thetas = len(thetas)
        #
        # acc = np.zeros((2*diag_len, num_thetas), dtype=np.uint8)
        # for x, y in barycenters_xy:
        #     for theta in range(num_thetas):
        #         rho = diag_len + int(round(x*cos_t+y*sin_t))
        #         acc[rho, theta] += 1
        # # find the most briliant points
        # for n in range(n_most_briliant):
        #     index = np.argmax(acc)
        #     acc[index] = 0.


# [189.77777777777777, 255.60714285714286, 267.38235294117646, 91.83783783783784, 106.85714285714286,
# 120.41666666666667, 133.15625, 161.7741935483871, 208.14705882352942, 240.06896551724137, 79.45714285714286,
# 147.63636363636363, 176.3, 224.96875, 41.18421052631579, 54.56410256410256, 66.55172413793103, 269.03333333333336,
# 252.63333333333333, 237.28, 210.67741935483872, 223.2, 193.74193548387098, 270.0, 222.75, 194.56756756756758,
# 209.0810810810811, 237.57692307692307, 253.72222222222223, 220.46875, 253.1764705882353, 270.07894736842104,
# 187.525, 236.1578947368421, 140.8, 155.73684210526315, 205.3421052631579, 175.12820512820514, 270.9230769230769,
# 236.3, 254.15, 198.68, 168.47222222222223, 141.59375, 112.84375, 91.66666666666667, 24.192307692307693, 71.36,
# 49.0, 241.69230769230768, 271.09090909090907, 213.65384615384616, 183.46428571428572, 127.3030303030303, 152.44,
# 82.84848484848484, 104.86206896551724, 61.29032258064516, 38.625, 18.782608695652176, 271.24, 254.11111111111111,
# 224.875, 200.75, 118.11428571428571, 139.97058823529412, 165.5909090909091, 27.545454545454547, 49.96296296296296,
# 72.86666666666666, 93.75, 7.266666666666667, 240.7872340425532, 271.13793103448273, 183.23684210526315,
# 213.6578947368421, 128.0, 63.225806451612904, 152.86206896551724, 105.67857142857143, 40.57142857142857,
# 83.95454545454545, 15.5625, 253.15151515151516, 272.61538461538464, 227.45714285714286, 166.78125,
# 199.28571428571428, 52.53658536585366, 72.275, 93.26829268292683, 138.76470588235293, 34.411764705882355,
# 116.69444444444444, 83.23333333333333, 15.971428571428572, 61.925925925925924, 103.91666666666667,
# 128.91304347826087, 212.93103448275863, 151.03333333333333, 182.23333333333332, 240.83333333333334,
# 272.58620689655174, 114.5, 26.363636363636363, 49.13953488372093, 74.16129032258064, 93.24137931034483,
# 137.3548387096774, 163.77777777777777, 195.625, 254.03846153846155, 227.17857142857142, 273.3636363636364,
# 61.55555555555556, 83.79411764705883, 103.35714285714286, 125.13888888888889, 150.28, 35.583333333333336,
# 179.3548387096774, 13.258064516129032, 211.125, 242.06896551724137, 273.8076923076923, 113.6923076923077,
# 19.95744680851064, 48.303030303030305, 93.1875, 136.85714285714286, 70.92105263157895, 163.0, 255.7826086956522,
# 192.7608695652174, 225.2972972972973, 273.4848484848485, 9.066666666666666, 150.70731707317074, 241.2826086956522,
# 58.02857142857143, 176.91666666666666, 209.48387096774192, 36.303030303030305, 84.31428571428572,
# 102.23076923076923, 126.34375, 275.1034482758621, 44.06382978723404, 226.4, 21.85, 257.8918918918919,
# 275.38709677419354, 71.09302325581395, 93.1842105263158, 114.89473684210526, 139.0, 164.52777777777777,
# 194.8918918918919, 81.76470588235294, 103.93333333333334, 31.565217391304348, 55.76190476190476,
# 126.32142857142857, 152.77777777777777, 177.52, 245.22222222222223, 276.72727272727275, 212.0, 70.46153846153847,
# 45.33802816901409, 91.02272727272727, 276.9642857142857, 114.81818181818181, 260.5952380952381, 16.514285714285716,
#  230.0, 138.625, 194.47727272727272, 165.59375, 99.57692307692308, 122.54545454545455, 277.6818181818182,
# 245.2258064516129, 57.138888888888886, 75.78125, 149.6206896551724, 210.67857142857142, 178.8235294117647, 30.15,
# 135.96969696969697, 261.06666666666666, 277.9583333333333, 44.44444444444444, 64.66666666666667, 108.4375, 163.5,
# 16.36111111111111, 86.11538461538461, 195.02941176470588, 229.72, 246.40740740740742, 279.4, 75.56,
# 213.25806451612902, 35.32142857142857, 56.37931034482759, 95.96551724137932, 123.96428571428571,
# 149.80555555555554, 178.71428571428572, 9.7, 280.05, 263.64102564102564, 230.91176470588235, 166.075,
# 21.756756756756758, 44.86486486486486, 67.25641025641026, 87.45714285714286, 110.93939393939394,
# 136.94444444444446, 197.97435897435898, 280.76190476190476, 247.5, 212.8846153846154, 96.6774193548387, 183.04,
# 124.08, 153.05, 33.666666666666664, 55.2, 77.76190476190476, 8.777777777777779, 281.1714285714286,
# 264.97297297297297, 167.69230769230768, 229.7, 137.56521739130434, 199.62264150943398, 109.3695652173913,
# 22.256410256410255, 43.16279069767442, 67.57894736842105, 84.39285714285714, 249.6341463414634, 282.3333333333333,
# 217.1891891891892, 93.11363636363636, 124.8529411764706, 154.82051282051282, 185.11111111111111, 77.66666666666667,
#  55.95652173913044, 11.379310344827585, 29.88, 282.42424242424244, 267.42424242424244, 233.34146341463415,
# 200.24324324324326, 19.842105263157894, 45.09090909090909, 65.44736842105263, 83.94444444444444,
# 171.64285714285714, 139.48717948717947, 108.03125, 251.85714285714286, 266.96, 282.5806451612903,
# 218.38181818181818, 188.0, 155.76363636363635, 123.37777777777778, 55.0, 94.35, 30.642857142857142, 71.75,
# 5.393939393939394]


def script_segmentation(src_folder, src_picture, dst_folder):
    """
    Retrieves the picture
    Transforms it in the wantd format
    The image is segmented into several frames
    The result is stored
    :return:
    """
    gray_image = skio.imread(os.path.join(src_folder, src_picture), as_grey=True)
    # gray_image = sktr.rotate(gray_image, -90.)
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
    energy = calculate_energy(image_canny)
    # print(image_canny[10:20, 100:150])
    skio.imsave(os.path.join(src_folder, "canny.jpg"), image_canny)
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
    spp.segment()
    print(spp.segment_lines(10))
    hh = 0
    # print(spp.tags)
    if not os.path.exists(dst_folder):
        os.mkdir(dst_folder)
    for gp in spp.tags:
        if gp.calculate_min_y() - 5 >= 0 and gp.calculate_max_y()+5 < tt and \
                gp.calculate_min_x()-5 >= 0 and gp.calculate_max_x()+5 < uu:
            mini_im = image_resize[gp.calculate_min_y() - 5:gp.calculate_max_y() + 5,
                      gp.calculate_min_x() - 5:gp.calculate_max_x() + 5]

            skio.imsave(os.path.join(dst_folder, str(hh) + ".jpg"), sktr.rotate(mini_im, -90., resize=True))
            print("numero", hh, "ligne", gp.line)
            hh += 1


def calculate_energy(image):
    # size = 11
    energy = np.zeros(image.shape)
    size_max = 45
    for size in range(3, size_max, 4):
        kernel = np.ones((size, size))
        energy += (size_max-size)/255*scipy.ndimage.filters.convolve(image, kernel)
    energy = 1000*(energy == np.zeros(image.shape)) + energy
    return energy


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
    script_segmentation("input", "characters_sheet.jpg", "letters")
    # remove_too_much()
