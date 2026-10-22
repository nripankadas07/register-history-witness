"""Check complete, small single-register histories against real-time precedence."""

def value(v):
    if v is None:return v
    if type(v) is int:return integer(v)
    if type(v) is str and len(v)<=128:return v
    raise ValueError('register value must be null, bounded integer or short string')

def analyze(data):
    obj(data,['initial','operations','state_limit'],['initial','operations']);initial=value(data['initial'])
    limit=integer(data.get('state_limit',100000),1,100000);ops=sequence(data['operations'],16);ids=set()
    for o in ops:
        if type(o) is not dict or o.get('kind') not in ('read','write','cas'):raise ValueError('unknown operation')
        keys=['id','client','start','end','kind']+({'read':['value'],'write':['value'],'cas':['expect','update','result']}[o['kind']])
        obj(o,keys);ident(o['id']);ident(o['client']);integer(o['start']);integer(o['end'])
        if o['id'] in ids or o['start']>=o['end']:raise ValueError('duplicate ID or nonpositive operation interval')
        ids.add(o['id'])
        for k in ('value','expect','update'):
            if k in o:value(o[k])
        if o['kind']=='cas' and type(o['result'])is not bool:raise ValueError('CAS result must be boolean')
    for i,a in enumerate(ops):
        for b in ops[i+1:]:
            if a['client']==b['client'] and max(a['start'],b['start'])<min(a['end'],b['end']):raise ValueError('overlapping operations for one client')
    n=len(ops);before=[sum(1<<j for j,b in enumerate(ops)if j!=i and b['end']<=a['start'])for i,a in enumerate(ops)]
    seen=set();deepest=[];witness=None
    class Budget(Exception):pass
    def search(mask,state,path):
        nonlocal deepest,witness
        if len(path)>len(deepest):deepest=path
        if mask==(1<<n)-1:witness=path;return True
        key=(mask,state)
        if key in seen:return False
        if len(seen)>=limit:raise Budget()
        seen.add(key)
        for i,o in enumerate(ops):
            if mask>>i&1 or before[i]&~mask:continue
            new=state
            if o['kind']=='read':
                if o['value']!=state:continue
            elif o['kind']=='write':new=o['value']
            else:
                succeeds=state==o['expect']
                if succeeds!=o['result']:continue
                if succeeds:new=o['update']
            if search(mask|1<<i,new,path+[o['id']]):return True
        return False
    try:status='LINEARIZABLE' if search(0,initial,[])else 'NOT_LINEARIZABLE'
    except Budget:status='UNKNOWN'
    return {'status':status,'linearization':witness,'deepest_prefix':deepest,'explored_states':len(seen),'state_limit':limit,
            'precedence':[{'before':ops[j]['id'],'after':ops[i]['id']}for i in range(n)for j in range(n)if before[i]>>j&1],
            'interpretation':'UNKNOWN is a resource bound, never a failed history. A deepest prefix alone is not a proof of impossibility.'}
import argparse, json, pathlib, sys

def obj(v, keys, required=None):
    if type(v) is not dict or set(v)-set(keys) or set(required if required is not None else keys)-set(v):
        raise ValueError('invalid object keys: '+str(keys))
    return v

def integer(v, low=-10**12, high=10**12):
    if type(v) is not int or not low<=v<=high: raise ValueError('integer outside supported range')
    return v

def ident(v):
    if type(v) is not str or not 1<=len(v)<=128: raise ValueError('identifier must be 1..128 characters')
    return v

def sequence(v, high):
    if type(v) is not list or len(v)>high: raise ValueError('invalid or oversized list')
    return v

def pairs(xs):
    d={}
    for k,v in xs:
        if k in d: raise ValueError('duplicate JSON key: '+k)
        d[k]=v
    return d

def read(path, limit):
    with open(path,'rb') as f: b=f.read(limit+1)
    if len(b)>limit: raise ValueError('input too large')
    return b

def load(path):
    return json.loads(read(path,1048576).decode('utf8'), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
    try: print(json.dumps(analyze(load(a.input)),ensure_ascii=True,indent=2));return 0
    except (ValueError,OSError,UnicodeError,RecursionError) as e:
        print(json.dumps({'error':str(e)}),file=sys.stderr);return 2

if __name__=="__main__": raise SystemExit(main())
