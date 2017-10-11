import h5py
import numpy as np
import random
import os, errno

def makeParticles(out_path, fname, shape, n_particles):
    try:
        os.makedirs(out_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    sx, sy, sz = shape

    data = h5py.File(fname, 'r')
    xs_e = (np.array(data['xe'].value) / np.array(sx) - np.array(0.5)) * 2.
    ys_e = (np.array(data['ye'].value) / np.array(sy) - np.array(0.5)) * 2.
    zs_e = (np.array(data['ze'].value) / np.array(sz) - np.array(0.5)) * 2.
    xs_i = (np.array(data['xi'].value) / np.array(sx) - np.array(0.5)) * 2.
    ys_i = (np.array(data['yi'].value) / np.array(sy) - np.array(0.5)) * 2.
    zs_i = (np.array(data['zi'].value) / np.array(sz) - np.array(0.5)) * 2.

    data = []
    es = range(n_particles)
    es = random.sample(range(len(xs_e)), n_particles)
    for i in es:
        data.append([xs_e[i], ys_e[i], zs_e[i], 0])
    ies = range(n_particles)
    ies = random.sample(range(len(xs_i)), len(ies))
    for j in ies:
        data.append([xs_i[j], ys_i[j], zs_i[j], 1])
    np.savetxt(out_path + "particles.dat", data, delimiter=' ', fmt="%s")

    import sys
    if sys.version_info[0] < 3:
        print "Particles written here:"
        print "\t" + out_path + "particles.dat"
    else:
        print("Particles written here:")
        print("\t" + out_path + "particles.dat")
    return out_path + "particles.dat"
