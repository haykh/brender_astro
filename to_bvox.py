import h5py
import numpy as np
import matplotlib.pyplot as plt
import os, errno

def makeBvox(out_path, fname, valueFunc, normalizeFunc, max_val, prefix = 'dens'):
    data = h5py.File(fname, 'r')
    z = valueFunc(data)
    z = np.array(z)
    z /= z.max()
    z = normalizeFunc(z)
    z[z > max_val] = max_val

    try:
        os.makedirs(out_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    header = np.array([len(z[0][0]),len(z[0]),len(z),1])
    binfile = open(out_path + prefix + '.bvox','wb')
    header.astype('<i4').tofile(binfile)
    z.astype('<f4').tofile(binfile)

    print("bvox saved here:")
    print("\t" + out_path + prefix + '.bvox')
    return out_path + prefix + '.bvox'