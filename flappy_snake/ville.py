from upemtk import *
from random import randint
from time import *

#créée une liste de valeurs aléatoires, on peut choisir le nombre d'éléments dans la liste, et entre un certain intervalle
def liste_aleatoire(nb,mini,maxi):
	lst=[]
	compteur=0
	while compteur<nb:
		aleatoire=randint(mini,maxi)
		lst.append(aleatoire)
		compteur+=1
	return lst   #renvoie cette liste

#créée une liste contenant les coordonnée d'un rectangle et renvoie cette liste
def un_rectange(h,l,hauteur_fenetre,d):
	return [d,hauteur_fenetre-h,d+l,hauteur_fenetre]

#fait appel à la fonction qui créée une liste de coords de rectangle
def coordonnees_rectangles(hauteur,largeur,hauteur_fenetre):
	lst_totale=[]
	i=0
	d=0   # d est le décalage pour les coords des rectangles
	while i<len(hauteur):  #nombre d'éléments dans "hauteur", c-à-d aussi le nombre de rectangles
		m=un_rectange(hauteur[i],largeur[i],hauteur_fenetre,d)
		d+=largeur[i]  #le décalage auquel on ajoute la largeur du rectangle précédent pour avoir la coordonnée en x du suivant
		lst_totale.append(m)
		i+=1
	return lst_totale

def dessiner_ville(rectangles):
	immeuble=0   # "immeuble" est l'indice pour la liste des coordonnées des rectangles
	while immeuble<len(rectangles):
		if immeuble%2==0:  #alterne les couleurs des rectangles
			rectangle(rectangles[immeuble][0],rectangles[immeuble][1],rectangles[immeuble][2],rectangles[immeuble][3],remplissage="black")
		else:
			rectangle(rectangles[immeuble][0],rectangles[immeuble][1],rectangles[immeuble][2],rectangles[immeuble][3],remplissage="blue")
		immeuble+=1

def calcule_largeur_fenetre(largeur):
	compteur=0
	s=0
	while compteur<len(largeur):
		s+=largeur[compteur]   #additionne les largeurs des rectangles pour calculer la largeur de la fenêtre
		compteur+=1
	return s



# Les fonctions pour les fenêtres :

#fonction pour les coordonnées x (en abscisse) et en horizontal d'un rectangle
def liste_fenetres_horizontale(coords,espace,large):
	lst_horizon=[]
	x0=coords[0]
	while x0<coords[2]-(espace+large):
		x0+=espace
		x1=x0+large
		lst_horizon.append([x0,x1])    #x0 correspond au "ax", et x1 au "bx" (d'après la documentation upemtk)
		x0=x1    #ici je passe aux coordonnées de la fenêtre suivante
	return lst_horizon

#fonction pour les coordonnées y (en ordonnée) et en vertical d'un rectangle
def liste_fenetres_verticale(coords,espace,large):
	lst_verticale=[]
	y0=coords[1]
	while y0<coords[3]-(espace+large):
		y0+=espace
		y1=y0+large
		lst_verticale.append([y0,y1])     #y0 correspond au "ay", et y1 au "by" (d'après la documentation upemtk)
		y0=y1    #ici je passe aux coordonnées de la fenêtre suivante
	return lst_verticale

#fonction qui regroupe les coordonnées horizontales et verticales pour un rectangle
def liste_fenetres_fin(coords,espace,large):
	lst_fin=[]
	x1=liste_fenetres_horizontale(coords,espace,large)
	y1=liste_fenetres_verticale(coords,espace,large)
	cpt=0
	while cpt<len(y1):   #tant que les coords fenêtres verticales
		cpt2=0
		while cpt2<len(x1):  #tant que les coords fenêtres horizontales
			temp=[x1[cpt2][0],y1[cpt][0],x1[cpt2][1],y1[cpt][1]]  #variable temporaire qui prend une liste des coordonnées des fenêtres
			lst_fin.append(temp)
			cpt2+=1
		cpt+=1
	return lst_fin

#fonction qui créée les coords des fenêtres de tous les rectangles
def liste_fenetres(lst_coords,espace,large):
	lst_fin=[]
	cpt=0
	while cpt<len(lst_coords):  #liste des coords des rectangles
		i=liste_fenetres_fin(lst_coords[cpt],espace,large)
		cpt2=0
		while cpt2<len(i):   #pour chaque rectangle je lui associe les coords des fenêtres
			lst=[i[cpt2][0],i[cpt2][1],i[cpt2][2],i[cpt2][3]]
			lst_fin.append(lst)
			cpt2+=1
		cpt+=1
	return lst_fin

#cette fonction dessine les fenêtres et ajoute l'option d'allumer et d'éteindre les fenêtres
def allumer_eteindre_fenetres(fenetre):
	while True:   #cette boucle while permet de pouvoir allumer et éteindre les fenêtres en continu, et de ne pas arrêter le programme pour allumer et éteindre
		immeuble=0
		if attente_clic():
			while immeuble<len(fenetre):   #ici, je dessine les fenêtres
				rectangle(fenetre[immeuble][0],fenetre[immeuble][1],fenetre[immeuble][2],fenetre[immeuble][3],remplissage="yellow",tag="fenetres")
				immeuble+=1
			if attente_clic():   #si il y a un clic, les fenêtre s'éteignent
				efface("fenetres")


# Le programme :

hauteur_fenetre = 400
nb_rectangles = 15
hauteur = liste_aleatoire(nb_rectangles,0,hauteur_fenetre)
largeur = liste_aleatoire(nb_rectangles,30,50)
largeur_fenetre = calcule_largeur_fenetre(largeur)

cree_fenetre(largeur_fenetre,hauteur_fenetre)


rectangles=coordonnees_rectangles(hauteur,largeur,hauteur_fenetre)
dessiner_ville(rectangles)

fen=liste_fenetres(rectangles,5,8)
allumer_eteindre_fenetres(fen)

attente_clic()
ferme_fenetre()
