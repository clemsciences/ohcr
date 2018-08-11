"""
Experimental class
"""
import os
import skimage.io as skio


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

