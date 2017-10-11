import h5py
import numpy as np

def defaultRegionFunc(point):
    return True

def generateFieldlines(fpath,
                       density = 1.,
                       keys = ('bx', 'by', 'bz'),
                       n_traj = 100,
                       region = defaultRegionFunc,
                       min_seglen = 100.,
                       seg_step = 0.2):
    key_1, key_2, key_3 = keys

    data = h5py.File(fpath, 'r')
    u = np.array(data[key_1].value)
    v = np.array(data[key_2].value)
    w = np.array(data[key_3].value)

    maxUVW = np.sqrt(u**2 + v**2 + w**2).max()
    u /= maxUVW
    v /= maxUVW
    w /= maxUVW

    size_x = len(u[0][0])
    size_y = len(u[0])
    size_z = len(u)
    x = range(size_x)
    y = range(size_y)
    z = range(size_z)
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    from find_flow import _gen_starting_points_3d, next_greater_power_of_2, grid2map_3d, map2grid_3d, integrate_3d

    n_cells_x = int(30 * density)
    n_cells_y = int(30 * density)
    n_cells_z = int(30 * density)
    nx_2 = next_greater_power_of_2(n_cells_x)
    ny_2 = next_greater_power_of_2(n_cells_y)
    nz_2 = next_greater_power_of_2(n_cells_z)
    n_cells_x = 2**nx_2
    n_cells_y = 2**ny_2
    n_cells_z = 2**nz_2
    gmap = np.zeros((n_cells_z, n_cells_y, n_cells_x))

    trajectories = []
    for xm, ym, zm in _gen_starting_points_3d((nx_2, ny_2, nz_2)):
        if gmap[zm][ym][xm] == 0:
            t = integrate_3d(xm, ym, zm, x, y, z, u, v, w, gmap, seg_step, region)
            if (t is not None) and (len(t) > min_seglen / seg_step):
                trajectories.append(t)
    import random as rnd
    if len(trajectories) > n_traj:
        trajectories = np.random.choice(trajectories, n_traj)
    return trajectories

def exportFieldlines(trajectories, out_path):
    f = open(out_path, 'w')
    for line in trajectories:
        f.write('{}\n'.format(len(line)))
        for coords in line:
            x,y,z = coords
            f.write('{} {} {}\n'.format(x, y, z))
    f.close()
    import sys
    if sys.version_info[0] < 3:
        print 'trajectories saved here:'
        print '\t' + out_path
    else:
        print ('trajectories saved here:')
        print ('\t' + out_path)
