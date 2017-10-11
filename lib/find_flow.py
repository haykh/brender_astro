import numpy as np
from hilbert_curve import TR_algo8

def next_greater_power_of_2(x):
    return (int(x-1)).bit_length()

def _gen_starting_points_3d(shape):
    nz, ny, nx = shape
    compact_M = [nx, ny, nz]
    points = [TR_algo8(i, compact_M) for i in range(2**sum(compact_M))]
    for pnt in points:
        x = pnt[0]
        y = pnt[1]
        z = pnt[2]
        yield x, y, z

def _gen_starting_points_2d(shape):
    ny, nx = shape
    xfirst = 0
    yfirst = 1
    xlast = nx - 1
    ylast = ny - 1
    x, y = 0, 0
    i = 0
    direction = 'right'
    for i in xrange(nx * ny):
        yield x, y
        if direction == 'right':
            x += 1
            if x >= xlast:
                xlast -= 1
                direction = 'up'
        elif direction == 'up':
            y += 1
            if y >= ylast:
                ylast -= 1
                direction = 'left'
        elif direction == 'left':
            x -= 1
            if x <= xfirst:
                xfirst += 1
                direction = 'down'
        elif direction == 'down':
            y -= 1
            if y <= yfirst:
                yfirst += 1
                direction = 'right'

def grid2map_3d(x, y, z, nx, ny, nz, xi, yi, zi):
    if (xi >= x[-1]) or (xi < x[0]) or (yi >= y[-1]) or (yi > y[-1]) or (zi >= z[-1]) or (zi > z[-1]):
        raise ValueError('xi, yi or zi out of range in grid2map_3d', xi, yi, zi)
    else:
        return (int(nx * (xi - x[0])/(x[-1] - x[0])), int(ny * (yi - y[0])/(y[-1] - y[0])), int(nz * (zi - z[0])/(z[-1] - z[0])))

def map2grid_3d(x, y, z, nx, ny, nz, ni, nj, nk):
    if (ni >= nx) or (ni < 0) or (nj >= ny) or (nj < 0) or (nk >= nz) or (nk < 0):
        raise ValueError('ni, nj or nk out of range in map2grid_3d', ni, nj, nk, nx, ny, nz)
    else:
        return (int((x[-1] - x[0]) * ni / nx), int((y[-1] - y[0]) * nj / ny), int((z[-1] - z[0]) * nk / nz))

def grid2map_2d(x, y, nx, ny, xi, yi):
    if (xi >= x[-1]) or (xi < x[0]) or (yi >= y[-1]) or (yi > y[-1]):
        raise ValueError('xi or yi out of range in grid2map_2d', xi, yi)
    else:
        return (int(nx * (xi - x[0])/(x[-1] - x[0])), int(ny * (yi - y[0])/(y[-1] - y[0])))

def map2grid_2d(x, y, nx, ny, ni, nj):
    if (ni >= nx) or (ni < 0) or (nj >= ny) or (nj < 0):
        raise ValueError('ni or nj out of range in map2grid_2d', ni, nj, nx, ny)
    else:
        return (int((x[-1] - x[0]) * ni / nx), int((y[-1] - y[0]) * nj / ny))

