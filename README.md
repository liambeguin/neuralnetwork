# ELE778
## Dependencies
* linux
* python
* make
* gnuplot

* numpy    
* pyyaml
* matplotlib
* re 
* fnmatch
* python3-qt5
* python3-matplotlib-qt5


* Les fichiers .txt de sorties se trouvent dans le repertoire `out/train` 
* Les courbes pour chaque chiffre se trouvent dans le repertoire `plot/comp`
lancer en ligne de commande:
# Etape 1
configuration du fichier run.py
## Variables a modifier
* verbose = niveau de verbose
* Si evalsample est a False alors sample_file n'est pas pris en compte 
* dataset_size = taille du dataset (40,50 ou 60)
* Si sex_classification est a True alors le reseau classifie les chiffres selon homme et femme
sinon il classifie que les chiffres de 1 a 9.
* La fonction d'activation 'sigmoid' ne peut prendre que la fonction cost = 'cross-entropy'.
  Les fonctions d'activation 'tanh' et 'softplus' ne peuvent prendre que cost = 'quadratic' 
* Les fonctions d'activations dissponible sont : 'L2', 'L1','none', 'self-decay'

epochs       = nombre d'epochs
batch_size   = taille des mini-batchs
early_stop_n = arrete si erreur il y un plateau sur l'erreur de validation en faisant la moyenne sur les early_stop_n dernieres valeurs
