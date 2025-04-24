'''
Script to:
1. Retrieve all approved drugs from the ChEMBL database, sorted by approval year and name.
2. For each approved drug since 2019, retrieve associated UniProt accession numbers (protein targets).
3. For each UniProt accession, retrieve associated UniProt keywords.

Each major step logs progress and writes its own output file.

Requirements:
    pip install chembl_webresource_client requests
'''
import time as t
import json as j
import requests as r
from collections import defaultdict as dd
from chembl_webresource_client.new_client import new_client as nc

# Step 1
print("Step 1: Retrieving approved drugs...")
m=nc.molecule
i1=m.filter(max_phase=4).only(['molecule_chembl_id','pref_name','first_approval'])
a=[]
for i,x in enumerate(i1,1):
    y=x.get('first_approval')
    try: yr=int(y) if y else None
    except: yr=None
    a.append({'c':x['molecule_chembl_id'],'n':x.get('pref_name')or'','y':yr})
    if i%500==0: print(f"  Retrieved {i} items...")
s=sorted(a,key=lambda z:((z['y'] is None,z['y'] or 0),z['n']))
print(f"Total approved: {len(s)}")
with open('step1_approved.json','w') as f: j.dump(s,f,indent=2)
print('Step 1 output: step1_approved.json')

# Step 2
print("Step 2: Retrieving targets for drugs since 2019...")
me=nc.mechanism
ta=nc.target
d=dd(set)
r1=[z for z in s if z['y'] and z['y']>=2019]
print(f"Drugs >=2019: {len(r1)}")
for i,z in enumerate(r1,1):
    cid=z['c']; print(f"  ({i}/{len(r1)}) {cid}...")
    for m2 in me.filter(molecule_chembl_id=cid):
        tc=m2.get('target_chembl_id')
        if not tc: continue
        try: t2=ta.get(tc)
        except: continue
        if t2.get('target_type')!='SINGLE PROTEIN': continue
        for c2 in t2.get('target_components',[]):
            acc=c2.get('accession')
            if acc: d[cid].add(acc)
    t.sleep(0.5)
D={k:list(v) for k,v in d.items()}
with open('step2_accessions.json','w') as f: j.dump(D,f,indent=2)
print('Step 2 output: step2_accessions.json')

# Step 3
print("Step 3: Retrieving UniProt keywords...")
U='https://rest.uniprot.org/uniprotkb/'
def f_acc(ac):
    p=r.get(f"{U}{ac}.json",headers={'Accept':'application/json'});p.raise_for_status()
    return [k.get('name') for k in p.json().get('keywords',[])]
K=dd(dict)
aa=[(c2,ac) for c2,acs in D.items() for ac in acs]
print(f"Total acc: {len(aa)}")
for i,(c2,ac) in enumerate(aa,1):
    print(f"  ({i}/{len(aa)}) {ac}...")
    try: kw=f_acc(ac)
    except: kw=[]
    K[c2][ac]=kw
    t.sleep(0.5)
K_out={k:v for k,v in K.items()}
with open('step3_keywords.json','w') as f: j.dump(K_out,f,indent=2)
print('Step 3 output: step3_keywords.json')
print('All done.')
