import numpy as np, pickle, json, base64, sys
p = pickle.load(open('params.pkl','rb'))
out = {}
qp = {}
for k in ['c1','c2','c3','f1','f2']:
    w = p[k].astype(np.float32); q = np.abs(w).max()/127.
    qi = np.clip(np.round(w/q), -127, 127).astype(np.int8)
    out[k] = {'q': float(q), 'b': base64.b64encode(qi.tobytes()).decode()}
    qp[k] = qi.astype(np.float32)*q
for k in ['b1','b2','b3','g1','g2']:
    out[k] = {'b': base64.b64encode(p[k].astype(np.float32).tobytes()).decode()}
    qp[k] = p[k]
json.dump(out, open('net.json','w'), separators=(',',':'))
pickle.dump(qp, open('params_q.pkl','wb'))
print('net.json bytes', len(json.dumps(out, separators=(',',':'))))
