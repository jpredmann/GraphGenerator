import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import operator
import pickle

class GraphGenerator(object):
	"""
	Generate optimized graphs given a relation defined by an array of floating point values.
	The generator produces a graph of as few components as possible with the edges minimized
	according to some specified comparison and set of constraints.
	"""

	def __init__(self):
		"""
		Initialize the GraphGenerator
		input: object to process input array for use in constructing the graph object
		constructor: object to convert processed input array into NetworkX graph object
		optimizer: object to optimize the graph object
		combiner: object to consolidate components of the final graph
		output: object to process final graph for output in different formats
		"""
		self.graph = nx.Graph(state="empty")

		self.input = Input()
		self.constructor = Constructor(self.graph)
		self.optimizer = Optimizer(self.graph)
		#self.combiner = Combiner(self.graph)
		self.output = Output(self.graph)
		#self.comparator = None
		


	# End def __init__


	def generateGraph(self, edgeWeightArray, weightLimit):
		"""
		Generate an optimized graph
		"""
		#self.comparator = comparator
		weightedAdjacencyMatrix = self.input.processInput(edgeWeightArray)
		self.constructor.constructGraph(weightedAdjacencyMatrix, weightLimit)
		self.optimizer.optimizeComponents()
		#self.output
		#self.finalGraph = self.combiner.combineComponents(optimizedGraph)

	# Ende def generateGraph

	def registerConstraints(self, *constraintsList):
		"""
		Constraint objects for optimization are registered with the optimizer object
		"""
		for constraint in constraintsList:
			print "I am here"
			constraint.graph = self.graph
			self.optimizer.addConstraint(constraint)



	def outputGraph(self, outputOption, fileName):
		"""
		Output the optimized graph in the specified format
		"""

		# TODO: make the magic numbers defined constants
		if outputOption == 1:
			self.output.dotFile(fileName)

		elif outputOption == 2:
			self.output.pickleFile(fileName)

		elif outputOption == 3:
			self.output.imageFile(fileName)

		else:
			print "Error"
			# raise an exception

	# End def outputGraph


	def getGraphObject(self):
		"""
		Returns the final NetworkX graph object
		"""

		return self.output.getNXObject()

	# End def getGraphObject


# End Class GraphGenerator



class Input(object):
	"""
	Processes the input for the GraphGenerator.
	"""

	def __init__(self):
		"""
		Initialize the Input object
		"""

	# End def __init__

	def processInput(self, edgeWeightsArray):
		"""
		Takes an array argument and processes it for use in genrating a graph object.
		"""

		# Use numpy's upper triangle function with k=1 to make diagonal and below zeros
		return np.triu(edgeWeightsArray, k=1)

# End Class Input



class Constructor(object):
	"""
	Constructs and initial graph from the input supplied by the Input object.
	"""

	def __init__(self, graph):
		"""
		Initialize the Constructor object
		"""
		self.graph = graph

	# End def __init__

	# TO DO: make weight comparison abstract to handle either > or <
	def constructGraph(self, weightedAdjacencyMatrix, weightLimit):
		"""
		Build a NetworkX graph object from a weighted adjacency matrix
		"""

		numberVertices = weightedAdjacencyMatrix.shape[0]
		self.graph.add_nodes_from( range(numberVertices) )

		for i in xrange(numberVertices):
			for j in xrange(numberVertices):

				if weightedAdjacencyMatrix[i][j] > weightLimit:
					self.graph.add_edge( i, j, weight=weightedAdjacencyMatrix[i][j] )

		self.graph.graph['state'] = "constructed(initial)"


	# End def constructGraph

# End Class Constructor



class Optimizer(object):
	"""
	Optimizes the initial graph by successive component-wise optimization of the initial
	graph created by the Constructor object.
	"""

	def __init__(self, graph):
		"""
		Initialize the Optimizer object
		"""
		self.constraintsList = []
		self.graph = graph

	# End def __init__


	def addConstraint(self, constraint):
		"""
		Registers a constraint to be used in optimization
		"""

		self.constraintsList.append(constraint)


	# End def addConstraint


	def optimizeComponents(self):
		"""
		Optimizes the graph with the registered constraints
		"""
		print "In Optimize Graph"
		print nx.info(self.graph)
		componentsList = nx.connected_component_subgraphs(self.graph)

		for constraint in self.constraintsList:
			constraint.checkPriorViolations()

		for component in componentsList:
			edgeList = component.edges(data=True)
			# TO DO: Need to make this work both in order and reverse
			edgeList.sort( key=operator.itemgetter(2) )

			for edge in edgeList:
				self.graph.remove_edge(edge[0], edge[1])

				for constraint in self.constraintsList:

					if constraint.checkConstraint():
						self.graph.add_edge(edge[0], edge[1], weight=edge[2])







	# End def optimizeGraph

# End Class Optimizer



class Combiner(object):
	"""
	Attempts to insert edges where needed and possible to the optmized graph from the Optimizer
	object to reduce the number of components in the final graph.
	"""

	def __init__(self, graph):
		"""
		Initialize the Combiner object
		"""

		self.graph = graph

	# End def __init__

# End Class Combiner



class Output(object):
	"""
	Formats the final graph from the Combiner object for output in any of several formats.
	Desired Formats:
		1. DOT File
		2. Pickled NetworkX Graph object
		3. Image file format (PNG, JPEG)
	Future:
		1. GML
		2. GraphML
	"""

	def __init__(self, graph):
		"""
		Initialize the Output object
		"""
		self.graph = graph

	# End def __init__


	def dotFile(self, fileName):
		"""
		Generate a DOT file of the final graph
		"""

		nx.write_dot(self.graph, fileName)

	# End def dotFile


	def pickleFile(self, fileName):
		"""
		Generate a pickleFile of the final graph
		"""

		nx.write_pickle(self.graph, fileName)

	# End def pickleFile


	def imageFile(self, fileName):
		"""
		Generate an image file in the specified type of the final graph
		"""

		nx.draw_networkx(self.graph)
		plt.savefig(fileName + ".png")

	# End def imageFile

	def getNXObject(self):
		"""
		Returns a NetworkX graph Object of the final graph
		"""
		return self.graph

	# End def getNXObject


# End Class Output

