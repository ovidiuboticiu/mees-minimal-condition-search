"""
Generalized MEES v0.2 FROZEN methodological candidate.
Post-METHOD-3 repair only: preserve 140 structural queries and independently
confirm phase anchor before mapping the continuous phase region.
FROZEN before MEES-METHOD-4 world generation. Do not modify for held-out testing.
"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier

N_BITS=8
LEVELS=np.array([0.,.25,.5,.75,1.])
MAX_BUDGET=180
BINARY_TARGET=140
MAX_ANCHOR_CANDIDATES=5
ANCHOR_CONFIRM_BATCHES=(1,2,3)
ANCHOR_CONFIRM_MIN=2
PHASE_BATCH=4
MASKS=np.arange(256)
BITS=((MASKS[:,None]>>np.arange(N_BITS))&1).astype(np.int8)

def _antichain(passm):
    ps=set(int(x) for x in passm)
    out=[]
    for m in sorted(ps,key=lambda z:(int(z).bit_count(),z)):
        proper=False
        sub=(m-1)&m
        while sub:
            if sub in ps:
                proper=True; break
            sub=(sub-1)&m
        if not proper: out.append(m)
    return out

def _neighbors(mask):
    return [mask^(1<<b) for b in range(N_BITS)]

def run_generalized_mees_v02(query_fn, seed):
    """query_fn(mask, xi, yi, batch_id) -> binary observed outcome."""
    rng=np.random.default_rng(seed)
    cache={}
    order=[]
    def ask(mask,xi,yi,batch=0):
        key=(int(mask),int(xi),int(yi),int(batch))
        if key in cache: return cache[key]
        if len(order)>=MAX_BUDGET: raise RuntimeError('query budget exhausted')
        val=int(query_fn(*key))
        cache[key]=val; order.append(key)
        return val

    center=(2,2)
    queried=[]; y=[]; seen=set()
    for h in range(N_BITS+1):
        ms=MASKS[BITS.sum(axis=1)==h]
        for _ in range(min(3,len(ms))):
            m=int(rng.choice(ms))
            if m not in seen:
                seen.add(m); queried.append(m); y.append(ask(m,*center,0))
    while len(queried)<32:
        m=int(rng.integers(256))
        if m not in seen:
            seen.add(m); queried.append(m); y.append(ask(m,*center,0))

    while len(queried)<100:
        clf=RandomForestClassifier(n_estimators=180,min_samples_leaf=1,class_weight='balanced',
                                   random_state=100+seed,n_jobs=-1,max_depth=8)
        clf.fit(BITS[queried],y)
        proba=clf.predict_proba(BITS)
        uncertainty=np.ones(256) if len(clf.classes_)<2 else np.abs(proba[:,list(clf.classes_).index(1)]-.5)
        batch=[]
        positives=[m for m,v in zip(queried,y) if v==1]
        local=[]
        for pm in positives: local.extend(_neighbors(pm))
        rng.shuffle(local)
        for m in local:
            if m not in seen and m not in batch:
                batch.append(int(m))
                if len(batch)>=5: break
        for m in np.argsort(uncertainty):
            m=int(m)
            if m not in seen and m not in batch:
                batch.append(m)
                if len(batch)>=10: break
        for m in batch:
            seen.add(m); queried.append(m); y.append(ask(m,*center,0))
            if len(queried)>=100: break

    while len(queried)<BINARY_TARGET:
        clf=RandomForestClassifier(n_estimators=260,min_samples_leaf=1,class_weight='balanced',
                                   random_state=101+seed,n_jobs=-1,max_depth=10)
        clf.fit(BITS[queried],y)
        pred=clf.predict(BITS).astype(int)
        predicted_min=_antichain([m for m in MASKS if pred[m]==1])
        candidates=[]
        for pm in predicted_min:
            candidates.append(pm); candidates.extend(_neighbors(pm))
        for pm,v in zip(queried,y):
            if v==1: candidates.extend(_neighbors(pm))
        added=False
        for m in candidates:
            m=int(m)
            if m not in seen:
                seen.add(m); queried.append(m); y.append(ask(m,*center,0)); added=True
                if len(queried)>=BINARY_TARGET: break
        if not added:
            proba=clf.predict_proba(BITS)
            p=proba[:,list(clf.classes_).index(1)] if len(clf.classes_)==2 else np.full(256,.5)
            for m in np.argsort(np.abs(p-.5)):
                m=int(m)
                if m not in seen:
                    seen.add(m); queried.append(m); y.append(ask(m,*center,0)); added=True; break
        if not added: break

    clf=RandomForestClassifier(n_estimators=500,min_samples_leaf=1,class_weight='balanced',
                               random_state=102+seed,n_jobs=-1,max_depth=None)
    clf.fit(BITS[queried],y)
    binary_prediction=clf.predict(BITS).astype(np.int8)
    proba=clf.predict_proba(BITS)
    ppos=proba[:,list(clf.classes_).index(1)] if len(clf.classes_)==2 else np.zeros(256)

    observed_positive=sorted({m for m,v in zip(queried,y) if v==1},
                             key=lambda m:(-ppos[m],int(m).bit_count(),m))
    anchor=None; anchor_confirmations=[]
    for m in observed_positive[:MAX_ANCHOR_CANDIDATES]:
        vals=[ask(m,*center,b) for b in ANCHOR_CONFIRM_BATCHES]
        anchor_confirmations.append((int(m),vals))
        if sum(vals)>=ANCHOR_CONFIRM_MIN:
            anchor=int(m); break

    phase_region=np.zeros((5,5),dtype=np.int8)
    if anchor is not None:
        for xi in range(5):
            for yi in range(5):
                phase_region[xi,yi]=ask(anchor,xi,yi,PHASE_BATCH)

    return {
        'binary_prediction':binary_prediction,
        'phase_region':phase_region,
        'anchor_mask':anchor,
        'anchor_confirmations':anchor_confirmations,
        'query_count':len(order),
        'query_order':order,
        'structural_query_count':len(queried),
    }
