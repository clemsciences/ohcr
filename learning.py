"""
Experimental class
"""
import os
import skimage.io as skio
from sklearn.cluster import KMeans
import numpy as np


def get_training_data():
    string_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                      "T", "U", "V", "W", "X", "Y", "Z"]
    l_training_data = []
    X = []
    y = []
    nom_dossier_principal = "lettres"
    dossier_lettres = os.listdir(nom_dossier_principal)
    for nom_dossier_lettres in dossier_lettres:
        if "pathologie" not in nom_dossier_lettres:
            dossier_lettre = os.listdir(os.path.join(nom_dossier_principal, nom_dossier_lettres))
            for nom_dossier_lettre in dossier_lettre:
                if "norm" in nom_dossier_lettre:
                    im = skio.imread(os.path.join(nom_dossier_principal, nom_dossier_lettres, nom_dossier_lettre),
                                     as_grey=True)
                    l_training_data.append([im.flatten(), string_letters.index(nom_dossier_lettres)])
                    X.append(im.flatten())
                    print(string_letters.index(nom_dossier_lettres))
                    y.append(string_letters.index(nom_dossier_lettres))
    # return l_training_data, np.row_stack(X), np.row_stack(y)
    return l_training_data, X, y


def compute_lines():
    barycenters_y = np.array([189.77777777777777, 255.60714285714286, 267.38235294117646, 91.83783783783784, 106.85714285714286, 120.41666666666667, 133.15625, 161.7741935483871, 208.14705882352942, 240.06896551724137, 79.45714285714286, 147.63636363636363, 176.3, 224.96875, 41.18421052631579, 54.56410256410256, 66.55172413793103, 269.03333333333336, 252.63333333333333, 237.28, 210.67741935483872, 223.2, 193.74193548387098, 270.0, 222.75, 194.56756756756758, 209.0810810810811, 237.57692307692307, 253.72222222222223, 220.46875, 253.1764705882353, 270.07894736842104, 187.525, 236.1578947368421, 140.8, 155.73684210526315, 205.3421052631579, 175.12820512820514, 270.9230769230769, 236.3, 254.15, 198.68, 168.47222222222223, 141.59375, 112.84375, 91.66666666666667, 24.192307692307693, 71.36, 49.0, 241.69230769230768, 271.09090909090907, 213.65384615384616, 183.46428571428572, 127.3030303030303, 152.44, 82.84848484848484, 104.86206896551724, 61.29032258064516, 38.625, 18.782608695652176, 271.24, 254.11111111111111, 224.875, 200.75, 118.11428571428571, 139.97058823529412, 165.5909090909091, 27.545454545454547, 49.96296296296296, 72.86666666666666, 93.75, 7.266666666666667, 240.7872340425532, 271.13793103448273, 183.23684210526315, 213.6578947368421, 128.0, 63.225806451612904, 152.86206896551724, 105.67857142857143, 40.57142857142857, 83.95454545454545, 15.5625, 253.15151515151516, 272.61538461538464, 227.45714285714286, 166.78125, 199.28571428571428, 52.53658536585366, 72.275, 93.26829268292683, 138.76470588235293, 34.411764705882355, 116.69444444444444, 83.23333333333333, 15.971428571428572, 61.925925925925924, 103.91666666666667, 128.91304347826087, 212.93103448275863, 151.03333333333333, 182.23333333333332, 240.83333333333334, 272.58620689655174, 114.5, 26.363636363636363, 49.13953488372093, 74.16129032258064, 93.24137931034483, 137.3548387096774, 163.77777777777777, 195.625, 254.03846153846155, 227.17857142857142, 273.3636363636364, 61.55555555555556, 83.79411764705883, 103.35714285714286, 125.13888888888889, 150.28, 35.583333333333336, 179.3548387096774, 13.258064516129032, 211.125, 242.06896551724137, 273.8076923076923, 113.6923076923077, 19.95744680851064, 48.303030303030305, 93.1875, 136.85714285714286, 70.92105263157895, 163.0, 255.7826086956522, 192.7608695652174, 225.2972972972973, 273.4848484848485, 9.066666666666666, 150.70731707317074, 241.2826086956522, 58.02857142857143, 176.91666666666666, 209.48387096774192, 36.303030303030305, 84.31428571428572, 102.23076923076923, 126.34375, 275.1034482758621, 44.06382978723404, 226.4, 21.85, 257.8918918918919, 275.38709677419354, 71.09302325581395, 93.1842105263158, 114.89473684210526, 139.0, 164.52777777777777, 194.8918918918919, 81.76470588235294, 103.93333333333334, 31.565217391304348, 55.76190476190476, 126.32142857142857, 152.77777777777777, 177.52, 245.22222222222223, 276.72727272727275, 212.0, 70.46153846153847, 45.33802816901409, 91.02272727272727, 276.9642857142857, 114.81818181818181, 260.5952380952381, 16.514285714285716, 230.0, 138.625, 194.47727272727272, 165.59375, 99.57692307692308, 122.54545454545455, 277.6818181818182, 245.2258064516129, 57.138888888888886, 75.78125, 149.6206896551724, 210.67857142857142, 178.8235294117647, 30.15, 135.96969696969697, 261.06666666666666, 277.9583333333333, 44.44444444444444, 64.66666666666667, 108.4375, 163.5, 16.36111111111111, 86.11538461538461, 195.02941176470588, 229.72, 246.40740740740742, 279.4, 75.56, 213.25806451612902, 35.32142857142857, 56.37931034482759, 95.96551724137932, 123.96428571428571, 149.80555555555554, 178.71428571428572, 9.7, 280.05, 263.64102564102564, 230.91176470588235, 166.075, 21.756756756756758, 44.86486486486486, 67.25641025641026, 87.45714285714286, 110.93939393939394, 136.94444444444446, 197.97435897435898, 280.76190476190476, 247.5, 212.8846153846154, 96.6774193548387, 183.04, 124.08, 153.05, 33.666666666666664, 55.2, 77.76190476190476, 8.777777777777779, 281.1714285714286, 264.97297297297297, 167.69230769230768, 229.7, 137.56521739130434, 199.62264150943398, 109.3695652173913, 22.256410256410255, 43.16279069767442, 67.57894736842105, 84.39285714285714, 249.6341463414634, 282.3333333333333, 217.1891891891892, 93.11363636363636, 124.8529411764706, 154.82051282051282, 185.11111111111111, 77.66666666666667, 55.95652173913044, 11.379310344827585, 29.88, 282.42424242424244, 267.42424242424244, 233.34146341463415, 200.24324324324326, 19.842105263157894, 45.09090909090909, 65.44736842105263, 83.94444444444444, 171.64285714285714, 139.48717948717947, 108.03125, 251.85714285714286, 266.96, 282.5806451612903, 218.38181818181818, 188.0, 155.76363636363635, 123.37777777777778, 55.0, 94.35, 30.642857142857142, 71.75, 5.393939393939394]).reshape(-1, 1)
    km = KMeans(26)
    km.fit(barycenters_y)
    print(km.labels_)


if __name__ == "__main__":
    compute_lines()



