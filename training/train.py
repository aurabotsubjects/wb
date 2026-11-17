import numpy as np, jax, jax.numpy as jnp, optax, time, pickle
d = np.load('data.npz')
Xtr, ytr, Xte, yte, Xm, ym = [d[k] for k in ['Xtr','ytr','Xte','yte','Xm','ym']]
print(Xtr.shape, flush=True)
def he(k, shape, fan): return jax.random.normal(k, shape)*np.sqrt(2./fan)
def init(key):
    k = jax.random.split(key, 5)
    return dict(
      c1=he(k[0], (3,3,1,16), 9),     b1=jnp.zeros(16),
      c2=he(k[1], (3,3,16,32), 144),  b2=jnp.zeros(32),
      c3=he(k[2], (3,3,32,48), 288),  b3=jnp.zeros(48),
      f1=he(k[3], (432,64), 432),     g1=jnp.zeros(64),
      f2=he(k[4], (64,11), 64),       g2=jnp.zeros(11))
def conv(x, w, b): return jax.lax.conv_general_dilated(x, w, (1,1), 'VALID', dimension_numbers=('NHWC','HWIO','NHWC'))+b
def pool(x): return jax.lax.reduce_window(x, -jnp.inf, jax.lax.max, (1,2,2,1), (1,2,2,1), 'VALID')
def fwd(p, x, key=None):
    x = jax.nn.relu(conv(x, p['c1'], p['b1']))      # 26
    x = pool(x)                                     # 13
    x = jax.nn.relu(conv(x, p['c2'], p['b2']))      # 11
    x = pool(x)                                     # 5
    x = jax.nn.relu(conv(x, p['c3'], p['b3']))      # 3
    x = x.reshape(x.shape[0], -1)                   # 432
    x = jax.nn.relu(x@p['f1']+p['g1'])
    if key is not None: x = x*jax.random.bernoulli(key, .8, x.shape)/.8
    return x@p['f2']+p['g2']
def loss(p, x, y, key):
    lg = fwd(p, x, key); oh = jax.nn.one_hot(y, 11)*.95+.05/11
    return optax.softmax_cross_entropy(lg, oh).mean()
EP, BS = 10, 256
steps = EP*(len(Xtr)//BS)
opt = optax.adamw(optax.cosine_decay_schedule(2.5e-3, steps), weight_decay=1e-4)
p = init(jax.random.PRNGKey(0)); st = opt.init(p)
@jax.jit
def step(p, st, x, y, key):
    l, g = jax.value_and_grad(loss)(p, x, y, key); u, st = opt.update(g, st, p); return optax.apply_updates(p, u), st, l
pred = jax.jit(lambda p, x: fwd(p, x))
def evalp(p, X, Y):
    out = []
    for i in range(0, len(X), 2000): out.append(np.array(pred(p, jnp.asarray(X[i:i+2000,:,:,None]/255.))))
    lg = np.concatenate(out); return (lg.argmax(1) == Y).mean(), lg
rng = np.random.default_rng(0); key = jax.random.PRNGKey(1); t0 = time.time()
for ep in range(EP):
    idx = rng.permutation(len(Xtr)); tot = 0
    for i in range(len(Xtr)//BS):
        b = idx[i*BS:(i+1)*BS]; key, k = jax.random.split(key)
        p, st, l = step(p, st, jnp.asarray(Xtr[b,:,:,None]/255.), jnp.asarray(ytr[b]), k); tot += float(l)
    a1,_ = evalp(p, Xte, yte); a2,_ = evalp(p, Xm, ym)
    print(f'ep {ep} loss {tot/(len(Xtr)//BS):.4f} augTest {a1:.4f} mnistTest {a2:.4f} t {time.time()-t0:.0f}s', flush=True)
    pickle.dump({k: np.array(v) for k, v in p.items()}, open('params.pkl', 'wb'))