def integrate_2d(xm, ym, x, y, u, v, gmap, seglen):
    x0, y0 = map2grid_2d(x, y, len(gmap[0]), len(gmap), xm, ym)
    nx = len(gmap[0])
    ny = len(gmap)
    xm0 = xm
    ym0 = ym
    x1 = x0
    y1 = y0
    points1 = [[x0, y0]]
    def inside_bounds(xi, yi):
        return (xi >= x[0] and xi <= x[-1]) and (yi >= y[0] and yi <= y[-1])
    # integrate forward
    counter = 0
    while (gmap[ym][xm] == 0 and counter < 1000):
        x0 = x1
        y0 = y1
        u0 = u[int(y1)][int(x1)]
        v0 = v[int(y1)][int(x1)]
        sqr0 = np.sqrt(u0**2 + v0**2)
        if (sqr0 == 0.):
            break
        x1 += seglen * u0 / sqr0
        y1 += seglen * v0 / sqr0
        u1 = u[int(y1)][int(x1)]
        v1 = v[int(y1)][int(x1)]
        sqr1 = np.sqrt(u1**2 + v1**2)
        if (sqr1 == 0.):
            break
        if not inside_bounds(x1, y1):
            break
        if (u1 * u0 + v1 * v0) / (sqr1 * sqr0) <= 0.1:
            # this means the previous direction of vector is strongly different
            if grid2map_2d(x, y, nx, ny, x1, y1) == (xm, ym):
                gmap[ym][xm] = 1
            break
        if grid2map_2d(x, y, nx, ny, x1, y1) != (xm, ym):
            gmap[ym][xm] = 1
            xm, ym = grid2map_2d(x, y, nx, ny, x1, y1)
        points1.append([x1, y1])
        counter += 1

    # integrate backward
    gmap[ym0][xm0] = 0
    xm = xm0
    ym = ym0
    x0, y0 = map2grid_2d(x, y, len(gmap[0]), len(gmap), xm, ym)
    x1 = x0
    y1 = y0

    points2 = []
    counter = 0
    while (gmap[ym][xm] == 0 and counter < 1000):
        x0 = x1
        y0 = y1
        u0 = -u[int(y1)][int(x1)]
        v0 = -v[int(y1)][int(x1)]
        sqr0 = np.sqrt(u0**2 + v0**2)
        if (sqr0 == 0.):
            break
        x1 += seglen * u0 / sqr0
        y1 += seglen * v0 / sqr0
        u1 = -u[int(y1)][int(x1)]
        v1 = -v[int(y1)][int(x1)]
        sqr1 = np.sqrt(u1**2 + v1**2)
        if (sqr1 == 0.):
            break
        if not inside_bounds(x1, y1):
            break
        if (u1 * u0 + v1 * v0) / (sqr1 * sqr0) <= 0.1:
            # this means the previous direction of vector is strongly different
            if grid2map_2d(x, y, nx, ny, x1, y1) == (xm, ym):
                gmap[ym][xm] = 1
            break
        if grid2map_2d(x, y, nx, ny, x1, y1) != (xm, ym):
            gmap[ym][xm] = 1
            xm, ym = grid2map_2d(x, y, nx, ny, x1, y1)
        points2.append([x1, y1])
        counter += 1
    return points2[::-1] + points1


    counter = 0
    while(i >= 0 and j >= 0 and i < len(bx[0]) and j < len(bx) and counter < 200):
        bmax = np.sqrt((bx**2+by**2).max())
        i = int(np.floor(x))
        j = int(np.floor(y))
        bb = np.sqrt(bx[j][i]**2 + by[j][i]**2)
        x += bx[j][i] / bb
        y += by[j][i] / bb
        points.append([x, y])
        counter += 1
        if(rad(x, y) > 100):
            return points
            break
    return points

