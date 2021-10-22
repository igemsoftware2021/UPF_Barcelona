# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd


#if not os.path.exists(output_path):
#           os.makedirs(output_path)
            
def save_seqset(seqset, name): 
    with open(name+".txt", 'w') as f:
        for seq in seqset:
            f.write("%s\n" % seq)     
            
            
r = pd.read_csv('resistance.csv')
r.itertuples()
r = r.values.tolist()

p = pd.read_csv('promiscuity.csv')
p.itertuples()
p = p.values.tolist()

v = pd.read_csv('virulence.csv')
v.itertuples()
v = v.values.tolist()

r_mechanisms = []
p_mechanisms = []
v_mechanisms = []

for i in range(len(r)):
    mechanisms = r[i][0].split(":")
    for m in mechanisms:
        if m not in r_mechanisms:     
            r_mechanisms.append(m)
        
for i in range(len(p)):
    mechanisms = p[i][0].split(":")
    for m in mechanisms:
        if m not in p_mechanisms:     
            p_mechanisms.append(m)
            
for i in range(len(v)):
    mechanisms = v[i][0].split(":")
    for m in mechanisms:
        if m not in v_mechanisms:     
            v_mechanisms.append(m)
              
            
resistant = []
promiscous = []
virulent = []

for i in range(len(r_mechanisms)):
    resistant.append([])
    
for i in range(len(p_mechanisms)):
    promiscous.append([])
    
for i in range(len(v_mechanisms)):
    virulent.append([])
    
print(len(resistant))
print(len(r_mechanisms))


for i in range(len(r)):
    
    for j in range(len(r_mechanisms)):
        
        if r_mechanisms[j] in r[i][0]:
            
            resistant[j].append(r[i][1])
            
            
for i in range(len(p)):
    
    for j in range(len(p_mechanisms)):
        
        if p_mechanisms[j] in p[i][0]:
            
            promiscous[j].append(p[i][1])
            
for i in range(len(v)):
    
    for j in range(len(v_mechanisms)):
        
        if v_mechanisms[j] in v[i][0]:
            
            virulent[j].append(r[i][1])
            
for i in range(len(resistant)):
    print(len(resistant[i]))
 
for i in range(len(promiscous)):
    print(len(promiscous[i]))
    
for i in range(len(virulent)):
    print(len(virulent[i]))           



# save_seqset(phosphorylation, "data/resistance/phosphorylation")
# save_seqset(acetylation, "data/resistance/acetylation")
# save_seqset(nucleotidylation, "data/resistance/nucleotidylation")
# save_seqset(efflux, "data/resistance/efflux")
# save_seqset(altered_target, "data/resistance/altered target")
# save_seqset(hydrolysis, "data/resistance/hydrolysis")
# save_seqset(reprogramming_peptidoglycan_biosynthesis, "data/resistance/reprogramming peptidoglycan biosynthesis")
# save_seqset(ADP_ribosylation, "data/resistance/ADP-ribosylation")
# save_seqset(monooxygenation, "data/resistance/monooxygenation")

# save_seqset(conjugation, "data/promiscuity/conjugation")
# save_seqset(transformation, "data/promiscuity/transformation")
     
# save_seqset(adhesion_based, "data/virulence/adhesion-based")
# save_seqset(toxin_based, "data/virulence/toxin-based")
     
     