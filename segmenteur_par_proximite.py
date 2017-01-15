# -*-coding:utf-8-*-
__author__ = 'besnier'

import groupe_points as gp
import skimage as sk
import skimage.io as skio
import skimage.feature as skf
import skimage.transform as sktr
import skimage.color as skc
import skimage.filters as skfi
import numpy as np
import os
from random import random
import skimage.draw as skd


class Segmenteur_par_proximite:
    def __init__(self, points_contour, distance_maximale):
        self.points_contour = points_contour
        self.distance_maximale = distance_maximale
        self.etiquettes = []

    def segmenter(self):
        label_courant = 0
        self.etiquettes.append(gp.GroupePoint())
        self.etiquettes[label_courant].ajouter_point(self.points_contour.retirer_point(0))
        while self.points_contour.nombre_points > 0:

            while self.etiquettes[label_courant].est_suffisamment_proche(self.points_contour, self.distance_maximale):
                i = 0
                nombre = self.points_contour.nombre_points
                while i < nombre:
                    if self.etiquettes[label_courant].calculer_distance_minimale(self.points_contour.groupe_points[i]) < self.distance_maximale:
                        self.etiquettes[label_courant].ajouter_point(self.points_contour.retirer_point(i))
                        nombre -= 1
                    else:
                        i += 1
            label_courant += 1
            self.etiquettes.append(gp.GroupePoint())
            self.etiquettes[label_courant].ajouter_point(self.points_contour.retirer_point(0))
        aze = 0
        n_eti = len(self.etiquettes)
        while aze < n_eti:
            if self.etiquettes[aze].nombre_points < 10:
                del self.etiquettes[aze]
                n_eti -= 1
            else:
                aze += 1
        return self.etiquettes

def script_segmentation():
    image_gris = skio.imread("entree\\papier_lettre.jpg", as_grey=True)
    #image = sktr.rotate(image, 3.1415/2.)
    tt = 300
    uu = 500
    image_resize = sktr.resize(image_gris, (tt, uu))
    #print(image_resize[10:20, 10:20])
    #image_gris = skc.rgb2gray(image_resize)
    #print(image_resize[10:20, 10:20])
    #skio.imsave("entree\\gris.jpg", image_resize)
    #image_gau = skfi.gaussian(image_resize, 0.1)
    #image_sobel = skfi.sobel(image_gau)
    #print(image_sobel[10:20, 10:20])
    #skio.imsave("entree\\sobel.jpg", image_sobel)
    #a = image_sobel > 0.005*np.ones(image_sobel.shape)
    image_canny = np.uint8(skf.canny(image_resize))*255
    #print(image_canny[10:20, 100:150])
    skio.imsave("entree\\canny.jpg", image_canny)
    n_points_choisis = int(tt*uu*0.1)
    #l_points = []
    #yy = 0
    #while yy < n_points_choisis:
    #    point = gp.Point(int(random()*tt), int(random()*uu))
    #    if image_canny[point.y, point.x] == 255:
    #        l_points.append(point)
    #   yy += 1
    pc = gp.GroupePoint()
    for i in range(uu):
        for j in range(tt):
            if image_canny[j, i] == 255:
                pc.ajouter_point(gp.Point(i, j))
    spp = Segmenteur_par_proximite(pc, 3)
    etiquettes = spp.segmenter()
    hh = 0
    print(etiquettes)
    for gp in etiquettes:
        if gp.calculer_min_y() - 5 >= 0 and gp.calculer_max_y()+5 < tt and gp.calculer_min_x()-5 >= 0 and gp.calculer_max_x()+5 <uu:
            skio.imsave("lettres\\"+str(hh)+".jpg", image_resize[gp.calculer_min_y() - 5:gp.calculer_max_y()+5, gp.calculer_min_x()-5:gp.calculer_max_x()+5])
            hh += 1


def script_binarise_normalise():
    nom_dossier_principal = "lettres"
    dossier_lettres = os.listdir(nom_dossier_principal)
    for nom_dossier_lettres in dossier_lettres:
        dossier_lettre = os.listdir(os.path.join(nom_dossier_principal, nom_dossier_lettres))
        for nom_dossier_lettre in dossier_lettre:
            im = skio.imread(os.path.join(nom_dossier_principal, nom_dossier_lettres, nom_dossier_lettre), as_grey=True)
            im_resize = sktr.resize(im, (20, 20))
            im_resize = sktr.rotate(im_resize, 3.1415/2.)
            skio.imsave(os.path.join(nom_dossier_principal, nom_dossier_lettres, "norm_"+nom_dossier_lettre), im_resize)

def supprimer_en_trop():
    nom_dossier_principal = "lettres"
    dossier_lettres = os.listdir(nom_dossier_principal)
    for nom_dossier_lettres in dossier_lettres:
        dossier_lettre = os.listdir(os.path.join(nom_dossier_principal, nom_dossier_lettres))
        for nom_dossier_lettre in dossier_lettre:
            if "norm_norm" in nom_dossier_lettre:
                os.remove(os.path.join(nom_dossier_principal, nom_dossier_lettres, nom_dossier_lettre))


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
                    im = skio.imread(os.path.join(nom_dossier_principal, nom_dossier_lettres, nom_dossier_lettre), as_grey=True)
                    l_training_data.append([im.flatten(), string_letters.index(nom_dossier_lettres)])
                    X.append(im.flatten())
                    print(string_letters.index(nom_dossier_lettres))
                    y.append(string_letters.index(nom_dossier_lettres))
    #return l_training_data, np.row_stack(X), np.row_stack(y)
    return l_training_data, X, y

if __name__ == "__main__":
    #script_segmentation()
    supprimer_en_trop()