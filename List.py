class SortedList(list):
	
	def __init__(self):
		list.__init__(self)
		
	def append(self, newElement):
		
		bottomIndex,topIndex = 0,len(self)
		middleIndex = int( topIndex/2 )
		
		while bottomIndex != topIndex:
			
			if newElement < self[middleIndex]:
				topIndex = middleIndex
			else:
				bottomIndex = middleIndex + 1
                
			middleIndex = int( (bottomIndex + topIndex)/2 )	

		self.insert( middleIndex, newElement )

class SortCacheList(list):
	
	def __init__(self):
		
		list.__init__(self)
		self.isSorted = False
		
	def sort(self):
		
		if not self.isSorted:
			super(SortCacheList, self).sort()
			self.isSorted = True
	
	def append(self, item):

		self.isSorted = False
		super(SortCacheList, self).append(item)
    
"""
>>> def heapsort(iterable):
...     'Equivalent to sorted(iterable)'
...     h = []
...     for value in iterable:
...         heappush(h, value)
...     return [heappop(h) for i in range(len(h))]
"""
