import unittest
from matrix import Matrix
class TestMatrixMethods(unittest.TestCase):
	
	'''def __init__(self):
		super().__init__(self)
		self.m1234 = Matrix('1,2;3,4')
		self.mzeroes = Matrix('0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0')
		try:
			nonRect = Matrix('1,3;1,3,4,5;0')
		except AssertionError:
			print('hi')
			pass
		else:
			raise RuntimeException("Bad matrix did not raise error")'''
	def test_main(self):
		#print('hi1324')
		pass
	def test_determinant(self):
		self.assertEqual(Matrix('0,0;0,0').getDeterminant(),0)
		self.assertEqual(Matrix('1,2;3,4').getDeterminant(),-2)
		self.assertEqual(Matrix('-1,-2;-3,-4').getDeterminant(),-2)
		self.assertEqual(Matrix('1,2,3;4,5,6;0,8,9').getDeterminant(),21)
		self.assertEqual(Matrix('7').getDeterminant(),7)
	def test_diagonal(self):
		self.assertEqual(Matrix('0,0;0,0').getDiagonalVals(),[0,0])
		self.assertEqual(Matrix('1,2;3,4').getDiagonalVals(),[1,4])
	def test_transpose(self):
		self.assertEqual(Matrix('1,2;3,4').transpose(),Matrix('1,3;2,4'))
		self.assertEqual(Matrix('0,0;0,0').transpose(),Matrix('0,0;0,0'))
		self.assertEqual(Matrix('1,2,3;4,5,6').transpose(),Matrix('1,4;2,5;3,6'))
		self.assertEqual(Matrix('1,4;2,5;3,6').transpose(),Matrix('1,2,3;4,5,6'))
	def test_spaces(self):
		longie = Matrix('1,-1,1,3,2;2,-1,1,5,1;3,-1,1,7,0;0,1,-1,-1,-3')
		self.assertEqual(longie.getRowSpace(),Matrix('1,0,0,0,0;0,1,0,0,0'))
		self.assertEqual(longie.getColSpace(),Matrix('1,0,0,0;0,1,0,0'))
	#def test_rref(self):
	#	self.assertEqual(Matrix('1,2;3,4').getRREF(),Matrix('1,0;0,1').getRREF())
	#	self.assertEqual(Matrix('1,2,3;4,5,6').getRREF(),Matrix('1,0,-1;0,1,2').getRREF())
if __name__ == '__main__':
	unittest.main()