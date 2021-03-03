from kmeans import *
import matplotlib.pyplot as plt

# Fichier dédié à l'analyse de la base de donnée "IRIS".


def accuracy(partition, k = 3):
	'''Prend la partition faite par l'algorithme et compare avec les labels.
	Renvoit une matrice A avec A_ij = nombre de fleurs dont le label est i
	étant catégorisée en j'''

	# On charge les labels qui sont dans la dernière colone
	labels = load_data('iris.data', dtype=int)[:,4]
	counts = np.zeros((3, k), dtype=int)

	for predicted, label in zip(partition, labels):
		counts[label-1, predicted-1] += 1

	# Pour remettre les colones dans le bon ordre, on considère que l' argmax
	# d'une ligne est la catégorie prédite.
	order = np.argmax(counts, axis = 1)
	counts = counts[:, order]

	diag = 0
	for i in range(3):
		diag += counts[i,i]

	global_rate = diag/np.sum(counts)

	return counts, global_rate

def show_graphs(data, centers, partition):
	'''Affiche deux graphes côte à côte :
	- à gauche les deux premier attributs : largeur des sépales en fonction
	  de leur longueur.
	- à droite les deux derniers attributs : largeur des pétales en fonction
	  de leur longueur.'''

	fig = plt.figure()

	# Premier graphe
	fig.add_subplot(121)
	plt.scatter(data[:,0], data[:,1], c=partition, s=3)
	if centers.size > 0:
		plt.scatter(centers[:,0], centers[:,1], marker='P', c = range(centers.shape[0]), s=100)
	plt.xlabel('sepal length')
	plt.ylabel('sepal width')

	# Deuxième graphe
	fig.add_subplot(122)
	plt.scatter(data[:,2], data[:,3], c=partition, s=3)
	if centers.size > 0:
		plt.scatter(centers[:,2], centers[:,3], marker='P', c = range(centers.shape[0]), s=100)
	plt.xlabel('petal length')
	plt.ylabel('petal width')

	# Affiche le tout
	plt.show()

def plot_real_classification():
	'''affiche la classification réelles des fleurs'''
	data = load_data('iris.data')[:,:4]
	labels = load_data('iris.data', dtype=int)[:,4]
	centers = np.empty(0)

	show_graphs(data, centers, labels)



def test_global(k = 3):
	'''test avec initialisation par global kmeans'''
	data = load_data('iris.data')[:, :4]

	centers, partition = global_init(data, k)
	centers, partition = k_means(data, centers, partition)

	show_graphs(data, centers, partition)
	print(accuracy(partition))

def test_random(k = 3):
	'''test avec initialisation aléatoire'''
	data = load_data('iris.data')[:, :4]

	centers, partition = k_means_best(data, 2, 1)
	accuracy(partition)

	print(accuracy(partition))
	show_graphs(data, centers, partition)


def test_db(k = 3):
	'''test de l'indice davies-bouldin'''
	data = load_data('iris.data')[:, :4]
	davies_bouldin(data, 20, 15, v=True)


if __name__ == '__main__':
	test_random()
