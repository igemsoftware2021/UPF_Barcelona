# -*- coding: utf-8 -*-

import os
import numpy as np
import sys
import math
import re
from collections import Counter

#The GC content of the guide sequence should be 40-80%. 
#High GC content stabilizes the RNA-DNA duplex while destabilizing off-target hybridization. 
#The length of the guide sequence should be between 17-24bp noting a shorter sequence minimizes 
#off-target effects. Guide sequences less than 17bp have a chance of targeting multiple loci.


class ARIABuilder():
    
     
     k = 20
    
     def preprocessing(seq1, seq2):
                 
            pass
        
     def kengine(seq1, seq2):
                 
            k = int(math.log((len(seq1)+len(seq2))/2,4))
            
            seq1 = seq1.lower()
            seq2 = seq2.lower()
          
            kmers1, kmers2 = re.compile("(?=(\w{%s}))" % k).findall(seq1), re.compile("(?=(\w{%s}))" % k).findall(seq2)
            
            freq1, freq2 = Counter(kmers1), Counter(kmers2)
            
            kmers = list(set(list(freq1.keys())) or set(list(freq2.keys())))
        
            vec1 = np.zeros((len(kmers),), dtype=int)
            vec2 = np.zeros((len(kmers),), dtype=int)
        
            for i in range(len(kmers)):
                vec1[i] = freq1[kmers[i]]
                vec2[i] = freq2[kmers[i]]
                
            return np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))*100
    
     def loadingBar(count,total,size):
        
        percent = float(count)/float(total)*100
        sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/"+str(int(total)).rjust(3,'0') + ' [' + '='*int(percent/10)*size + ' '*(10-int(percent/10))*size + ']') 
               
     def show_list(element_list):
         
         print("----------------------------------")
         for element in element_list:
             print(element)
             
     def show_dict(element_dict):
         
         print("----------------------------------")
         for key in element_dict.keys():
             print(key.upper()+": "+(", ".join(element_dict[key]))+".")
            
             
     def create_directory(path):
         
         if not os.path.exists(path):
             os.makedirs(path)
            
     
     def load_file(path):
         
         return open(path).read().splitlines()
            
    
     def load_tags():
         
          antibiotics = os.listdir("data/profiles")
          virulence_mechanisms = os.listdir("data/virulence")
          promiscuity_mechanisms = os.listdir("data/promiscuity")
          resistance_mechanisms = []
          antibiotic_profiles = {}
          
          for i in range(len(virulence_mechanisms)):
              
              virulence_mechanisms[i]=  virulence_mechanisms[i][:-4]
             
          for i in range(len(promiscuity_mechanisms)):
              
              promiscuity_mechanisms[i] = promiscuity_mechanisms[i][:-4]
          
          for i in range(len(antibiotics)):
              
              profile = ARIABuilder.load_file("data/profiles/"+antibiotics[i])
              
              antibiotic_profiles[antibiotics[i][:-4]] = profile
              
              for mechanism in profile:
                  
                  if mechanism not in resistance_mechanisms:
                      
                      resistance_mechanisms.append(mechanism)
              
             
            
          class_num = len(resistance_mechanisms)+len(virulence_mechanisms)+len(promiscuity_mechanisms)
          
          print("DATA")
          print(" ")
          print("Resistance Profiles per Antibiotic ("+str(len(antibiotics))+")")
          ARIABuilder.show_dict(antibiotic_profiles)
          print(" ")
          print("Resistance Mechanisms ("+str(len(resistance_mechanisms))+")")
          ARIABuilder.show_list(resistance_mechanisms)
          print(" ")
          print("Promiscuity Mechanisms  ("+str(len(promiscuity_mechanisms))+")")
          ARIABuilder.show_list(promiscuity_mechanisms)
          print(" ")
          print("Virulence Mechanisms  ("+str(len(virulence_mechanisms))+")")
          ARIABuilder.show_list(virulence_mechanisms)
          print(" ")
          print("Total amount of classes: ", str(class_num))
          print(" ")
          
          
          return resistance_mechanisms, promiscuity_mechanisms, virulence_mechanisms
          
          
     def load_sequences(r_classes, p_classes, v_classes):
         
          sequences = []
          
          for path in r_classes:
              
              sequences.append(ARIABuilder.load_file("data/resistance/"+path+".txt"))
              
          for path in p_classes:
              
              sequences.append(ARIABuilder.load_file("data/promiscuity/"+path+".txt"))
              
          for path in v_classes:
              
              sequences.append(ARIABuilder.load_file("data/virulence/"+path+".txt"))
    
              
          return sequences
      
        
     def filter_sequences(sequences):
        
 
         return sequences



     def generate_templates(seq):
         
     
         templates = []
         
         PAM_pos = []
             
         for i in re.finditer("ttta",seq):
             PAM_pos.append(i.start())
             
         for i in re.finditer("tttg",seq):
             PAM_pos.append(i.start())
             
         for i in re.finditer("tttc",seq):
             PAM_pos.append(i.start())
      
         for PAM in PAM_pos:
             
             try:
                 
                 templates.append(seq[PAM-1-ARIABuilder.k:PAM-1])
                 
             except Exception as e:
                
                 print(e)
                
                 
         return templates
            
             
             
     def create_candidates(sequence):
         
         
         COUNT = 0
         
         candidates = []
         for seqset in sequence:
             
             candidates_seqset = []
             
             for seq in seqset:
                
                 candidates_seqset.append(ARIABuilder.generate_templates(seq))
                 COUNT += len(ARIABuilder.generate_templates(seq))
                 
             candidates.append(candidates_seqset)
       
             
         print(COUNT)
        
         return candidates
     
     def score_candidate(candidate):
         
        #Mas score es
    
        weights = [
   
        (1,'g',-0.2753771),(2,'a',-0.3238875),(2,'c',0.17212887),(3,'c',-0.1006662),
        (4,'c',-0.2018029),(4,'g',0.24595663),(5,'a',0.03644004),(5,'c',0.09837684),
        (6,'c',-0.7411813),(6,'g',-0.3932644),(11,'a',-0.466099),(14,'a',0.08537695),
        (14,'c',-0.013814),(15,'a',0.27262051),(15,'c',-0.1190226),(15,'t',-0.2859442),
        (16,'a',0.09745459),(16,'g',-0.1755462),(17,'c',-0.3457955),(17,'g',-0.6780964),
        (18,'a',0.22508903),(18,'c',-0.5077941),(19,'g',-0.4173736),(19,'t',-0.054307),
        (20,'g',0.37989937),(20,'t',-0.0907126),(21,'c',0.05782332),(21,'t',-0.5305673),
        (22,'t',-0.8770074),(23,'c',-0.8762358),(23,'g',0.27891626),(23,'t',-0.4031022),
        (24,'a',-0.0773007),(24,'c',0.28793562),(24,'t',-0.2216372),(27,'g',-0.6890167),
        (27,'t',0.11787758),(28,'c',-0.1604453),(29,'g',0.38634258),(1,'gt',-0.6257787),
        (4,'gc',0.30004332),(5,'aa',-0.8348362),(5,'ta',0.76062777),(6,'gg',-0.4908167),
        (11,'gg',-1.5169074),(11,'ta',0.7092612),(11,'tc',0.49629861),(11,'tt',-0.5868739),
        (12,'gg',-0.3345637),(13,'ga',0.76384993),(13,'gc',-0.5370252),(16,'tg',-0.7981461),
        (18,'gg',-0.6668087),(18,'tc',0.35318325),(19,'cc',0.74807209),(19,'tg',-0.3672668),
        (20,'ac',0.56820913),(20,'cg',0.32907207),(20,'ga',-0.8364568),(20,'gg',-0.7822076),
        (21,'tc',-1.029693),(22,'cg',0.85619782),(22,'ct',-0.4632077),(23,'aa',-0.5794924),
        (23,'ag',0.64907554),(24,'ag',-0.0773007),(24,'cg',0.28793562),(24,'tg',-0.2216372),
        (26,'gt',0.11787758),(28,'gg',-0.69774) ]
    
         
        gc_weights = [-0.2026259,-0.1665878]
        
        spacer = candidate[4:24]
        
        gc = (spacer.count('c') + spacer.count('g'))/len(spacer)
           
        score =  0.59763615
    
        if gc == 0.5:
            w_gc = gc_weights[0]
        else:
            w_gc = gc_weights[round(gc)]
        
        score += abs(0.5-gc)*w_gc*len(spacer)
    
        for base, subkmer, w in weights:
            if candidate[base:base+len(subkmer)] == subkmer:
                score += w
                
        score = 1.0/(1.0+math.exp(-score))
                
        return 
         
        
     def filter_candidates(all_candidates):
         
         print("Filtering candidates")
         
         new_all_candidates = []

         COUNT = 0
         for seqset_candidates in all_candidates:
             
             new_seqset_candidates = []
             
             for seq_candidates in seqset_candidates:
                 
                 new_candidates = []
                 
                 for candidate in seq_candidates:
                     
                     gc = (candidate.count('c') + candidate.count('g')) / ARIABuilder.k
                     
                     if 0.4 < gc < 0.8:
                         
                         new_candidates.append(candidate)
                         COUNT += 1
                         
                 new_seqset_candidates.append(new_candidates)
                
             new_all_candidates.append(new_seqset_candidates)
             
         print(COUNT)
         
         return new_all_candidates
         
       
     def select_templates(templates):
         
         pass
     
     def construct_array(selected_templates, r_tags, p_tags, v_tags):
         
         pass
     
     def save_array(array):
         
         pass
         
         
         
          
if __name__ == "__main__":
    
    
    r_tags, p_tags, v_tags = ARIABuilder.load_tags()
    
    sequences = ARIABuilder.load_sequences(r_tags, p_tags, v_tags)
            
    filtered_sequences = ARIABuilder.filter_sequences(sequences)
    
    candidates = ARIABuilder.create_candidates(filtered_sequences)
       
    templates =  ARIABuilder.filter_candidates(candidates)
    
    selected_templates = ARIABuilder.select_templates(templates)
    
    array = ARIABuilder.construct_array(selected_templates, r_tags, p_tags, v_tags)
    
    ARIABuilder.save_array(array)
    

  
    
     
          
           
    