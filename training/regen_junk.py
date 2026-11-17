import numpy as np
from common import *
d=np.load('data.npz'); Xtr,ytr,Xte,yte,Xm,ym=[d[k] for k in ['Xtr','ytr','Xte','yte','Xm','ym']]
m=np.load('mnist.npz'); X,Xt=m['X'],m['Xt']
def mk(Xs,n,seed):
    r=np.random.default_rng(seed); out=[]
    while len(out)<n:
        im=junk(Xs,r)
        if im is not None: out.append(im)
    return (np.clip(np.stack(out),0,1)*255).astype(np.uint8)
keep=ytr!=10; Xtr2=np.concatenate([Xtr[keep],mk(X,50000,11)]); ytr2=np.concatenate([ytr[keep],np.full(50000,10,np.uint8)])
keep=yte!=10; Xte2=np.concatenate([Xte[keep],mk(Xt,1500,12)]); yte2=np.concatenate([yte[keep],np.full(1500,10,np.uint8)])
np.savez_compressed('data.npz',Xtr=Xtr2,ytr=ytr2,Xte=Xte2,yte=yte2,Xm=Xm,ym=ym)
print(Xtr2.shape,np.bincount(ytr2))
