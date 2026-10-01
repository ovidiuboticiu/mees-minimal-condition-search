"""
Generalized MEES v0.1
Frozen methodological algorithm.

Assumptions:
- 8 binary design variables.
- two continuous experimental axes, each with 5 levels.
- query_fn(mask, xi, yi) -> binary observed phenomenon outcome.
- a fixed reference slice (xi=2, yi=2) is used for binary structural search.
- binary and continuous effects are factorized in the final predictor.

The algorithm does NOT know the hidden causal formula.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier

N_BITS=8
LEVELS=np.array([0.,.25,.5,.75,1.])
MAX_BUDGET=180
BINARY_TARGET=140

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
                proper=True
                break
            sub=(sub-1)&m
        if not proper:
            out.append(m)
    return out

def _neighbors(mask):
    return [mask^(1<<b) for b in range(N_BITS)]

def run_generalized_mees(query_fn, seed):
    rng=np.random.default_rng(seed)
    cache={}
    order=[]

    def ask(mask,xi,yi):
        key=(int(mask),int(xi),int(yi))
        if key in cache:
            return cache[key]
        if len(order)>=MAX_BUDGET:
            raise RuntimeError("query budget exhausted")
        val=int(query_fn(*key))
        cache[key]=val
        order.append(key)
        return val

    center=(2,2)
    queried=[]
    y=[]
    seen=set()

    for h in range(N_BITS+1):
        ms=MASKS[BITS.sum(axis=1)==h]
        for _ in range(min(3,len(ms))):
            m=int(rng.choice(ms))
            if m not in seen:
                seen.add(m)
                queried.append(m)
                y.append(ask(m,*center))

    while len(queried)<32:
        m=int(rng.integers(256))
        if m not in seen:
            seen.add(m)
            queried.append(m)
            y.append(ask(m,*center))

    while len(queried)<100:
        clf=RandomForestClassifier(
            n_estimators=180,min_samples_leaf=1,class_weight="balanced",
            random_state=100+seed,n_jobs=-1,max_depth=8)
        clf.fit(BITS[queried],y)
        proba=clf.predict_proba(BITS)
        if len(clf.classes_)<2:
            uncertainty=np.ones(256)
        else:
            uncertainty=np.abs(proba[:,list(clf.classes_).index(1)]-.5)
        batch=[]
        positives=[m for m,v in zip(queried,y) if v==1]
        local=[]
        for pm in positives:
            local.extend(_neighbors(pm))
        rng.shuffle(local)
        for m in local:
            if m not in seen and m not in batch:
                batch.append(int(m))
                if len(batch)>=5:
                    break
        for m in np.argsort(uncertainty):
            m=int(m)
            if m not in seen and m not in batch:
                batch.append(m)
                if len(batch)>=10:
                    break
        for m in batch:
            seen.add(m)
            queried.append(m)
            y.append(ask(m,*center))
            if len(queried)>=100:
                break

    while len(queried)<BINARY_TARGET:
        clf=RandomForestClassifier(
            n_estimators=260,min_samples_leaf=1,class_weight="balanced",
            random_state=101+seed,n_jobs=-1,max_depth=10)
        clf.fit(BITS[queried],y)
        pred=clf.predict(BITS).astype(int)
        predicted_min=_antichain([m for m in MASKS if pred[m]==1])
        candidates=[]
        for pm in predicted_min:
            candidates.append(pm)
            candidates.extend(_neighbors(pm))
        for pm,v in zip(queried,y):
            if v==1:
                candidates.extend(_neighbors(pm))
        added=False
        for m in candidates:
            m=int(m)
            if m not in seen:
                seen.add(m)
                queried.append(m)
                y.append(ask(m,*center))
                added=True
                if len(queried)>=BINARY_TARGET:
                    break
        if not added:
            proba=clf.predict_proba(BITS)
            if len(clf.classes_)==2:
                p=proba[:,list(clf.classes_).index(1)]
            else:
                p=np.full(256,.5)
            for m in np.argsort(np.abs(p-.5)):
                m=int(m)
                if m not in seen:
                    seen.add(m)
                    queried.append(m)
                    y.append(ask(m,*center))
                    added=True
                    break
        if not added:
            break

    clf=RandomForestClassifier(
        n_estimators=500,min_samples_leaf=1,class_weight="balanced",
        random_state=102+seed,n_jobs=-1,max_depth=None)
    clf.fit(BITS[queried],y)
    binary_prediction=clf.predict(BITS).astype(np.int8)

    positives=[m for m,v in zip(queried,y) if v==1]
    if positives:
        anchor=min(positives,key=lambda m:(int(m).bit_count(),m))
    else:
        prob=clf.predict_proba(BITS)
        if len(clf.classes_)==2:
            anchor=int(np.argmax(prob[:,list(clf.classes_).index(1)]))
        else:
            anchor=255

    phase_region=np.zeros((5,5),dtype=np.int8)
    for xi in range(5):
        for yi in range(5):
            if len(order)<MAX_BUDGET:
                phase_region[xi,yi]=ask(anchor,xi,yi)

    return {
        "binary_prediction":binary_prediction,
        "phase_region":phase_region,
        "anchor_mask":anchor,
        "query_count":len(order),
        "query_order":order,
    }
