import numpy as np, cv2
cv2.setNumThreads(1)
def norm28(img, thr=0.08):
    """ink float image (any size, ink=1) -> 28x28 MNIST-style: bbox fit 20px, centre of mass in 28x28. returns None if empty"""
    m = img > thr
    if not m.any(): return None
    ys, xs = np.where(m); y0, y1, x0, x1 = ys.min(), ys.max()+1, xs.min(), xs.max()+1
    c = img[y0:y1, x0:x1]
    h, w = c.shape; k = 20.0/max(h, w)
    nw, nh = max(1, int(round(w*k))), max(1, int(round(h*k)))
    r = cv2.resize(c, (nw, nh), interpolation=cv2.INTER_AREA)
    out = np.zeros((28, 28), np.float32)
    s = r.sum()
    cy = (r.sum(1)*np.arange(nh)).sum()/s + .5; cx = (r.sum(0)*np.arange(nw)).sum()/s + .5
    oy = int(round(14-cy)); ox = int(round(14-cx))
    oy = max(0, min(28-nh, oy)); ox = max(0, min(28-nw, ox))
    out[oy:oy+nh, ox:ox+nw] = r
    return out

def augment(img28, rng, S=84):
    """MNIST digit -> varied 'finger on iPad' digit, normalised to 28x28."""
    a = cv2.resize(img28.astype(np.float32)/255., (S, S), interpolation=cv2.INTER_CUBIC)
    a = np.clip(a, 0, 1)
    ang = np.clip(rng.normal(0, 8), -20, 20)*np.pi/180
    sx, sy = rng.uniform(.8, 1.2, 2); sh = rng.uniform(-.3, .3)
    c, s_ = np.cos(ang), np.sin(ang)
    M = np.array([[c*sx, -s_*sy+sh*sx*0.0+sh, 0], [s_*sx, c*sy, 0]], np.float32)
    ctr = np.array([S/2, S/2]); M[:, 2] = ctr - M[:, :2]@ctr + rng.uniform(-4, 4, 2)
    a = cv2.warpAffine(a, M, (S, S), flags=cv2.INTER_CUBIC, borderValue=0)
    # slight wobble (smooth random displacement)
    if rng.random() < .6:
        dx = cv2.GaussianBlur(rng.normal(0, 1, (S, S)).astype(np.float32), (0, 0), 9)*rng.uniform(20, 60)
        dy = cv2.GaussianBlur(rng.normal(0, 1, (S, S)).astype(np.float32), (0, 0), 9)*rng.uniform(20, 60)
        gx, gy = np.meshgrid(np.arange(S, dtype=np.float32), np.arange(S, dtype=np.float32))
        a = cv2.remap(a, gx+dx, gy+dy, cv2.INTER_LINEAR, borderValue=0)
    # stroke thickness
    t = rng.random()
    if t < .12:
        a = cv2.erode(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    elif t < .88:
        r = int(rng.integers(0, 7))
        if r: a = cv2.dilate(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*r+1, 2*r+1)))
    a = cv2.GaussianBlur(a, (0, 0), rng.uniform(.6, 1.6))
    a = np.clip(a*rng.uniform(1.0, 1.6), 0, 1)
    return norm28(a), a

def scribble(rng, S=84):
    a = np.zeros((S, S), np.uint8); kind = rng.integers(0, 4)
    th = int(rng.integers(3, 12))
    if kind == 0:   # random polyline scribble
        n = int(rng.integers(7, 14)); p = rng.uniform(8, S-8, (n, 2)).astype(np.int32)
        cv2.polylines(a, [p], False, 255, th, cv2.LINE_AA)
    elif kind == 1: # zig-zag / hatch fill
        x0, y0, w, h = rng.integers(5, 30), rng.integers(5, 30), rng.integers(25, 50), rng.integers(25, 50)
        for i in range(int(rng.integers(4, 10))):
            xa = x0+int(rng.integers(0, w)); xb = x0+int(rng.integers(0, w))
            cv2.line(a, (xa, y0), (xb, y0+h), 255, th, cv2.LINE_AA)
    elif kind == 2: # blob / ring-ish
        cv2.ellipse(a, (S//2, S//2), (int(rng.integers(8, 30)), int(rng.integers(8, 30))), rng.uniform(0, 180), 0, 360, 255, -1, cv2.LINE_AA)
    else:           # short dash / dot / cross
        if rng.random() < .5:
            y = int(rng.integers(25, 60)); cv2.line(a, (20, y), (20+int(rng.integers(15, 45)), y+int(rng.integers(-6, 6))), 255, th, cv2.LINE_AA)
        else:
            cv2.line(a, (20, 20), (60, 60), 255, th, cv2.LINE_AA); cv2.line(a, (60, 20), (20, 60), 255, th, cv2.LINE_AA)
    return norm28(cv2.GaussianBlur(a.astype(np.float32)/255., (0, 0), rng.uniform(.6, 1.4)))

def junk(X, rng, S=84):
    k = rng.random()
    if k < .35:    # two digits merged / overlapping
        i, j = rng.integers(0, len(X), 2)
        _, a = augment(X[i], rng); _, b = augment(X[j], rng)
        d = int(rng.integers(-26, 8))
        b = np.roll(b, d, axis=1)
        # place side by side but overlapping heavily: digits shrunk horizontally
        a = cv2.resize(a, (S//2+10, S))[:, :]; b2 = cv2.resize(b, (S//2+10, S))
        canvas = np.zeros((S, S*2), np.float32)
        off = int(rng.integers(0, 22))
        canvas[:, :a.shape[1]] += a; canvas[:, off:off+b2.shape[1]] = np.maximum(canvas[:, off:off+b2.shape[1]], b2)
        return norm28(np.clip(canvas, 0, 1))
    if k < .6:     # crossed-out digit
        i = rng.integers(0, len(X)); _, a = augment(X[i], rng); a = (a*255).astype(np.uint8)
        for _ in range(int(rng.integers(1, 3))):
            p1 = (int(rng.integers(0, S)), int(rng.integers(0, S))); p2 = (int(rng.integers(0, S)), int(rng.integers(0, S)))
            cv2.line(a, p1, p2, 255, int(rng.integers(3, 9)), cv2.LINE_AA)
        return norm28(a.astype(np.float32)/255.)
    return scribble(rng)
