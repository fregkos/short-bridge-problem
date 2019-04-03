from threading import Lock, Condition

###SuperClass
class Bridge:
	"""docstring for Bridge."""

	def __init__(self):
		self._nReds = 0
		self._nBlues = 0
		self._totalCollisions = 0

	def arrived(self, car):
		pass

	def isEmpty(self):
		return self._nReds + self._nBlues == 0

	def isSafe(self):
		return self._nReds + self._nBlues < 2

	def collisionDetection(self):
		if not self.isSafe():
			self._totalCollisions += 1

	def insertCar(self, car):
		if car._color == 'Red':
			self._nReds += 1
		elif car._color == 'Blue':
			self._nBlues += 1
		self.collisionDetection()

	def removeCar(self, car):
		if car._color == 'Red':
			self._nReds -= 1
		elif car._color == 'Blue':
			self._nBlues -= 1

	def __repr__(self):
		return '\n\n\t' * 1 + 'Left side' + '\t' * 3 + 'Bridge' + '\t' * 4 + 'Right Side\n' + '=' * 95

###Bridges for each scenario
class UnsafeUnfairBridge(Bridge):
	"""docstring for UnsafeUnfairBridge."""
	def __init__(self):
		super().__init__()

class SafeUnfairBridge(Bridge):
	"""docstring for SafeUnfairBridge."""

	def __init__(self):
		super().__init__()
		self._condition = Condition()

	def insertCar(self, car):
		with self._condition:
			while not self.isEmpty():
				self._condition.wait()

			if car._color == 'Red':
				self._nReds += 1
			elif car._color == 'Blue':
				self._nBlues += 1

			self.collisionDetection()

	def removeCar(self, car):
		with self._condition:
			if car._color == 'Red':
				self._nReds -= 1
			elif car._color == 'Blue':
				self._nBlues -= 1
			self._condition.notifyAll()


class SafeFairStrictBridge(Bridge):
	"""docstring for SafeFairStrictBridge."""

	def __init__(self):
		super().__init__()
		self._nRedArrivals = 0
		self._nBlueArrivals = 0
		self._condition = Condition()
		self._turn = 'Red'

	def arrived(self, car):
		if car._color == 'Red':
			self._nRedArrivals += 1
		elif car._color == 'Blue':
			self._nBlueArrivals += 1

	def loadBalancing(self):
		"""When the load becomes 100%, it means we are using FCFS. Load is relative."""
		totalArrivals = self._nRedArrivals + self._nBlueArrivals
		#Check whether load is at 100% on a side, and give priority, because none is waiting (has arrived) on the other side.
		if self._nRedArrivals / totalArrivals == 1.0:
			print('[!] Left side load: ' + str(round(self._nRedArrivals / totalArrivals * 100, 2)) + '%' + ' and ' + str(self._nRedArrivals) + ' cars are waiting')
			self._turn = 'Red'
		elif self._nBlueArrivals / totalArrivals == 1.0:
			print('\t' * 6 + '[!] Right side load: ' + str(round(self._nBlueArrivals / totalArrivals * 100, 2)) + '%' + ' and ' + str(self._nBlueArrivals) + ' cars are waiting')
			self._turn = 'Blue'

	def insertCar(self, car):
		with self._condition:
			while not self.isEmpty() or self._turn != car._color:
				"""
				We call loadBalancing here to override the strict rule (alternating colors) on the special case of
				the condition lock waiting forever for a car that will never arrive,
				since all of a specific have arrived, but not from the other.
				"""
				self.loadBalancing()
				self._condition.wait()

			if car._color == 'Red':
				self._nReds += 1
				self._turn = 'Blue'
			elif car._color == 'Blue':
				self._turn = 'Red'
				self._nBlues += 1

			self.collisionDetection()

	def removeCar(self, car):
		with self._condition:
			if car._color == 'Red':
				self._nReds -= 1
				self._nRedArrivals -= 1
			elif car._color == 'Blue':
				self._nBlues -= 1
				self._nBlueArrivals -= 1
			self._condition.notifyAll()

class SafeFairAdaptiveBridge(Bridge):
	"""docstring for SafeFairAdaptiveBridge."""

	def __init__(self):
		super().__init__()
		self._nRedArrivals = 0
		self._nBlueArrivals = 0
		self._condition = Condition()
		self._turn = 'Red'

	def arrived(self, car):
		if car._color == 'Red':
			self._nRedArrivals += 1
		elif car._color == 'Blue':
			self._nBlueArrivals += 1

	def loadBalancing(self):
		"""When the load becomes 100%, it means we are using FCFS. Load is relative."""
		totalArrivals = self._nRedArrivals + self._nBlueArrivals
		#Check if a side has relatively more than half the arrivals and give that side priority.
		if self._nRedArrivals / totalArrivals > 0.5:
			print('[!] Left side load: ' + str(round(self._nRedArrivals / totalArrivals * 100, 2)) + '%' + ' and ' + str(self._nRedArrivals) + ' cars are waiting')
			self._turn = 'Red'
		elif self._nBlueArrivals / totalArrivals > 0.5:
			print('\t' * 6 + '[!] Right side load: ' + str(round(self._nBlueArrivals / totalArrivals * 100, 2)) + '%' + ' and ' + str(self._nBlueArrivals) + ' cars are waiting')
			self._turn = 'Blue'
		#else: #if any number of car arrivals is at 50% load, then it's already fair, no need to balance.
		#	pass

	def insertCar(self, car):
		with self._condition:
			while not self.isEmpty() or self._turn != car._color:
				"""
				We call loadBalancing here to override the strict rule (alternating colors),
				by adapting to the load of arrivals of each side. When a side is 50% more loaded
				than the other, we give priority to the overloaded one, to keep crossing even.
				When load is as close as to 50% then, our method does absolutely nothing, thus
				the strict rule takes place.
				"""
				self.loadBalancing()
				self._condition.wait()

			if car._color == 'Red':
				self._nReds += 1
				self._turn = 'Blue'
			elif car._color == 'Blue':
				self._nBlues += 1
				self._turn = 'Red'

			self.collisionDetection()

	def removeCar(self, car):
		with self._condition:
			if car._color == 'Red':
				self._nReds -= 1
				self._nRedArrivals -= 1
			elif car._color == 'Blue':
				self._nBlues -= 1
				self._nBlueArrivals -= 1
			self._condition.notifyAll()
