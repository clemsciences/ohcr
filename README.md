# OHCR
Traitement d'image pour isoler des caractères dans une image et apprentissage pour la reconnaissance.

L'algorithme pour isoler les caractères dans une image se fait de la manière suivante :  
- On récupère une image
- On applique le filtre de Canny pour ne conserver que les contours des caractères
- Tous les points qui sont des contours sont retenus
- On regroupe tous ces points par paquet dont le critère de regroupement est la distance inter-groupe
- On retient les groupes qui ont au moins un certain nombre de points
- On encadre les caractères obtenus
- On enregistre l'image final
