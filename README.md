# OHCR (Optical Hand-written Character Recognition)
### Image processing to isolate hand-written characters in an image and to learn recognize them.
The algorithm is done in different steps:
- An image is retrieved
- The Canny's filter is used to keep only characters edges
- All edge points are kept and clustered whose criteria is the inter-group distance
- Clusters with unsufficient points are removed
- Clusters are framed
- The final image is stored

#### Line extraction
The edge image is convoluted with ones kernels of sifferent sizes. The larger the kernel size is, the lesswr weight it has. Then, lines are defined as shortest paths from one side to the other side.


### Traitement d'image pour isoler des caractères dans une image et apprendre à les reconnaître

L'algorithme pour isoler les caractères dans une image se fait de la manière suivante :  
- On récupère une image
- On applique le filtre de Canny pour ne conserver que les contours des caractères
- Tous les points qui sont des contours sont retenus
- On regroupe tous ces points par paquet dont le critère de regroupement est la distance inter-groupe
- On retient les groupes qui ont au moins un certain nombre de points
- On encadre les caractères obtenus
- On enregistre l'image final

A lire : article dans le magazine Programmez! de mars 2019 #227 "Python : faire une intelligence artificielle pour de la reconnaissance de caractères avec OpenCV et Keras".
