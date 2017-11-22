class Matrix:
	def __init__(self,matInput):
		self.data = self.evaluateMatrixInput(matInput)
		assert self.isValid(),"Matrix is not valid. Data input: "+str(self.data)
		self.numRows = len(self.data)
		self.numCols = len(self.data[0])
		self.isSquare = (self.numRows == self.numCols)
		self.onlyOneEntry = (self.numRows == self.numCols == 1)
	def isValid(self):
		rowLength = len(self.data[0])
		for row in self.data:
			if len(row) != rowLength:
				print("Bad row: \t"+str(row))
				print("Should have length: "+str(rowLength))
				return False
		return True
	def evaluateMatrixInput(self,m):
		'''
		Could be:
			'1 2 3;4 5 6;7 8 9'
			'1,2,3;4,5,6;7,8,9'
			'1&2&3@4&5&6@7&8&9'
			[[1,2,3],[4,5,6],[7,8,9]]
				Or any combination of tuples
		'''
		if isinstance(m,str):
			data = list()
			m2 = m.replace('&',' ').replace(',',' ').replace('@',';')
			rowsString = m2.split(';')
			for i in range(len(rowsString)):
				rowString = rowsString[i]
				colElements = [float(element) for element in rowString.split(' ')]
				data.append(tuple(colElements))
			return tuple(data)
		elif isinstance(m,(list,tuple)):
			assert isinstance(m[0],(list,tuple)),"m[0] is of type "+str(type(m[0]))
			data = m
			return data
	def getDiagonalVals(self):
		return [self[rcNum,rcNum] for rcNum in range(min(self.numRows,self.numCols))]
	def isDiagonal(self):
		return self.isUpperTriangular() and self.isLowerTriangular()
	def isUpperTriangular(self):
		return all([self[rowNum,colNum]==0 for rowNum in range(self.numRows) for colNum in range(rowNum)])
	def isLowerTriangular(self):
		return all([self[rowNum,colNum]==0 for rowNum in range(self.numRows) for colNum in range(rowNum+1,self.numCols)])
	def getREF(self):
		def numLeadingZeroes(row):
			for i in range(len(row)):
				if not row[i]==0:
					return i
			return len(row)
		ref = sorted([list(row) for row in list(self.data)],key=numLeadingZeroes)
		for upperRowNum in range(min(len(ref),len(ref[0]))): #Changed this with min
			colIndex = upperRowNum
			for lowerRowNum in range(upperRowNum+1,len(ref)):
				if ref[lowerRowNum][colIndex] != 0 and ref[upperRowNum][colIndex] != 0:
					multBy = ref[lowerRowNum][colIndex] / ref[upperRowNum][colIndex]
					for j in range(len(ref[lowerRowNum])):
						ref[lowerRowNum][j] -= multBy*ref[upperRowNum][j]
		return Matrix(ref)
	def getRREF(self):
		m = self.getREF().flipflopped().getREF().flipflopped().getREF()
		for rowNum in range(m.numRows):
			fnz = Matrix.firstNonzero(m.data[rowNum])
			if fnz is not None:
				divisor = m.data[rowNum][fnz]
				for colNum in range(m.numCols):
					m.data[rowNum][colNum] = m.data[rowNum][colNum]/divisor
		return m
	def flipflopped(self):
		#Rotate horizontally and vertically. Not the same as transpose.
		return Matrix([list(reversed(row)) for row in reversed(self.data)])
	def transpose(self):
		t = [[self[colNum,rowNum] for colNum in range(self.numRows)] for rowNum in range(self.numCols)]
		return Matrix(t)
	def getDeterminant(self):
		if not self.isSquare:
			print("Warning - Determinant is only defined for square matrices")
			return None
		if self.onlyOneEntry:
			return self[0,0]
		det = 0
		rowNum = 0
		for colNum in range(self.numCols):
			sign = 1 if (colNum%2 == 0) else -1
			det += sign*self[rowNum,colNum]*self.matrixWithoutRowCol(rowNum,colNum).getDeterminant()
		return det
	def isZeroMatrix(self):
		for rowNum in self.numRows:
			for colNum in self.numCols:
				if self[rowNum,colNum] != 0:
					return False
		return True
	def __bool__(self):
		return self.isZeroMatrix()
	def __eq__(self,other):
		if self.numRows != other.numRows or self.numCols != other.numCols:
			return False
		for rowNum in range(self.numRows):
			for colNum in range(self.numCols):
				if self[rowNum,colNum] != other[rowNum,colNum]:
					return False
		return True
		#return self.data == other.data
	def matrixWithoutRowCol(self,rowNumExclude,colNumExclude):
		without = list()
		for rowNum in range(self.numRows):
			if (rowNum != rowNumExclude):
				currentRow = list()
				for colNum in range(self.numCols):
					if (colNum != colNumExclude):
						currentRow.append(self[rowNum,colNum])
				without.append(currentRow)
		withoutMatrix = Matrix(without)
		return Matrix(without)
		
	def __str__(self):
		s = str()
		for row in self.data:
			s +='\n '
			for element in row:
				s += str(element) + ' '
		return s
		
	def __getitem__(self,key):
		return self.data[key[0]][key[1]]
	def getRowSpace(self):
		return Matrix([row for row in self.getRREF().data if not all(val == 0 for val in row)])
	def getColSpace(self):
		#return Matrix([row for row in self.transpose().getRowSpace().transpose().data if not all(val==0 for val in row)])
		#return Matrix([row for row in self.transpose().getRREF().transpose().data if not all(val == 0 for val in row)])
		return Matrix([row for row in self.transpose().getRowSpace().data if not all(val==0 for val in row)])
	def getRank(self):
		assert(len(self.getRowSpace().data) == len(self.getColSpace().data)),"Error in code - Length of row space and length of column space do not match up"
		return len(self.getRowSpace().data)
	def withExtendedCol(self,vec):
		assert(self.numRows == len(vec)),"Error - Number of rows in matrix must equal length of vector"
		extended = Matrix([list(self.data[rowNum])+[vec[rowNum]] for rowNum in range(self.numRows)])
		#print("Before: \n"+str(self))
		#print("After: \n"+str(extended))
		return extended
	def withoutZeroRows(self):
		reduced = Matrix([row for row in self.data if not all (val==0 for val in row)])
		#print("Before reduction: \n"+str(self))
		#print("After reduction: \n"+str(reduced))
		return reduced
		
		
	def vectorSolutions(self,vec):
		def hasOneNonzeroLastRow(row):
			return Matrix.firstNonzero(row) == len(row)-1
		def hasOneNonzeroVar(row):
			return len([True for index in range(len(row)-1) if row[index] != 0]) == 1
		#print("\n\n\n\n\n")
		m = self.withExtendedCol(vec).getRREF().withoutZeroRows()
		sVec = [None]*(m.numCols-1) #solution vector (will not only contain numbers)
		for row in m.data:
			if hasOneNonzeroLastRow(row):
				return None #This means that we have an impossible situation
			elif hasOneNonzeroVar(row):
				nonzeroIndex = [val==0 for val in row].index(False)
				sVec[nonzeroIndex] = row[len(row)-1]/row[nonzeroIndex]
		colNumsWithPivots = list(set([Matrix.firstNonzero(row) for row in m.data if Matrix.firstNonzero(row) is not None]))
		colNumsWithoutPivots = [colNum for colNum in range(m.numCols-1) if colNum not in colNumsWithPivots]
		for colNum in colNumsWithoutPivots:
			sVec[colNum] = MParam('Param'+str(colNum))
		noneIndeces = [index for index in range(len(sVec)) if sVec[index] is None]
		for noneIndex in noneIndeces:
			for rowNum in range(m.numRows):
				row = m.data[rowNum]
				if row[noneIndex] != 0:
					assert(row[noneIndex] is not None),"Dunno how that's possible, thing in matrix is none"
					resultant = MParam(row[len(row)-1])
					for colNum in range(len(row)-1):
						if colNum != noneIndex and row[colNum] != 0:
							try:
								resultant = resultant - row[colNum]*sVec[colNum] #I think?
							except TypeError:
								resultant = resultant - MParam(row[colNum])*MParam(sVec[colNum])
					resultant = resultant / row[noneIndex]
					sVec[noneIndex] = resultant
		return sVec
	def nullSpace(self):
		return self.vectorSolutions([0]*self.numRows)
	'''
	def timesVector(self,vec):
		#assert(len(vec) == self.numCols),"Attempted to multiply "+str(self)+" by "+str(vec)+", but the inner dimensions do not match."
		#solutionVec = [None]*
		vecAsMatFlip = Matrix([[element] for element in vec])
		return self.timesMatrix(vecAsMatFlip)
	def timesMatrix(self,m):
		assert(self.numCols == m.numRows),"Attempted to multiply "+str(self)+" by "+str(m)+", but the inner dimensions do not match."
		solutionMatrix = 
	def dominantEigenValue(self,numIters=10):
		initialApprox = [1]*self.numRows
		for iter in range(numIters):
	'''
			
	@staticmethod
	def firstNonzero(vec):
		for index in range(len(vec)):
			if (vec[index] != 0):
				return index
		return None
	def extendedString(self):
		s = "\n\n\nOriginal: \n"+str(self)
		s += "\nREF: "+str(self.getREF())
		s += "\nRREF: "+str(self.getRREF())
		s += "\nDet: "+str(self.getDeterminant())
		s += "\nDiagonal vals: "+str(self.getDiagonalVals())
		s += "\nIs lower triangular: "+str(self.isLowerTriangular())
		s += "\nIs upper triangular: "+str(self.isUpperTriangular())
		s += "\nRow space: \n"+str(self.getRowSpace())
		s += "\nCol space: \n"+str(self.getColSpace())
		s += "\nRank: "+str(self.getRank())
		s += "\nNull space: "+str([str(element) for element in self.nullSpace()])
		return s+"\n\n\n"
