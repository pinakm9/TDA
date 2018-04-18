import sys
from paths import *
sys.path.append(p2_gudhi)
import gudhi
import process
from utility import *

@timer
def plot_persistence(data, max_edge_length=25.0):
	rips_complex = gudhi.RipsComplex(points=data, max_edge_length = max_edge_length)
	simplex_tree = rips_complex.create_simplex_tree(max_dimension = 15)
	print('Dimension of Rips complex: {}\nNumber of vertices: {}\nNumber of simplices: {}'.\
		format(simplex_tree.dimension(), simplex_tree.num_vertices(), simplex_tree.num_simplices()))
	#for filtered_value in simplex_tree.get_filtration():
	    #print(tuple(filtered_value))
	diag = simplex_tree.persistence(homology_coeff_field = 2, min_persistence=0)
	#print('diag = {}'.format(diag))
	pplot = gudhi.plot_persistence_diagram(diag)
	pplot.show()

data = process.collect_data_(p2_sample)
print type(data)
print data
plot_persistence(data)