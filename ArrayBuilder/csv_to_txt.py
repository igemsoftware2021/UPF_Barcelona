# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd

def save_seqset(seqset, name): 
    with open(name+".txt", 'w') as f:
        for seq in seqset:
            f.write("%s\n" % seq)     
            
            
r_mechanisms = ["phosphorylation","acetylation","nucleotidylation","efflux",
              "altered target","hydrolysis","reprogramming peptidoglycan biosynthesis",
              "ADP-ribosylation", "monooxygenation"]
              

p_mechanisms = ["conjugation","transformation"]

v_mechanisms = ["Adhesion","Toxin"]
              


              

phosphorylation = []
acetylation = []
nucleotidylation = []
efflux = []
altered_target = []
hydrolysis = []
reprogramming_peptidoglycan_biosynthesis = []
ADP_ribosylation = []
monooxygenation = []


conjugation = []
transformation = []


adhesion_based = []
toxin_based = []

r = pd.read_csv('resistance.csv')
r.itertuples()
r = r.values.tolist()

p = pd.read_csv('promiscuity.csv')
p.itertuples()
p = p.values.tolist()

v = pd.read_csv('virulence.csv')
v.itertuples()
v = v.values.tolist()

for i in range(len(r)):
    
    if r_mechanisms[0] in r[i][0]:
        
        phosphorylation.append(r[i][1])
        
    if r_mechanisms[1] in r[i][0]:
        
        acetylation.append(r[i][1])
        
    if r_mechanisms[2] in r[i][0]:
        
        nucleotidylation.append(r[i][1])
        
    if r_mechanisms[3] in r[i][0]:
        
        efflux.append(r[i][1])
        
    if r_mechanisms[4] in r[i][0]:
        
        altered_target.append(r[i][1])
        
    if r_mechanisms[5] in r[i][0]:
        
        hydrolysis.append(r[i][1])
        
    if r_mechanisms[6] in r[i][0]:
        
        reprogramming_peptidoglycan_biosynthesis.append(r[i][1])
        
    if r_mechanisms[7] in r[i][0]:
        
        ADP_ribosylation.append(r[i][1])
    
    if r_mechanisms[8] in r[i][0]:
        
        monooxygenation.append(r[i][1])



for i in range(len(p)):
    
    if p_mechanisms[0] in p[i][0]:
        
        conjugation.append(p[i][1])
        
    if p_mechanisms[1] in p[i][0]:
        
        transformation.append(p[i][1])
        
        
for i in range(len(v)):

    
    if v_mechanisms[0] in v[i][0]:
        
        adhesion_based.append(v[i][1])
        
    if v_mechanisms[1] in v[i][0]:
        
        toxin_based.append(v[i][1])
        
        
print(len(phosphorylation)) 
print(len(acetylation)) 
print(len(nucleotidylation)) 
print(len(efflux))
print(len(altered_target))
print(len(hydrolysis))
print(len(reprogramming_peptidoglycan_biosynthesis))
print(len(ADP_ribosylation))
print(len(monooxygenation))


print(len(conjugation))
print(len(transformation))


print(len(adhesion_based))
print(len(toxin_based))
        


save_seqset(phosphorylation, "data/resistance/phosphorylation")
save_seqset(acetylation, "data/resistance/acetylation")
save_seqset(nucleotidylation, "data/resistance/nucleotidylation")
save_seqset(efflux, "data/resistance/efflux")
save_seqset(altered_target, "data/resistance/altered target")
save_seqset(hydrolysis, "data/resistance/hydrolysis")
save_seqset(reprogramming_peptidoglycan_biosynthesis, "data/resistance/reprogramming peptidoglycan biosynthesis")
save_seqset(ADP_ribosylation, "data/resistance/ADP-ribosylation")
save_seqset(monooxygenation, "data/resistance/monooxygenation")

save_seqset(conjugation, "data/promiscuity/conjugation")
save_seqset(transformation, "data/promiscuity/transformation")
     
save_seqset(adhesion_based, "data/virulence/adhesion-based")
save_seqset(toxin_based, "data/virulence/toxin-based")
     
     