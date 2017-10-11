import h5py
import numpy as np
import os, errno

def defaultNormalizeFunc(value):
    return value

def defaultValueFunc(data):
    return data['dens'].value

def makeBvox(out_path, fname,
             valueFunc = defaultValueFunc,
             normalizeFunc = defaultNormalizeFunc,
             min_val = 0.,
             max_val = 1.,
             prefix = 'dens'):
    data = h5py.File(fname, 'r')
    z = valueFunc(data)
    z = np.array(z)
    z /= z.max()
    z = normalizeFunc(z)
    z[z < min_val] = min_val
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

def getShape(fpath, key):
    f = h5py.File(fpath, 'r')
    return f[key].value.shape[::-1]
