import numpy as np
import matplotlib.pyplot as plt

from copy import deepcopy
from warnings import warn

#	Variables qui reviennent souvent dans les fonctions :
# - (numpy array (n,d)) data : les données à analyser.
#
# - (numpy array (k,d)) centers : contient les coordonées des centres
#	 (soit pendant leur calcul, soit une fois calculés)

# - (numpy array (n)) partition : contient les index du centre qui
#	 est le plus proche pour chaque point de data.
#
#	Avec n le nombre de points, d la dimension des données.

#------------- File Handling -------------#
# Foncions pour le chargement et la sauvegarde

def load_data(filename, delimiter=',', dtype=float):
	'''Charge les données depuis un fichier csv (par défaut)'''
	return np.genfromtxt(filename, delimiter=delimiter, dtype=dtype)

def save_data(filename, data, delimiter=','):
	'''sauvegarde dans un fichier csv (par défaut) des données'''
	np.savetxt(filename, data, delimiter=delimiter)


#------------ Pre-processing -------------#
# Fonctions pour un pré-traitement des données (non utilisé)

def normalize(data):
	'''renvoie les données normalisée, c'est à dire que les valeurs
	sont transformée linéairement pour toutes être entre 0 et 1'''

	for i in range(data.shape[1]):
		m, M = np.min(data[:,i]), np.max(data[:,i])
		data[:,i] -= m
		data[:,i] /= (M-m)
	return data



#---------------- Init -------------------#
# Fonction pour l'initialisation des centres (première étape de k-means)
# + Global K-Means

def random_centers_init(data, k):
	'''Initialise les centres en prenant simplement k points au hasard parmis les données'''

	index = np.random.choice(data.shape[0], k, replace=False)  
	return data[index]

def partition_init(data):
	'''renvoie une liste vide avec le nombre de points comme taille
	Entiers qui correspondent à quel centre est le plus proche de
	ce point.'''

	return np.zeros(data.shape[0], dtype=int)


def global_init(data, k, v=False):
	'''Implémentation de la méthode d'initialisation de Global K-Means'''

	n, d = data.shape

	# Liste qui va contenir les centres
	centers = np.empty((k, d))

	# Premier centre, qui est simplement le barycentre des données
	centers[0] = np.sum(data, axis=0)/n
	
	# On va attribuer les autres centres de manière récursive.
	for i in range(1, k):

		# Option verbose
		if v:
			print(f'global_init : {i}')

		# Deux variable pour garder une trace du meilleur point
		best_v = np.inf
		best_x = None

		partition = partition_init(data)

		for x in data:

			# On considère successivement chaque point comme un centre
			# et on prend celui qui minimise la variance intra-classe.
			centers[i] = x
			update_partition(data, centers[:i+1], partition)
			v = intra_variance(data, centers[:i+1], partition)

			if v < best_v:
				best_v = v
				best_x = x

		# On garde le meilleur centre avant de passer au suivant
		centers[i] = best_x

	return centers, partition
	# Le contenu de la liste partition importe peu, mais on la garde
	# pour éviter d'avoir à en faire une autre avant de lancer k-means.



#-------------- Computations -------------#
# Les calculs nécéssaire pour l'algorithme k-means, et pour

def minimize_distance(centers, point):
	'''Renvoie l'index (parmis la liste centers) du centre qui minimize la
	distance à point'''

	distance = np.sum((centers-point)**2, axis=1)
	return np.argmin(distance)

def intra_variance(data, centers, partition):
	'''Renvoie la somme des carrés des distance entre chaque point et son centre
	le plus proche. Utilisé pour comparer les performances de differents choix
	de centres. C'est la variance intra-classe'''

	variance = 0
	for i in range(centers.shape[0]):
		variance += np.sum((centers[i]-data[tuple([partition==i])])**2)
	return variance

def update_partition(data, centers, partition):
	'''En utilisant minimize_distance, renvoie une liste d'index, qui indique
	quel centre est plus proche de chaque point'''

	for i in range(data.shape[0]):
		partition[i] = minimize_distance(centers, data[i])

def update_centers(data, centers, partition):
	'''Re-calcul les centres en fonction de partition (simplement en
	prenant le barycentre des nuages de points formés par partition)'''

	k = centers.shape[0]
	for i in range(k):
		centers[i] = np.mean(data[tuple([partition==i])], axis=0)



#----------- The actual algorithm ----------#

