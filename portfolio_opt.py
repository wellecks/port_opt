from cvxopt import matrix, solvers
from cvxopt.modeling import variable
import stocks
import numpy

# chosen using http://money.msn.com/investing/stockscouter-stock-category.aspx
symbols = ['GOOG', 'AIMC', 'CE', 'BH', 'AHGP', 'AB', 'HLS', 'BKH', 'LUV']

start = '1/1/2010'
end   = '1/1/2014'

n       = len(symbols)
avg_ret = matrix(map(lambda s: stocks.avg_return(s, start, end, 'y'), symbols))
covs    = matrix(numpy.array(stocks.cov_matrix(symbols, start, end, 'y')))

# minimum return
r_min = 0.10
budget = 10000.0

# solve the QP:
# minimize   x'Px + q'x
# subject to Gx <= h
#            Ax == b
P = covs
# x is the allocation of the portfolio
x = variable(n)
q = matrix(numpy.zeros((n, 1)), tc='d')
# inequality constraints Gx <= h
# captures the constraints (avg_ret'x >= r_min) and (x >= 0)
G = matrix(numpy.concatenate((
	-numpy.transpose(numpy.array(avg_ret)), 
	-numpy.identity(n)), 0))
h = matrix(numpy.concatenate((
	-numpy.ones((1,1))*r_min, 
	numpy.zeros((n,1))), 0))
# equality constraint Ax = b; captures the constraint sum(x) == 1
A = matrix(1.0, (1,n))
b = matrix(1.0)
sol = solvers.qp(P, q, G, h, A, b)