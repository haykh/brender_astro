import h5py
import numpy as np
fname = '/Users/hayk/Documents/astroblend/my_experiments/data/flds.tot.004'

data = h5py.File(fname, 'r')
bx = np.array(data['bx'].value)
by = np.array(data['by'].value)
bz = np.array(data['bz'].value)

# u = np.array([bx[150] for i in range(len(bx))])
# v = np.array([by[150] for i in range(len(bx))])
# w = np.array([bz[150]*0. for i in range(len(bx))])
u = bx[150]
v = by[150]

x = range(len(u[0]))
y = range(len(u))
x = np.array(x)
y = np.array(y)
