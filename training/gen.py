import numpy as np, time, sys
from common import *
d = np.load('mnist.npz'); X, y, Xt, yt = d['X'], d['y'], d['Xt'], d['yt']
rng = np.random.default_rng(1)
def build(Xs, ys, copies, njunk, rng):
    out = []; lab = []
    for c in range(copies):
        for i in range(len(Xs)):
            im, _ = augment(Xs[i], rng)
            if im is None: continue
            out.append(im); lab.append(ys[i])
        print('copy', c, time.time()-t0, flush=True)
    for i in range(njunk):
        im = junk(Xs, rng)
        if im is None: continue
        out.append(im); lab.append(10)
    return (np.clip(np.stack(out), 0, 1)*255).astype(np.uint8), np.array(lab, np.uint8)
t0 = time.time()
# clean MNIST copy as-is too (digits 0-9) so the model keeps the original style
Xtr, ytr = build(X, y, 5, 50000, rng)
Xtr = np.concatenate([Xtr, X]); ytr = np.concatenate([ytr, y])
Xte, yte = build(Xt, yt, 1, 1500, np.random.default_rng(7))   # held-out augmented test (from test digits only)
np.savez_compressed('data.npz', Xtr=Xtr, ytr=ytr, Xte=Xte, yte=yte, Xm=Xt, ym=yt)
print(Xtr.shape, Xte.shape, np.bincount(ytr), time.time()-t0)
