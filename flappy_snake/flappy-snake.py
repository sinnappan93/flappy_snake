from upemtk import *
from random import randint
from time import *

###

# les fonctions de l'exercice 1 :
# Commentaires des fonctions des rectangles dans "ville.py"

def liste_aleatoire(nb,mini,maxi):
	lst=[]
	compteur=0
	while compteur<nb:
		aleatoire=randint(mini,maxi)
		lst.append(aleatoire)
		compteur+=1
	return lst


def un_rectange(h,l,hauteur_fenetre,d):
	return [d,hauteur_fenetre-h,d+l,hauteur_fenetre]

def coordonnees_rectangles(hauteur,largeur,hauteur_fenetre,position):
	lst_totale=[]
	i=0
	d=0
	#coords pour les rectangles du bas
	if position=="Down":
		while i<len(hauteur):
			m=un_rectange(hauteur[i],largeur[i],hauteur_fenetre,d)
			d+=largeur[i]
			lst_totale.append(m)
			i+=1
	#coords pour les rectangles du haut
	if position=="Up":
		while i<len(hauteur):
			m=un_rectange(hauteur[i],largeur[i],hauteur[i],d)
			d+=largeur[i]
			lst_totale.append(m)
			i+=1
	return lst_totale


def dessiner_ville(rectangles):
	immeuble=0
	while immeuble<len(rectangles):
		if immeuble%2==0:
			rectangle(rectangles[immeuble][0],rectangles[immeuble][1],rectangles[immeuble][2],rectangles[immeuble][3],remplissage="black")
		else:
			rectangle(rectangles[immeuble][0],rectangles[immeuble][1],rectangles[immeuble][2],rectangles[immeuble][3],remplissage="blue")
		immeuble+=1

def calcule_largeur_fenetre(largeur):
	compteur=0
	s=0
	while compteur<len(largeur):
		s+=largeur[compteur]
		compteur+=1
	return s


###

def hauteurs_complementaires(lst,hauteur_fenetre,difficulte):
	lst_fin=[]
	i=0
	complement=hauteur_fenetre//difficulte
	#je regarde pour le premier rectangle, parce qu'il n'y a pas de précédent
	if i==0:
		actuel=lst[i]
		suivant=lst[i+1]
		
		#je regarde quel rectangle du bas a la plus grande hauteur
		if actuel>suivant:
			haut_max=actuel
		else:
			haut_max=suivant
		a=hauteur_fenetre-haut_max-complement    #je calcule la hauteur du rectangle du haut, avec l'espace à laisser
		lst_fin.append(a)
		i+=1
	while i<len(lst)-1:
		precedent=lst[i-1]
		actuel=lst[i]
		suivant=lst[i+1]
		
		#je regarde quel rectangle du bas a la plus grande hauteur, parmis le précédent, l'actuel et le suivant
		if precedent>actuel and precedent>suivant:
			haut_max=precedent
		elif actuel>precedent and actuel>suivant:
			haut_max=actuel
		elif suivant>precedent and suivant>actuel:
			haut_max=suivant
		a=hauteur_fenetre-haut_max-complement   #je calcule la hauteur du rectangle du haut, avec l'espace à laisser
		lst_fin.append(a)
		i+=1
	
	#je regarde le dernier qui n'a pas de suivant
	if i==len(lst)-1:
		actuel=lst[i]
		precedent=lst[i-1]
		#je regarde quel rectangle du bas a la plus grande hauteur
		if actuel>precedent:
			haut_max=actuel
		else:
			haut_max=precedent
		a=hauteur_fenetre-haut_max-complement
		lst_fin.append(a)
	return lst_fin


def detection_bords(hauteur_bas,hauteur_haut,largeur,hauteur_fenetre):
	lst_bords=[]
	i=0
	while i<len(largeur):
		pix=largeur[i]   #nombre de pixels avant d'atteindre le rectangle suivant
		cpt=0
		while cpt<pix:
			lst_bords.append([hauteur_haut[i],hauteur_fenetre-hauteur_bas[i]])
			cpt+=1
		i+=1
	return lst_bords

###

def dessiner_serpent(x,y,tag):
    cercle(x,y,6,tag=tag)
    cercle(x-1,y-1,1,tag=tag)
    cercle(x+2,y-1,1,tag=tag)
    cercle(x-10,y,4,tag=tag)
    cercle(x-18,y,3,tag=tag)

def deplacer_serpent(x,y,tag):
    efface(tag)
    dessiner_serpent(x,y,tag)
    sleep(0.020) # wait 2.10^-2 second

def touche_ou_pas():
    evenement = donne_evenement()
    type_ev = type_evenement(evenement)
    if type_ev == 'Touche':
        return touche(evenement)
    else: 
        return 'pas_touche'

def mise_a_jour_position(nom_touche,y,gap):
    if nom_touche == 'Up':
        return y-gap
    elif nom_touche == 'Down':
        return y+gap
    else:
        return y

def affiche_texte_centre_et_attend_clic(message, largeur_fenetre, hauteur_fenetre):
    t=texte(largeur_fenetre/2, 
            hauteur_fenetre/2, 
            message, 
            couleur="red", 
            ancrage="center")
    attente_clic()
    efface(t)

def perdu(score,meilleur_score):    
    meilleur_score=max(score,meilleur_score)
    affiche_texte_centre_et_attend_clic("Score: " + str(score) + " (meilleur score: " + str(meilleur_score) + ")",
        largeur_fenetre, 
        hauteur_fenetre)
    return meilleur_score


hauteur_fenetre=400
nb_rectangles=10
hauteurs = liste_aleatoire(nb_rectangles,hauteur_fenetre/5,3*hauteur_fenetre/5)
largeurs = liste_aleatoire(nb_rectangles,40,60)
rectangles1 = coordonnees_rectangles(hauteurs,largeurs,hauteur_fenetre,"Down")

largeur_fenetre=calcule_largeur_fenetre(largeurs)

cree_fenetre(largeur_fenetre,hauteur_fenetre)
dessiner_ville(rectangles1)

hauteurs2 = hauteurs_complementaires(hauteurs,hauteur_fenetre,7)
rectangles2 = coordonnees_rectangles(hauteurs2,largeurs,hauteur_fenetre,"Up")
intervalles = detection_bords(hauteurs,hauteurs2,largeurs,hauteur_fenetre)

dessiner_ville(rectangles2)
meilleur_score = 0
while True:
   
    x_serpent=0
    y_serpent=hauteurs2[0]+(hauteur_fenetre-hauteurs[0]-hauteurs2[0])/2
    vitesse=1
    dx=vitesse
    dy=0

    dessiner_serpent(x_serpent,y_serpent,"serpent")

    cpt = 0
    pas_perdu=True
    while pas_perdu and x_serpent+6<largeur_fenetre:
        x_serpent+=dx
        y_serpent+=0.4  # pour rajouter de la gravité
        deplacer_serpent(x_serpent,y_serpent,"serpent")   
        cpt+=1

        if y_serpent-6<intervalles[cpt][0] or y_serpent+6>intervalles[cpt][1]:
            meilleur_score=perdu(cpt,meilleur_score)
            pas_perdu=False
        else:
            top = touche_ou_pas()
            if top != 'pas_touche':
                y_serpent=mise_a_jour_position(top,y_serpent,6)
            
        mise_a_jour()

    if pas_perdu:
        affiche_texte_centre_et_attend_clic("Gagné, score: " + str(cpt), largeur_fenetre, hauteur_fenetre)
        attente_clic()
        ferme_fenetre()


attente_clic()
ferme_fenetre()
