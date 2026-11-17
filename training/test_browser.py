import json, base64, sys, collections, time
from playwright.sync_api import sync_playwright
HTML = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/build/index.html'
SD = sys.argv[2] if len(sys.argv) > 2 else 'sheets'
meta = json.load(open(SD+'/meta.json'))
JS = """async ([b64, g, rows, cols]) => {
  const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode();
  const cv = document.createElement('canvas'); cv.width = 1600; cv.height = 1200; cv.getContext('2d').drawImage(img, 0, 0);
  const G = frenzyGeom(g.nr, g.nc);
  const geomOK = Math.abs(G.gx-g.gx)<1e-6 && Math.abs(G.gy-g.gy)<1e-6 && Math.abs(G.cw-g.cw)<1e-6 && Math.abs(G.ch-g.ch)<1e-6;
  const t0 = performance.now();
  const cells = fzReadSheet(cv, G);
  const ms = performance.now() - t0;
  const out = cells.map((row, r) => row.map((c, k) => { const v = fzVerdict(c, rows[r]*cols[k]); return [v.v, v.read, c.groups.length]; }));
  return {out, geomOK, ms};
}"""
res = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 900})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route('**/*unpkg*/**', lambda r: r.abort()); pg.route('**/cdnjs*/**', lambda r: r.abort())
    pg.goto('file://' + HTML)
    for m in meta:
        b64 = base64.b64encode(open(f"{SD}/{m['name']}.png", 'rb').read()).decode()
        r = pg.evaluate(JS, [b64, m['g'], m['rows'], m['cols']])
        assert r['geomOK'], 'geometry mismatch'
        res.append((m, r))
    b.close()
print('page errors:', errs[:3])
# ---- metrics ----
def summarise(rs, label):
    C = collections.Counter(); sheets = []
    for m, r in rs:
        okc = trueok = 0
        for i, row in enumerate(m['truth']):
            for j, t in enumerate(row):
                v, read, ng = r['out'][i][j]; correct = (t['kind'] == 'right')
                key = ('right' if correct else t['kind'], v); C[key] += 1
                trueok += correct; okc += (v == 'ok')
        sheets.append((trueok, okc))
    n_right = sum(C[('right', v)] for v in ['ok', '?', 'bad', 'blank'])
    n_wrong = sum(C[(k, v)] for k in ['wrong'] for v in ['ok', '?', 'bad', 'blank'])
    n_scr = sum(C[('scribble', v)] for v in ['ok', '?', 'bad', 'blank'])
    n_blank = sum(C[('blank', v)] for v in ['ok', '?', 'bad', 'blank'])
    print(f'\n=== {label}: {len(rs)} sheets, {sum(C.values())} boxes ({n_right} correctly answered, {n_wrong} wrong answers, {n_scr} crossed-out/scribbled, {n_blank} blank) ===')
    pct = lambda a, b: f'{100*a/max(1,b):5.1f}%'
    print(f"correct answers  -> ✓ {pct(C[('right','ok')],n_right)}   ? {pct(C[('right','?')],n_right)}   ✗(false) {pct(C[('right','bad')],n_right)}   blank(false) {pct(C[('right','blank')],n_right)}")
    print(f"wrong answers    -> ✗ {pct(C[('wrong','bad')],n_wrong)}   ? {pct(C[('wrong','?')],n_wrong)}   ✓(FALSE TICK) {pct(C[('wrong','ok')],n_wrong)}")
    print(f"scribbled        -> ✓(FALSE) {pct(C[('scribble','ok')],n_scr)}  ✗ {pct(C[('scribble','bad')],n_scr)}  ? {pct(C[('scribble','?')],n_scr)}  blank {pct(C[('scribble','blank')],n_scr)}")
    print(f"blank boxes      -> detected blank {pct(C[('blank','blank')],n_blank)}   (anything else: {n_blank-C[('blank','blank')]} boxes)")
    dec = C[('right','ok')]+C[('right','bad')]+C[('wrong','ok')]+C[('wrong','bad')]
    err = C[('right','bad')]+C[('wrong','ok')]
    print(f"of boxes it was confident about (✓ or ✗): {pct(dec-err,dec)} agreed with the truth ({err} of {dec} wrong)")
    diffs = [abs(a-b) for a, b in sheets]
    print(f"per-sheet score error if the teacher ignores every '?': avg {sum(diffs)/len(diffs):.1f}, worst {max(diffs)}  (out of {sum(len(m['truth'])*len(m['truth'][0]) for m,_ in rs)//len(rs)} boxes per sheet)")
    return C
for st in ['mnist', 'aug', 'font']:
    summarise([x for x in res if x[0]['style'] == st], {'mnist': 'Neat MNIST-style digits', 'aug': 'Kid-style (thick, slanted, wobbly)', 'font': 'Typed fonts (a different style the model never trained on)'}[st])
summarise(res, 'ALL')
print('\nmarking time per sheet (ms):', [round(r['ms']) for _, r in res][:6])