class MParam:
	def __init__(self,paramStr):
		self.paramStr = str(paramStr)
	def __str__(self):
		return self.paramStr
	def arith(self,other,symbol):
		return MParam('('+str(self)+str(symbol)+str(other)+')')
	def __add__(self,other):
		try:
			if float(str(other)) == 0:
				return self
		except:
			pass
		try:
			if float(str(self)) == 0:
				return MParam(other)
		except:
			pass
		return self.arith(other,'+')
	def __sub__(self,other):
		try:
			if float(str(other)) == 0:
				return self
		except:
			pass
		try:
			if float(str(self)) == 0:
				return MParam(other)
		except:
			pass
		return self.arith(other,'-')
	def __mul__(self,other):
		try:
			if float(str(other)) == 1:
				return self
		except:
			pass
		try:
			if float(str(self)) == 1:
				return MParam(other)
		except:
			pass
		return self.arith(other,'*')
	def __truediv__(self,other):
		try:
			if float(str(other)) == 1:
				return self
		except:
			pass
		try:
			if float(str(self)) == 1:
				return MParam(other)
		except:
			pass
		return self.arith(other,r'/')
		
if __name__ == "__main__":
	#thing = Matrix('1 2 3;4 5 6;7 8 9')
	#thing = Matrix('1 2;3 4')
	#thing = Matrix('1,-1,1,3,2;2,-1,1,5,1;3,-1,1,7,0;0,1,-1,-1,-3')
	thing = Matrix('2,-1,3;0,0,7')
	print(str(thing.extendedString()))
	
	