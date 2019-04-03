from threading import Thread
import time

class Car(Thread):
	"""docstring for Car."""
	def __init__(self, id, color, destination):
		super(Car, self).__init__()
		self._id = id
		self._color = color
		self._state = 'INSTANCIATED'
		self._destination = destination

	def run(self):
		self._destination.arrived(self)
		self._state = 'Arrived'
		print(self)

		self._destination.insertCar(self)
		self._state = 'Passing'
		print(self)

		self._destination.removeCar(self)
		self._state = 'Passed'
		print(self)

	def __repr__(self):
		nTabs = 0
		if self._state == 'Passing':
			nTabs = 4
		elif self._state == 'Passed':
			if self._color == 'Red':
				nTabs = 8
			else: #Blue
				nTabs = 0
		elif self._state == 'Arrived':
			if self._color == 'Red':
				nTabs = 0
			else: #Blue
				nTabs = 8
		else:
			self._state == 'MALFUNCTIONED'

		myTime = time.localtime()
		return '\t' * nTabs + self._color + ' Car ' + str(self._id) + ' ' + self._state + ' at ' + str(time.clock())# str(myTime[3]) + ':' + str(myTime[4]) + ':' + str(myTime[5]) #time.pthread_getcpuclockid(self.ident)
