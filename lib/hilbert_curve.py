import math
import numpy as np

########################################################################################
#
#   3D Hilbert curve
#       algorithm borrowed from here: http://pdebuyl.be/blog/2015/hilbert-curve.html
#
########################################################################################

def rotate_right(x, d):
    """Rotate x by d bits to the right."""
    N = 3
    d = d % N
    out = x >> d
    for i in range(d):
        bit = (x & 2**i)>>i
        out |= bit << (N+i-d)
    return out

def rotate_left(x, d):
    """Rotate x by d bits to the left."""
    N = 3
    d = d % N
    out = x << d
    excess = out
    out = out & (2**N-1)
    for i in range(d):
        bit = (x & 2**(N-1-d+1+i))>> (N-1-d+1+i)
        out |= bit << i
    return out

def bit_component(x, i):
    """Return i-th bit of x"""
    return (x & 2**i) >> i

def extract_mask(i, compact_M):
    """Extract the mask for iteration i of the algorithm.
    Algorithm 6 in [TR]"""
    N = 3
    mu = 0
    for j in range(N-1, -1, -1):
        mu = mu << 1
        if compact_M[j] > i:
            mu = mu | 1
    return mu

def gcr(i, mu, pi):
    """Compute the gray code rank of i given the mask mu.
    Algorithm 4 in [TR]"""
    N = 3
    r = 0
    for k in range(N-1, -1, -1):
        if bit_component(mu, k):
            r = (r << 1) | bit_component(i, k)
    return r

def gcr_inv(r, mu, pi):
    """Inverse of the gray code rank, given the mask mu and the pattern pi.
    Algorithm 5 in [TR]"""
    N = 3
    i = 0
    g = 0
    j = sum([bit_component(mu, k) for k in range(N)])-1
    for k in range(N-1, -1, -1):
        if bit_component(mu, k)==1:
            i |= bit_component(r, j) << k
            g |= ( (bit_component(i, k) + bit_component(i, k+1))%2 ) << k
            j -= 1
        else:
            g |= bit_component(pi, k) << k
            i |= ( (bit_component(g, k) + bit_component(i, k+1)) % 2) << k
    return i

def gc(i):
    """Return the Gray code index of i."""
    return i ^ (i >> 1)

def g(i):
    """The direction between subcube i and the next one"""
    return int(np.log2(gc(i)^gc(i+1)))

def e(i):
    """Return the entry point of hypercube i."""
    if i==0:
        return 0
    else:
        return gc(2*int(math.floor((i-1)//2)))

def d(i):
    """The direction of the arrow whithin a subcube."""
    N = 3
    if i==0:
        return 0
    elif (i%2)==0:
        return g(i-1) % N
    else:
        return g(i) % N

def T(e, d, b):
    """Transform b."""
    out = b ^ e
    return rotate_right(out, d+1)

def T_inv(e, d, b):
    """Inverse transform b."""
    N = 3
    return T(rotate_right(e, d+1), N-d-2, b)

def TR_algo8(h, compact_M):
    """Compute the point with compact Hilbert index h"""
    N = 3
    ve = 0
    vd = 2
    k = 0
    p = [0,]*N
    m = max(compact_M)
    vM = sum(compact_M)
    for i in range(m-1, -1, -1):
        mu = extract_mask(i, compact_M)
        mu_norm = sum([bit_component(mu, j) for j in range(N)])
        mu = rotate_right(mu, vd+1)
        pi = rotate_right(ve, vd+1) & (~mu & 2**N-1)
        r = [bit_component(h, vM - k - (j+1)) for j in range(mu_norm)][::-1]
        r = sum( [rx*2**j for j, rx in enumerate(r)] )
        k = k + mu_norm
        w = gcr_inv(r, mu, pi)
        l = gc(w)
        l = T_inv(ve, vd, l)
        for j in range(N):
            p[j] |= bit_component(l, j) << i
        ve = ve ^ (rotate_left(e(w), vd+1))
        vd = (vd + d(w) + 1) % N
    return p