def k_means(data, centers = np.empty(0), partition = np.empty(0), k = None):
	'''implémentation de la méthode des k-moyennes, en utiliant
	pour l'instant une initialisation purement aléatoire'''

	#Initialisation aléatoire si centers et partition ne sont pas donnés
	if partition.size == 0:
		partition = partition_init(data)
	if centers.size == 0:
		if not k:
			raise Exception('Missing argument : either k or centers need be given')
		centers = random_centers_init(data, k)


	# L'algo, on recommence jusqu'à rencontrer la condition d'arrêt
	while True:

		previous_centers = deepcopy(centers)

		# Mises à jour successives
		update_partition(data, centers, partition)
		update_centers(data, centers, partition)

		#  Cette condition survient dans certain cas, lorsqu'un des centre
		# se retrouve sans point, car tous sont plus proches d'un autre
		# centre ! Semble arriver surtout quand les nuages de points sont
		# très concentrés. Un avertissement est affiché dans ce cas.
		if np.isnan(np.sum(centers)):
			warn("Center has no associated point !")
			break

		# Quitte quand on est stabilisé
		if np.all(previous_centers == centers):
			break


	
	return centers, partition

def k_means_best(data, k, n):
	'''Lance k_means n fois, et selectionne le meilleure (celui qui
	minimise la variance intra-classe)'''

	best_v = np.inf
	for _useless in range(n):
		centers, partition = k_means(data, k=k)
		v = intra_variance(data, centers, partition)
		if v < best_v:
			best_v = v
			best_centers = centers
			best_partition = partition

	return best_centers, best_partition



#-------------- Graphics ---------------#
# Pour l'affichage de données, avec matplotlib


def graph_2D(data, centers=None, partition=None, size=5):
	'''Utile pour visualiser des données en 2 dimensions'''

	plt.scatter(data[:,0], data[:,1], c=partition, s=size)
	if centers is not None:
		plt.scatter(centers[:,0], centers[:,1], marker='P', c = range(centers.shape[0]), s=100)
	plt.show()



#----------- Davies-Bouldin -----------#
# Fonctions pour calculer l'indice de Davies-Bouldin, qui sert à
# aider le choix du nombre k.

def sigma(data, centers, partition, i):
	'''Renvoie la variance de la classe i'''
	return np.sqrt(np.sum((centers[i]-data[tuple([partition==i])])**2))/np.sum([partition==i])


def db(data, centers, partition):
	'''Calcul I_DB pour k'''

	k = centers.shape[0]
	sig = [sigma(data, centers, partition, i) for i in range(k)]
	total = 0
	for i in range(k):
		total += max([(sig[i]+sig[j])/np.sqrt(np.sum((centers[i]-centers[j])**2)) for j in range(k) if j!=i])
	return total/k


def davies_bouldin(data, n = 100, max_k = 8, v=False):
	'''Lance k_means_best n fois, avec k allant de 2 jusqu'à max_k.
	pour chauqe k, calcul I_DB associé ainsi que la variance intra-classe
	et affiche un graphe du tout'''
	K = np.arange(2, max_k+1)
	score_db = np.empty(max_k-1)
	score_v = np.empty(max_k-1)
	for k in K:
		if v:
			print(k)
		centers, partition = k_means_best(data, k, n)
		score_db[k-2] = db(data, centers, partition)
		score_v[k-2] = intra_variance(data, centers, partition)

	score_v *= np.max(score_db)/np.max(score_v)

	plt.plot(K, score_db)
	plt.plot(K, score_v)
	plt.xlabel("K : nombre de groupes")
	plt.ylabel("DB")
	plt.show()
		




#---------- Testing ----------#
# Fonctions pour les tests

def random_dataset(centers, n, v):
	'''créer des données aléatoire.
	Créer n points autour de chaque centre, selon une loi normale
	de variance v
	Les centres ne sont PAS conservées dans les données générées'''

	# La dimensions des points doit être la même que celle des centres
	d = centers.shape[1]
	data = []
	for center in centers:
		# On créer un nuage de point par centre donné.
		data.append(np.random.randn(n, d)*v + center)

	# On renvois la concatenation des nuages de points.
	return np.concatenate(data, axis = 0)


#----- Code à exécuter -----#


if __name__ == '__main__':
	import example_data
	data = example_data.diffuse_4()
	centers, partition = global_init(data, 4)
	
	centers, partition = k_means(data, centers, partition)

	graph_2D(data, centers, partition)
	