def integrate_3d(xm, ym, zm, x, y, z, u, v, w, gmap, seglen, region):
    nx = len(gmap[0][0])
    ny = len(gmap[0])
    nz = len(gmap)
    # xmid = 0.5 * (x[-1] - x[0])
    # ymid = 0.5 * (y[-1] - y[0])
    # zmid = 0.5 * (z[-1] - z[0])
    x0, y0, z0 = map2grid_3d(x, y, z, nx, ny, nz, xm, ym, zm)
    xm0 = xm
    ym0 = ym
    zm0 = zm
    x1 = x0
    y1 = y0
    z1 = z0
    points1 = [[x0, y0, z0]]
    def inside_bounds(xi, yi, zi):
        return (xi >= x[0] and xi <= x[-1]) and (yi >= y[0] and yi <= y[-1]) and (zi >= z[0] and zi <= z[-1])
    # integrate forward
    counter = 0
    while (gmap[zm][ym][xm] == 0 and counter < 4000): # max number of iterations is set to 4000
        x0 = x1
        y0 = y1
        z0 = z1
        if not region((x0, y0, z0)):
            break
        u0 = u[int(z1)][int(y1)][int(x1)]
        v0 = v[int(z1)][int(y1)][int(x1)]
        w0 = w[int(z1)][int(y1)][int(x1)]
        sqr0 = np.sqrt(u0**2 + v0**2 + w0**2)
        if (sqr0 == 0.):
            break
        x1 += seglen * u0 / sqr0
        y1 += seglen * v0 / sqr0
        z1 += seglen * w0 / sqr0
        u1 = u[int(z1)][int(y1)][int(x1)]
        v1 = v[int(z1)][int(y1)][int(x1)]
        w1 = w[int(z1)][int(y1)][int(x1)]
        sqr1 = np.sqrt(u1**2 + v1**2 + w1**2)
        if (sqr1 == 0.):
            break
        if not inside_bounds(x1, y1, z1):
            break
        if (u1 * u0 + v1 * v0 + w1 * w0) / (sqr1 * sqr0) <= 0.1:
            # this means the previous direction of vector is strongly different
            if grid2map_3d(x, y, z, nx, ny, nz, x1, y1, z1) == (xm, ym, zm):
                gmap[zm][ym][xm] = 1
            break
        if grid2map_3d(x, y, z, nx, ny, nz, x1, y1, z1) != (xm, ym, zm):
            gmap[zm][ym][xm] = 1
            xm, ym, zm = grid2map_3d(x, y, z, nx, ny, nz, x1, y1, z1)
        points1.append([x1, y1, z1])
        counter += 1

    # integrate backward
    gmap[zm0][ym0][xm0] = 0
    xm = xm0
    ym = ym0
    zm = zm0
    x0, y0, z0 = map2grid_3d(x, y, z, nx, ny, nz, xm, ym, zm)
    x1 = x0
    y1 = y0
    z1 = z0

    points2 = []
    counter = 0
    while (gmap[zm][ym][xm] == 0 and counter < 4000): # max number of iterations is set to 4000
        x0 = x1
        y0 = y1
        z0 = z1
        if not region((x0, y0, z0)):
            break
        x0 = x1
        y0 = y1
        z0 = z1
        u0 = -u[int(z1)][int(y1)][int(x1)]
        v0 = -v[int(z1)][int(y1)][int(x1)]
        w0 = -w[int(z1)][int(y1)][int(x1)]
        sqr0 = np.sqrt(u0**2 + v0**2 + w0**2)
        if (sqr0 == 0.):
            break
        x1 += seglen * u0 / sqr0
        y1 += seglen * v0 / sqr0
        z1 += seglen * w0 / sqr0
        u1 = -u[int(z1)][int(y1)][int(x1)]
        v1 = -v[int(z1)][int(y1)][int(x1)]
        w1 = -w[int(z1)][int(y1)][int(x1)]
        sqr1 = np.sqrt(u1**2 + v1**2 + w1**2)
        if (sqr1 == 0.):
            break
        if not inside_bounds(x1, y1, z1):
            break
        if (u1 * u0 + v1 * v0 + w1 * w0) / (sqr1 * sqr0) <= 0.1:
            # this means the previous direction of vector is different by 90 deg (presumably other fieldline)
            if grid2map_3d(x, y, z, nx, ny, nz, x1, y1, z1) == (xm, ym, zm):
                gmap[zm][ym][xm] = 1
            break
        if grid2map_3d(x, y, z, nx, ny, nz, x1, y1, z1) != (xm, ym, zm):
            gmap[zm][ym][xm] = 1
            xm, ym, zm = grid2map_3d(x, y, z, nx, ny, nz, x1, y1, z1)
        points2.append([x1, y1, z1])
        counter += 1
    return points2[::-1] + points1
