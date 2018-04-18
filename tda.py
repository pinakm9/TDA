import sys
from paths import *
sys.path.append(p2_gudhi)
import gudhi
import process
from utility import *
import numpy as np

@timer
def diagram2array(diag):
	arr = []
	for elem in diag:
		hom, life = elem
		birth, death = life
		arr.append([hom, birth, death])
	return np.array(arr)

def fname(cols, prefix = 0, max_edge_length = 10, max_dimension = 15):
	cols.sort()
	index = ''
	for i in cols:
		index = index + str(i)
	if prefix == 0:
		prefix = p2_plots + 'pplot'
		suffix = '.png'
	elif prefix == 1:
		prefix = p2_pers + 'pers'
		suffix = '.txt'
	return prefix + '_mel{:.1f}_md{}_{}'.format(max_edge_length, max_dimension, index) + suffix

@timer
def purge(diag):
	arr = []
	for elem in diag:
		if float('inf') not in elem:
			arr.append(elem[1:])
	return np.array(arr)

@timer
def plot_persistence(data, cols, max_edge_length = 5, max_dimension = 5, save = False):
	rips_complex = gudhi.RipsComplex(points=data, max_edge_length = max_edge_length)
	simplex_tree = rips_complex.create_simplex_tree(max_dimension = max_dimension)
	print('Dimension of Rips complex: {}\nNumber of vertices: {}\nNumber of simplices: {}'.\
		format(simplex_tree.dimension(), simplex_tree.num_vertices(), simplex_tree.num_simplices()))
	#for filtered_value in simplex_tree.get_filtration():
	    #print(tuple(filtered_value))
	diag = simplex_tree.persistence(homology_coeff_field = 2, min_persistence=0)
	#print('diag = {}'.format(diag))
	pplot = gudhi.plot_persistence_diagram(diag)
	pplot.savefig(fname(cols, 0, max_edge_length, max_dimension))
	pplot.show()
	diag = diagram2array(diag)
	np.savetxt(fname(cols, 1, max_edge_length, max_dimension), diag)
	print diag
	return diag

@timer
def bdist(A, B):
	d = []
	for a in A:
		ad = []
		for b in B:
			ad.append(np.linalg.norm(a-b))
		d.append(max(ad))
	return min(d)

@timer
def bottleneck(cols1, mel1, md1, cols2, mel2, md2):
	diag1 = purge(np.loadtxt(fname(cols1, 1, mel1, md1)))
	diag2 = purge(np.loadtxt(fname(cols2, 1, mel2, md2)))
	dist =  bdist(diag1, diag2)
	print('Bottleneck distance between pplots withs {} and {}: {}'\
		.format(cols1, cols2, dist))
	return dist

#data, cols = process.collect_data_(p2_sample, cols = [0,1,2,4,5,6,7,8,9,10])
#plot_persistence(data, cols, max_edge_length = 25, max_dimension = 25, save = True)
"""diag = [(2, (24.0805852276289, float('inf'))), (2, (24.828829125546616, float('inf'))),\
 (2, (24.1713368659666, float('inf'))), (2, (19.58621054486118, 21.96714222838945)),]
diagram2array(diag)"""
bottleneck([0,1,2,3,4,5,6,7,8,9,10], 25, 25,  [0,1,2,4,5,6,7,8,9,10], 25, 25)