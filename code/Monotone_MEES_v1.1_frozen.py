
"""
Monotone MEES v1.1
Frozen before MEES-METHOD-6 world generation.

Change from v1.0:
- structural search remains the same class of causal subtraction/substitution search;
- phase mapping is decoupled from discovered minimal-set anchors;
- all 25 continuous cells are queried on the full binary design, guaranteed
  valid by the preregistered factorable monotone problem class;
- the monotone phase boundary is fit by minimum-disagreement dynamic programming.

Scope remains restricted to monotone/factorizable minimal-condition systems.
"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier

N_BITS=8
LEVELS=np.array([0.00,0.25,0.50,0.75,1.00])
MAX_BUDGET=180
MASKS=np.arange(256,dtype=int)
BITS=((MASKS[:,None]>>np.arange(N_BITS))&1).astype(np.int8)
CONFIGS=np.array([(m,xi,yi) for m in MASKS for xi in range(5) for yi in range(5)],dtype=int)
X_UNIVERSE=np.concatenate(
    [BITS[CONFIGS[:,0]],LEVELS[CONFIGS[:,1],None],LEVELS[CONFIGS[:,2],None]],
    axis=1
)

def mask_to_set(mask):
    return frozenset(np.where(BITS[int(mask)]==1)[0].tolist())

def antichain_minimal_masks(pass_masks):
    pset=set(int(m) for m in pass_masks)
    mins=[]
    for m in sorted(pset,key=lambda z:(int(z).bit_count(),z)):
        proper=False
        sub=(m-1)&m
        while sub:
            if sub in pset:
                proper=True
                break
            sub=(sub-1)&m
        if not proper:
            mins.append(m)
    return mins

def substitution_pairs_from_sets(minsets):
    ss=list(minsets)
    pairs=set()
    for i in range(len(ss)):
        for j in range(i+1,len(ss)):
            a,b=ss[i],ss[j]
            if len(a)==len(b) and len(a.symmetric_difference(b))==2:
                x=list(a-b)[0]
                y=list(b-a)[0]
                pairs.add(tuple(sorted((x,y))))
    return pairs

class Ledger:
    def __init__(self,query_fn,budget=MAX_BUDGET):
        self.query_fn=query_fn
        self.budget=budget
        self.cache={}
        self.order=[]
    def ask(self,mask,xi,yi):
        key=(int(mask),int(xi),int(yi))
        if key in self.cache:
            return self.cache[key]
        if len(self.order)>=self.budget:
            raise RuntimeError("query budget exhausted")
        val=int(self.query_fn(*key))
        self.cache[key]=val
        self.order.append(key)
        return val
    @property
    def n(self):
        return len(self.order)

def fit_monotone_boundary(obs):
    # obs[xi,yi] in {0,1}; threshold t_y in {0..5}.
    # Pattern is 0 below threshold, 1 at/above it.
    # Positive slope => threshold cannot increase with y.
    cost=np.zeros((5,6),dtype=int)
    for yi in range(5):
        for t in range(6):
            pred=np.array([0 if xi<t else 1 for xi in range(5)],dtype=int)
            cost[yi,t]=int(np.sum(pred!=obs[:,yi]))

    dp=np.full((5,6),10**9,dtype=int)
    parent=np.full((5,6),-1,dtype=int)
    dp[0]=cost[0]

    for yi in range(1,5):
        for t in range(6):
            candidates=range(t,6)  # previous threshold >= current
            best=None
            bestv=10**9
            for tp in candidates:
                v=dp[yi-1,tp]+cost[yi,t]
                if v<bestv:
                    bestv=v
                    best=tp
            dp[yi,t]=bestv
            parent[yi,t]=best

    t=int(np.argmin(dp[4]))
    out=[0]*5
    out[4]=t
    for yi in range(4,0,-1):
        out[yi-1]=int(parent[yi,out[yi]])
    return tuple(out)

def run_monotone_mees(query_fn,seed):
    rng=np.random.default_rng(seed)
    led=Ledger(query_fn)
    full=(1<<N_BITS)-1

    if led.ask(full,4,4)!=1:
        return {
            "minimal_sets":set(),
            "substitution_pairs":set(),
            "boundary":(5,5,5,5,5),
            "query_count":led.n,
            "status":"anchor_failed"
        }

    discovered=set()
    no_new=0
    attempts=0

    # Reserve 50 queries before substitution/phase stages.
    while led.n<MAX_BUDGET-50 and attempts<56 and no_new<14:
        attempts+=1
        m=full
        for bit in rng.permutation(N_BITS):
            bit=int(bit)
            if (m>>bit)&1:
                cand=m&~(1<<bit)
                if led.ask(cand,4,4)==1:
                    m=cand
        s=mask_to_set(m)
        if s in discovered:
            no_new+=1
        else:
            discovered.add(s)
            no_new=0

    substitution_pairs=set()
    for s in list(discovered):
        if led.n>=MAX_BUDGET-25:
            break
        base_mask=sum(1<<b for b in s)
        for old in list(s):
            for new in range(N_BITS):
                if new in s:
                    continue
                if led.n>=MAX_BUDGET-25:
                    break
                cand=(base_mask&~(1<<old))|(1<<new)
                if led.ask(cand,4,4)==1:
                    substitution_pairs.add(tuple(sorted((old,new))))
                    mm=cand
                    for bit in rng.permutation(N_BITS):
                        bit=int(bit)
                        if (mm>>bit)&1 and led.n<MAX_BUDGET-25:
                            cc=mm&~(1<<bit)
                            if led.ask(cc,4,4)==1:
                                mm=cc
                    discovered.add(mask_to_set(mm))

    substitution_pairs |= substitution_pairs_from_sets(discovered)

    # Full 5x5 phase map on the guaranteed-valid full binary design.
    obs=np.zeros((5,5),dtype=int)
    for xi in range(5):
        for yi in range(5):
            obs[xi,yi]=led.ask(full,xi,yi)
    boundary=fit_monotone_boundary(obs)

    return {
        "minimal_sets":discovered,
        "substitution_pairs":substitution_pairs,
        "boundary":boundary,
        "query_count":led.n,
        "status":"ok"
    }

# Frozen baseline definitions are retained from METHOD-5 for direct comparability.
def _fit_rf(indices,labels,seed,trees):
    clf=RandomForestClassifier(
        n_estimators=trees,min_samples_leaf=2,class_weight="balanced",
        random_state=seed,n_jobs=-1
    )
    clf.fit(X_UNIVERSE[np.asarray(indices,dtype=int)],np.asarray(labels,dtype=int))
    return clf

def run_uniform_grid(query_fn,seed):
    rng=np.random.default_rng(seed)
    led=Ledger(query_fn)
    chosen=rng.choice(len(CONFIGS),MAX_BUDGET,replace=False)
    y=[led.ask(*CONFIGS[i]) for i in chosen]
    clf=_fit_rf(chosen,y,seed+1,220)
    return {"ypred":clf.predict(X_UNIVERSE).astype(np.int8),"query_count":led.n}

def run_active_phase_only(query_fn,seed):
    rng=np.random.default_rng(seed)
    led=Ledger(query_fn)
    chosen=list(rng.choice(len(CONFIGS),40,replace=False))
    seen=set(chosen)
    y=[led.ask(*CONFIGS[i]) for i in chosen]
    while led.n<MAX_BUDGET:
        clf=_fit_rf(chosen,y,seed+2,140)
        prob=clf.predict_proba(X_UNIVERSE)
        if len(clf.classes_)<2:
            uncertainty=np.ones(len(CONFIGS))
        else:
            p=prob[:,list(clf.classes_).index(1)]
            uncertainty=np.abs(p-.5)
        batch=[]
        for ii in np.argsort(uncertainty):
            ii=int(ii)
            if ii not in seen:
                batch.append(ii)
                if len(batch)>=min(20,MAX_BUDGET-led.n):
                    break
        for ii in batch:
            chosen.append(ii)
            seen.add(ii)
            y.append(led.ask(*CONFIGS[ii]))
    clf=_fit_rf(chosen,y,seed+3,320)
    return {"ypred":clf.predict(X_UNIVERSE).astype(np.int8),"query_count":led.n}

def run_causal_ablation_only(query_fn,seed):
    led=Ledger(query_fn)
    full=(1<<N_BITS)-1
    boundary=[]
    for yi in range(5):
        idx=5
        for xi in range(5):
            if led.ask(full,xi,yi)==1:
                idx=xi
                break
        boundary.append(idx)
    necessary=set()
    if led.ask(full,4,4)==1:
        for bit in range(N_BITS):
            if led.ask(full&~(1<<bit),4,4)==0:
                necessary.add(bit)
    return {"necessary":necessary,"boundary":tuple(boundary),"query_count":led.n}
