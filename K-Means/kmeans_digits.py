from kmeans import *

# Fichier dédié à l'analyse de la base de donnée "optdigits".


#-------- Partie K-means ----------#

def get_classification(data, centers, v=True):
	'''Compte le nombre de fois où un point se retrouve dans chaque classe,
	pour tout les points dans data qui correspondent au chiffre p'''
	k = centers.shape[0]

	# Counts va compter le nombre d'occurence de chaque label rencontré,
	# pour chaque centre. counts(i, j) = nombre de point associés au 
	# centre i qui ont le label j.
	counts = np.zeros((k,10))
	for point in data:
		p = int(point[-1])
		counts[minimize_distance(centers, point[:-1]), p] += 1

	# classifiction associe chaque centre à un chiffre. On utilise counts,
	# et on choisit le centre i, le j qui maximise counts[i,j]
	classification = np.empty(k, dtype=int)
	for i in range(k):
		digit = np.argmax(counts[i,:])
		classification[i] = digit

	# Option verbose pour afficher plus d'information. Actif par défault.
	if v:
		print(classification)
		print(counts)

	return(classification)


def learn(n, k):
	'''lance l'algo des k-means sur les données d'apprentissage, n fois'''

	# On retire la dernière colone (les labels), car on ne veut lancer
	# l'algo que sur les données graphiques.
	data = load_data("optdigits.tra")[:,:-1]

	centers, partition = k_means_best(data, k, n)

	save_data("digits.result", centers)

def learn_global(k):
	data = load_data("optdigits.tra")[:,:-1]
	centers, partition = global_init(data, k, v=True)
	centers, partition = k_means(data, centers, partition)

	save_data("digits.result", centers)


#-------- Partie affichage -----#

def show_image(im):
	'''affiche une des images, im étant un point des données.'''
	im = np.reshape(im[:64], (8, 8))
	plt.imshow(im, cmap='Greys')
	plt.show()

def show_centers(centers, classification):

	fig=plt.figure(figsize=(8, 8))
	rows = 5
	columns = 4
	i = 1
	for number in range(10):
		for j in range(len(centers)):
			if classification[j] == number:
				fig.add_subplot(rows, columns, i)
				plt.imshow(np.reshape(centers[j], (8,8)), cmap='Greys')
				plt.axis('off')
				i += 1

	plt.show()


#--------- Partie test ---------#

def test(filename='digits.result', v=True, graph=True):
	'''Affiche  les taux de bonne réponse pour chaque chiffre, ainsi que le
	chiffre prédit en fonction du chiffre réel (sous forme d'une matrice)
	Utilise les postions des centres (pré-calculés par la fonction learn)
	enregistrées dans digits.result
	Renvoie le taux de bonne réponse global.'''

	# On charge les données du dataset d'apprentissage, et les centre
	# obtenus par k-means, pour obtenir la classification.
	data = load_data("optdigits.tra")
	centers = load_data(filename)
	classification = get_classification(data, centers, v=v)

	# On charge les donées test
	data_test = load_data("optdigits.tes")

	# Cette matrice accuracy donne le taux de chiffre prédit en fonction
	# du chiffre réel (i=chiffre réel j=chiffre prédit)
	accuracy = np.zeros((10,10), dtype=int)
	for point in data_test:
		predicted = classification[minimize_distance(centers, point[:-1])]
		accuracy[int(point[-1]), predicted] += 1

	# Verbose : affiche plus d'informations
	if v:
		print(accuracy)
		for i in range(10):
			rate = accuracy[i,i]/np.sum(accuracy[i,:])
			print(f'{i} : {rate:.2f}')

		diag = 0
		for i in range(10):
			diag += accuracy[i,i]

		global_rate = diag/np.sum(accuracy)
		print(f'Total : {global_rate}')

	# Option pour afficher graphiquement la matrice accuracy.
	if graph:
		plt.matshow(accuracy)
		plt.show()
		show_centers(centers, classification)


	# Retourne le taux de bonne réponse global.
	return global_rate


def influence_of_k(n):
	test_values = np.array([10, 11, 12, 13, 14, 15, 20, 25, 30, 40, 50, 70, 100, 200])
	scores = np.zeros(test_values.shape)
	for i in range(test_values.shape[0]):
		k = test_values[i]
		learn(n, test_values[i])
		scores[i] = test(graph=False)
	plt.plot(test_values, scores)
	plt.show()



if __name__ == "__main__":
	# Some code you wanna run
	#learn(100, 20)
	test()

