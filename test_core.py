import itertools,unittest
from register_history_witness import analyze

def op(i,k,start,end,**kw):return dict(id=str(i),client=str(i),kind=k,start=start,end=end,**kw)
def oracle(ops,initial):
    for perm in itertools.permutations(ops):
        order={o['id']:i for i,o in enumerate(perm)}
        if any(a['end']<=b['start'] and order[a['id']]>order[b['id']] for a in ops for b in ops if a!=b):continue
        state=initial;ok=True
        for o in perm:
            if o['kind']=='write':state=o['value']
            elif o['kind']=='read':ok &=state==o['value']
            else:
                match=state==o['expect'];ok &=match==o['result']
                if match:state=o['update']
        if ok:return True
    return False

class Histories(unittest.TestCase):
    def test_exhaustive_small_histories_agree_with_permutations(self):
        for a,b in itertools.product(range(3),repeat=2):
            for concurrent in [False,True]:
                ops=[op(0,'write',0,3,value=1),op(1,'write',1,4,value=2),op(2,'read',2 if concurrent else 5,6,value=a),op(3,'read',3 if concurrent else 7,8,value=b)]
                r=analyze({'initial':0,'operations':ops});self.assertEqual(r['status']=='LINEARIZABLE',oracle(ops,0))
                if r['linearization']is not None:self.assertEqual(set(r['linearization']),set(o['id']for o in ops))
    def test_stale_read_after_completed_write_fails(self):
        r=analyze({'initial':0,'operations':[op(1,'write',0,1,value=1),op(2,'read',1,2,value=0)]})
        self.assertEqual(r['status'],'NOT_LINEARIZABLE');self.assertIsNone(r['linearization'])
        self.assertEqual(r['precedence'],[{'before':'1','after':'2'}])
    def test_overlapping_write_can_linearize_after_read(self):
        r=analyze({'initial':0,'operations':[op(1,'write',0,10,value=1),op(2,'read',1,2,value=0)]})
        self.assertEqual(r['linearization'],['2','1'])
    def test_compare_and_swap_success_failure_and_null(self):
        ops=[op(1,'cas',0,1,expect=None,update='x',result=True),op(2,'cas',1,2,expect=None,update='y',result=False),op(3,'read',2,3,value='x')]
        self.assertEqual(analyze({'initial':None,'operations':ops})['status'],'LINEARIZABLE')
        ops[1]['result']=True;self.assertEqual(analyze({'initial':None,'operations':ops})['status'],'NOT_LINEARIZABLE')
    def test_budget_exhaustion_is_unknown(self):
        r=analyze({'initial':0,'state_limit':1,'operations':[op(1,'write',0,1,value=1),op(2,'read',1,2,value=1)]})
        self.assertEqual(r['status'],'UNKNOWN');self.assertIsNone(r['linearization'])
    def test_reject_invalid_or_incomplete_histories(self):
        bad=[{'initial':True,'operations':[]},{'initial':0,'operations':[op(1,'read',0,0,value=0)]},{'initial':0,'operations':[op(1,'read',0,2,value=0),dict(op(2,'write',1,3,value=1),client='1')]},{'initial':0,'operations':[dict(op(1,'write',0,1,value=1),pending=True)]}]
        for d in bad:
            with self.assertRaises(ValueError):analyze(d)
    def test_empty_history(self):self.assertEqual(analyze({'initial':0,'operations':[]})['linearization'],[])

if __name__=='__main__':unittest.main()
