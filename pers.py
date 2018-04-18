# Do not import this module without taking necessary measures, this module thinks current working directory is p2_gudhi
#import gudhi
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument()
    args = parser.parse_args()
    print args
    """rips_complex = gudhi.RipsComplex(data, max_edge_length = max_edge_length)
	simplex_tree = rips_complex.create_simplex_tree(max_dimension = 11)
	print('Dimension of Rips complex: {}\nNumber of vertices: {}\nNumber of simplices: {}'.\
		format(simplex_tree.dimension(), simplex_tree.num_simplices(), simplex_tree.num_vertices()))
	for filtered_value in simplex_tree.get_filtration():
	    print('{} -> {.4f}'.format(tuple(filtered_value)))
	diag = simplex_tree.persistence(homology_coeff_field = 2, min_persistence=0)
	print('diag = {}'.format(diag))
	pplot = gudhi.plot_persistence_diagram(diag)
	pplot.show()"""