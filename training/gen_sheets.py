import numpy as np, cv2, json, subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont
from common import augment
m = np.load('mnist.npz'); Xt, yt = m['Xt'], m['yt']
pool = {d: np.where(yt == d)[0] for d in range(10)}
fonts = []
for ln in subprocess.run(['fc-list', ':', 'file', 'family', 'style'], capture_output=True, text=True).stdout.splitlines():
    f = ln.split(':')[0]
    if f.lower().endswith(('.ttf', '.otf')) and any(k in ln for k in ['DejaVu Sans:', 'DejaVu Serif:', 'FreeSans', 'FreeSerif', 'Carlito', 'Inter:style=Regular', 'Inter:style=Bold', 'Caladea', 'Charter']) and 'Italic' not in ln.split('style=')[-1][:20]:
        fonts.append(f)
fonts = sorted(set(fonts))[:14]
OUT = os.environ.get('OUT','sheets')
GW, GH = 1600, 1200

def geom(nr, nc):
    zoneT, zoneB, zoneW = 160, 1118, GW-80
    cw = min(210, zoneW/(nc+1)); ch = min(135, (zoneB-zoneT)/(nr+1))
    gw, gh = cw*(nc+1), ch*(nr+1)
    return dict(gx=(GW-gw)/2, gy=zoneT+((zoneB-zoneT)-gh)/2, cw=cw, ch=ch, nr=nr, nc=nc)

def digit_img(style, d, rng, hpx):
    """ink float image of one digit, tight-cropped and scaled to height hpx"""
    if style == 'mnist':
        a = Xt[rng.choice(pool[d])].astype(np.float32)/255.
        a = cv2.resize(a, (112, 112), interpolation=cv2.INTER_CUBIC); a = np.clip(a, 0, 1)
        r = int(rng.integers(0, 4))
        if r: a = cv2.dilate(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*r+1, 2*r+1)))
    elif style == 'aug':
        i = rng.choice(pool[d]); _, a = augment(Xt[i], rng)
    else:  # fonts
        f = ImageFont.truetype(fonts[int(rng.integers(0, len(fonts)))], 200)
        im = Image.new('L', (300, 300), 0); dr = ImageDraw.Draw(im)
        dr.text((60, 20), str(d), fill=255, font=f, stroke_width=int(rng.integers(0, 6)), stroke_fill=255)
        a = np.array(im, np.float32)/255.
        ang = rng.uniform(-10, 10); sh = rng.uniform(-.25, .25)
        M = np.array([[1, sh, 0], [0, 1, 0]], np.float32); a = cv2.warpAffine(a, M, (300, 300))
        M = cv2.getRotationMatrix2D((150, 150), ang, 1); a = cv2.warpAffine(a, M, (300, 300))
    ys, xs = np.where(a > .1); a = a[ys.min():ys.max()+1, xs.min():xs.max()+1]
    k = hpx/a.shape[0]
    return cv2.resize(a, (max(2, int(round(a.shape[1]*k))), int(round(hpx))), interpolation=cv2.INTER_AREA)

def wrong_for(E, rng):
    v = int(E); opts = [v+1, v-1, v+2, v-2, v+10, v-10, v*2 % 150, int(str(v)[::-1])]
    opts = [o for o in opts if o >= 0 and o != v]
    return str(opts[int(rng.integers(0, len(opts)))])

