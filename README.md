# ELE778
## Dependencies
* linux
* python
* make
* tar
* gnuplot
* numpy
* pyyaml
* matplotlib
* re
* fnmatch
* python3-qt5
* python3-matplotlib-qt5


## preparation des datasets
`$ make prep`
Cette commande decompresse les fichiers TiDigits.

## Choix 1: ligne de commande

configuration du fichier run.py

### Variables a modifier
* verbose = niveau de verbose
* Si evalsample est a False alors sample_file n'est pas pris en compte
* dataset_size = taille du dataset (40,50 ou 60)
* Si sex_classification est a True alors le reseau classifie les chiffres selon homme et femme
sinon il classifie que les chiffres de 1 a 9.
* Les fonction d'activations disponibles sont 'sigmoid','tanh' ou 'sotplus'
* Les fonctions de cout disponibles sont 'quadratic','cross-entropy'.
* Les fonctions de regularisation disponibles sont : 'L2', 'L1','none'

* epochs       = nombre d'epochs
* batch_size   = taille des mini-batchs
* early_stop_n = arrete si erreur il y un plateau sur l'erreur de validation en faisant la moyenne sur les early_stop_n dernieres valeurs

### Demarrer le script
```
$ ./run.py
```
##Choix 2: gui
```
$ ./neuralNetworkGui.py
```
* 1) Appuyer sur l'icon Load (Attendre la fin du chargement)
* 2) Faire la selection des parametres
* 3) Appuyer l'icon play
* 4) Appuyer l'icon train

Note: Les boutons du menu ne sont pas fonctionnels (save, load et reset)
