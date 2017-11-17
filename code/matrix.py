class Matrix:
	def __init__(self,matInput):
		#print(matInput)
		self.data = self.evaluateMatrixInput(matInput)
		self.ref = self.getRowEchelonForm()
		
	def evaluateMatrixInput(self,m):
		'''
		Could be:
			'1 2 3;4 5 6;7 8 9'
			'1,2,3;4,5,6;7,8,9'
			'1&2&3@4&5&6@7&8&9'
			[[1,2,3],[4,5,6],[7,8,9]]
				Or any combination of tuples
		'''
		#print('hi1 '+str(args))
		#print('hi2 '+str(args[0]))
		#print('hi3 '+str(args[1]))
		data = list()
		if isinstance(m,str):
			m2 = m.replace('&',' ').replace('@',';')
			rowsString = m2.split(';')
			#print(str(rowsString))
			for i in range(len(rowsString)):
				rowString = rowsString[i]
				colElements = [float(element) for element in rowString.split(' ')]
				#print(str(colElements))
				data.append(tuple(colElements))
				#for j in range(len(colElements)):
					#print(str(i))
					#print(str(j))
				#	data[i][j] = colElements[j]
		#elif isinstance(m,(list,tuple)):
		return tuple(data)
		
	def getRowEchelonForm(self):
		def numLeadingZeroes(row):
			count = 0
			for element in row:
				if element == 0:
					count += 1
				else:
					break
			return count
		ref = sorted([list(row) for row in list(self.data)],key=numLeadingZeroes)
		for upperRowNum in range(len(ref)):
			upperRow = ref[upperRowNum]
			colIndex = upperRowNum
			for lowerRowNum in range(upperRowNum+1,len(ref)):
				lowerRow = ref[lowerRowNum]
				lowerRowElement = lowerRow[colIndex]
				if lowerRowElement == 0:
					continue
				upperRowElement = upperRow[colIndex]
				multBy = lowerRowElement/upperRowElement
				#print('multBy on row '+str(lowerRowNum)+': '+str(multBy))
				for j in range(colIndex,len(lowerRow)):
					lowerRow[j] -= multBy*upperRow[j]
				#assert(row[i-1]==0),"Should be zero: "+str(row[i-1])
				#oldRow = self.data[i]
				#newRow = list()
				#multRowAbove
				#for j in range(i):
				#	colElement = self[
			print('upperRowNum: '+str(upperRowNum))
			print(str(ref))
			#print('lmao')
		return ref
		
		
	def __str__(self):
		s = str()
		for row in self.data:
			s +='\n '
			for element in row:
				s += str(element) + ' '
		return s
		
	def __getitem__(self,key):
		return self.data[key[0]][key[1]]
	#def __setitem__(self,key,value):
	#	self.data[key[0]]
	
	
if __name__ == "__main__":
	thing = Matrix('1 2 3;4 5 6;7 8 9')
	print(str(thing))
	print(str(thing[1,2]))