def make_sheet(style, rng, nr, nc, rows, cols, p_wrong=.15):
    g = geom(nr, nc); A = np.zeros((GH, GW), np.float32); truth = []
    for r in range(nr):
        tr = []
        for c in range(nc):
            E = str(rows[r]*cols[c]); u = rng.random(); kind = 'right'; W_ = E
            if u < .03: kind, W_ = 'blank', ''
            elif u < .05: kind, W_ = 'scribble', E
            elif u < .05+p_wrong: kind, W_ = 'wrong', wrong_for(E, rng)
            x0 = g['gx']+(c+1)*g['cw']; y0 = g['gy']+(r+1)*g['ch']
            if kind != 'blank':
                hpx = g['ch']*rng.uniform(.45, .72) if len(W_) < 3 else g['ch']*rng.uniform(.42, .62)
                imgs = [digit_img(style, int(ch_), rng, hpx) for ch_ in W_]
                gaps = [int(rng.choice([-2, 1, 3, 5, 8, 12, 16], p=[.04, .1, .2, .22, .2, .14, .1])) for _ in imgs[1:]]
                tw = sum(i.shape[1] for i in imgs)+sum(gaps)
                if tw > g['cw']*.92:                       # shrink to fit if too wide
                    s = g['cw']*.92/tw; imgs = [cv2.resize(i, (max(2, int(i.shape[1]*s)), max(2, int(i.shape[0]*s)))) for i in imgs]
                    tw = sum(i.shape[1] for i in imgs)+sum(gaps)
                xs = x0+(g['cw']-tw)/2+rng.uniform(-.25, .25)*(g['cw']-tw); y_c = y0+g['ch']/2+rng.uniform(-6, 6)
                for k, im in enumerate(imgs):
                    yy = int(round(y_c-im.shape[0]/2+rng.uniform(-4, 4))); xx = int(round(xs))
                    xx = max(0, xx); yy = max(0, yy)
                    h_, w_ = im.shape; sub = A[yy:yy+h_, xx:xx+w_]; sub[:] = np.maximum(sub, im[:sub.shape[0], :sub.shape[1]])
                    xs += w_+(gaps[k] if k < len(gaps) else 0)
                if kind == 'scribble':
                    a = np.zeros((GH, GW), np.uint8)
                    for _ in range(int(rng.integers(1, 3))):
                        p1 = (int(x0+rng.uniform(5, g['cw']-5)), int(y0+rng.uniform(5, g['ch']-5))); p2 = (int(x0+rng.uniform(5, g['cw']-5)), int(y0+rng.uniform(5, g['ch']-5)))
                        cv2.line(a, p1, p2, 255, int(rng.integers(3, 8)), cv2.LINE_AA)
                    A = np.maximum(A, a.astype(np.float32)/255.)
            if rng.random() < .03:   # stray dot
                cv2.circle(A, (int(x0+rng.uniform(5, g['cw']-5)), int(y0+rng.uniform(5, g['ch']-5))), 3, 1.0, -1)
            tr.append(dict(E=E, written=W_, kind=kind))
        truth.append(tr)
    A = cv2.GaussianBlur(A, (0, 0), .8)
    rgba = np.zeros((GH, GW, 4), np.uint8); rgba[..., :3] = (30, 60, 200); rgba[..., 3] = np.clip(A*255*1.15, 0, 255).astype(np.uint8)
    return rgba, truth, g

if __name__ == '__main__':
    os.makedirs(OUT+'', exist_ok=True)
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
    n_per = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    meta = []
    for style in ['mnist', 'aug', 'font']:
        for k in range(n_per):
            nr, nc = [(10, 10), (10, 10), (8, 6), (12, 12), (10, 10), (6, 8)][k % 6]
            lo, hi = [(2, 12), (2, 12), (1, 9), (2, 12), (2, 12), (3, 10)][k % 6]
            rows = list(rng.permutation(np.arange(lo, hi+1))[:nr]) if hi-lo+1 >= nr else list(rng.integers(lo, hi+1, nr))
            cols = list(rng.permutation(np.arange(lo, hi+1))[:nc]) if hi-lo+1 >= nc else list(rng.integers(lo, hi+1, nc))
            rgba, truth, g = make_sheet(style, rng, nr, nc, [int(x) for x in rows], [int(x) for x in cols])
            name = f'{style}_{k}'; cv2.imwrite(f'{OUT}/{name}.png', cv2.cvtColor(rgba, cv2.COLOR_RGBA2BGRA))
            meta.append(dict(name=name, style=style, rows=[int(x) for x in rows], cols=[int(x) for x in cols], g=g, truth=truth))
    json.dump(meta, open(OUT+'/meta.json', 'w'))
    print(len(meta), OUT, len(fonts), 'fonts')
