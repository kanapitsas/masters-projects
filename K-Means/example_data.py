from kmeans import random_dataset
from numpy import array
	
def concentrated_6():
	return random_dataset(array([[-2, 1],[-2.5, 1.5], [-1.5, 1.5], [2, 1.5], [1.5, 2], [2.5, 2]]), 15, 0.05)

def diffuse_4():
	return random_dataset(array([[-1, -1], [-1,1], [1,-1], [1, 1]]), 15, 0.3)