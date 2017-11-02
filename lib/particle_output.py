import h5py
import numpy as np
import random
import os, errno
import os.path

# this function is specifically for TRISTAN (hdf5 format)
def makeParticles(out_path,
                  fpart,
                  n_particles,
                  istep = None,
                  shape = None
                  ):
    try:
        os.makedirs(out_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    param = fpart.replace('prtl.tot', 'param')
    flds = fpart.replace('prtl.tot', 'flds.tot')
    if os.path.isfile(param):
        prm = h5py.File(param, 'r')
        sx = prm['mx0'].value[0]
        sy = prm['my0'].value[0]
        sz = prm['mz0'].value[0]
    elif os.path.isfile(flds):
        print ('`param` file not found, trying to figure out from `flds`')
        if istep is None:
            print ('\t`istep` required in the input')
            return
        else:
            fields = h5py.File(flds, 'r')
            dns = fields['dens'].value
            sx = len(dns[0][0]) * istep
            sy = len(dns[0]) * istep
            sz = len(dns) * istep
    else:
        print ('`param` & `flds` files not found, give sizes manually')
        if shape is None:
            print ('\t`shape` required in the input')
        else:
            sx, sy, sz = shape

    size = min(sx, sy, sz)
    data = h5py.File(fpart, 'r')
    xs_e = (np.array(data['xe'].value) / np.array(size) - np.array(0.5 * sx / size)) * 2.
    ys_e = (np.array(data['ye'].value) / np.array(size) - np.array(0.5 * sy / size)) * 2.
    zs_e = (np.array(data['ze'].value) / np.array(size) - np.array(0.5 * sz / size)) * 2.
    xs_i = (np.array(data['xi'].value) / np.array(size) - np.array(0.5 * sx / size)) * 2.
    ys_i = (np.array(data['yi'].value) / np.array(size) - np.array(0.5 * sy / size)) * 2.
    zs_i = (np.array(data['zi'].value) / np.array(size) - np.array(0.5 * sz / size)) * 2.

    data = []
    es = range(n_particles)
    if (n_particles > len(xs_e)) or (n_particles > len(xs_i)):
        n_particles = min(len(xs_e), len(xs_i))
    es = random.sample(range(len(xs_e)), n_particles)
    for i in es:
        data.append([xs_e[i], ys_e[i], zs_e[i], 0])
    ies = range(n_particles)
    ies = random.sample(range(len(xs_i)), len(ies))
    for j in ies:
        data.append([xs_i[j], ys_i[j], zs_i[j], 1])
    np.savetxt(out_path + "particles.dat", data, delimiter=' ', fmt="%s")

    print ("Particles written here:")
    print ("\t" + out_path + "particles.dat")
    return out_path + "particles.dat"
