import h5py
import numpy as np
import random
import os, errno

def makeParticles(out_path, fname, n_particles):
    try:
        os.makedirs(out_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    data = h5py.File(fname, 'r')
    xs_e = data['xe'].value
    ys_e = data['ye'].value
    zs_e = data['ze'].value
    xs_i = data['xi'].value
    ys_i = data['yi'].value
    zs_i = data['zi'].value

    # coordinate normalization needs to be fixed!!!

    xs_e -= max(xs_e) * 0.5
    ys_e -= max(ys_e) * 0.5
    zs_e -= max(zs_e) * 0.5
    xs_i -= max(xs_i) * 0.5
    ys_i -= max(ys_i) * 0.5
    zs_i -= max(zs_i) * 0.5

    xs_e /= max(zs_i)
    ys_e /= max(zs_i)
    zs_e /= max(zs_i)
    xs_i /= max(zs_i)
    ys_i /= max(zs_i)
    zs_i /= max(zs_i)

    # / coordinate normalization needs to be fixed!!!

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
    print("Particles written here:")
    print("\t" + out_path + "particles.dat")
    return out_path + "particles.dat"
