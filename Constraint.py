import networkx as nx

# I added a comment


class Constraint(object):
	"""
	Abstract Base Class for constraint objects
	"""

	def __init__(self):
		"""
		Constructor
		"""

		self.graph = None
		self.violatorsSet = None

	# End __init__


	def constraintDataCheck(self):
		"""
		Iterates over vertices and/or edges checking for the required data.
		If the required data is not present, it throws an exception
		"""
		# TO DO: Determine if and how data checking would be required
		pass
		#raise NotImplementedError("constraintDataCheck should have been implmented")

	# End def constraintDataCheck


	def checkViolations(self):
		"""
		Check for specific violations of the constraint
		"""

		raise NotImplementedError("checkViolations should have been implmented")

	# End def checkViolations


	def checkPriorViolations(self):
		"""
		Checks for violations of the constraint that are inherent to the data
		(i.e. are there before any optimization is performed).  If there are any
		then add them to a list to be ignored later.
		"""
		self.violatorsSet = self.checkViolations()

	# End def checkPriorViolations


	def checkConstraint(self):
		"""
		Trivariate valued logic function returns
			True if constraint is violated
			False if constraint is not violated 
			None if constraint is not violated and there were no pre-exisiting violation
		"""
		raise NotImplementedError("checkConstraint should have been implmented")

	# End def checkConstraint


class cycleConstraint(Constraint):
	"""
	Constraint ensures that all vertices are in a cycle
	"""

	def __init__(self):

		# Store a reference to the graph for constaint chcking
		self.graph = None
		# A set of vertices that violate the cycle constraint 
		# prior to any optimization
		self.violatorsSet = None

	# End def __init__


	def constraintDataCheck(self):
		"""
		There is no data that is needed for general cycle checking
		"""
		pass

	# End def constraintCheck


	def checkViolations(self):
		"""
		Finds all vertices that are not in cycles
		"""

		# Get the set of vertices in the graph
		vertexSet = set( self.graph.nodes() )
		# Get the list of basis cycles
		cycleBasis = nx.cycle_basis( self.graph )
		# Convert the list of basis cycles into a set of vertices in the cycles
		cycleVertexSet = set( [vertex for sublist in cycleBasis for vertex in sublist] )
		# Get the difference between the set of vertices in the graph and those in cycles
		nonCycleVertexSet = vertexSet.difference(cycleVertexSet)

		return nonCycleVertexSet

	def checkPriorViolations(self):
		"""
		Determine if any vertices are not in cycles from the initial graph.
		If there are any, add them to a list of vertices to ignore when checking
		constraint violation.
		"""

		# Initialize the list of violations of the constraint that exist
		# prior to any optimization
		self.violatorsSet = self.checkViolations()

	# End def checkPriorViolations


	def checkConstraint(self):
		"""
		Check to see if any vertices that were in cycles are no longer in cycles.
		"""

		# Default return true that a constraint was violated
		constraintViolated = True

		# Check for current violations of the constraint
		violationsSet = self.checkViolations()
		print "ViolationsSet: ", violationsSet
		# Get the difference between current and prior violations,
		# if the difference is the empty set, then no new violations
		newViolationsSet = violationsSet.difference(self.violatorsSet)

		# Return None if there are no prior and no new violations of the constraint
		if not newViolationsSet and not self.violatorsSet: constraintViolated = None
		# Return False if there are prior violations but no new violations
		elif not newViolationsSet: constraintViolated = False

		return constraintViolated

	# End def checkConstraint



class connectedConstraint(object):
	"""
	Abstract Base Class for constraint objects
	"""

	def __init__(self):
		"""
		Constructor
		"""

		self.graph = None
		self.violatorsSet = None

	# End __init__


	def constraintDataCheck(self):
		"""
		Iterates over vertices and/or edges checking for the required data.
		If the required data is not present, it throws an exception
		"""
		# TO DO: Determine if and how data checking would be required
		pass
		#raise NotImplementedError("constraintDataCheck should have been implmented")

	# End def constraintDataCheck


	def checkViolations(self):
		"""
		"""


	# End def checkViolations


	def checkPriorViolations(self):
		"""
		Checks for violations of the constraint that are inherent to the data
		(i.e. are there before any optimization is performed).  If there are any
		then add them to a list to be ignored later.
		"""
		self.violatorsSet = self.checkViolations()

	# End def checkPriorViolations


	def checkConstraint(self):
		"""
		Trivariate valued logic function returns
			True if constraint is violated
			False if constraint is not violated 
			None if constraint is not violated and there were no pre-exisiting violation
		"""
		raise NotImplementedError("checkConstraint should have been implmented")

	# End def checkConstraint
