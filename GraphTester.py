import numpy as np
import networkx as nx
import GraphGenerator as gg
import Constraint

class GraphTester():

	def __init__(self):
		"""
		Initilaize a tester object for the graph generator software
		"""

		self.testArray = None

	# End def __init__


	def generateInputArray(self, rows, columns):
		"""
		Generate an array of random values between 0.00 and 1.00
		"""

		testArray = np.random.random_sample( (rows,columns) )

		self.testArray = testArray

	# End def generateInputArray


	def generateInputArrayFromFile(self, fileName):
		"""
		Generates an array of values between 0.00 and 1.00 from an input file
		"""


	def runTest(self):
		"""
		Use the randomly generated array to test the graph generator
		"""
		cycleConstraint = Constraint.cycleConstraint()
		generator = gg.GraphGenerator()
		generator.registerConstraints(cycleConstraint)
		generator.generateGraph(self.testArray, 0.1)
		generator.outputGraph(3, "testGraph")
		graph = generator.getGraphObject()
		print nx.info(graph)



	# End def runTest


def main():
	"""
	Test the graph generator
	"""

	tester = GraphTester()

	tester.generateInputArray(10,10)

	tester.runTest()


main()

