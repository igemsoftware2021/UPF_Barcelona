# -*- coding: utf-8 -*-

#In order to work properly, ARIABuilder needs the following modules.
import os
import numpy as np
import sys
import math
import re
import pandas as pd
from Bio.Seq import Seq
import random


#This is the main class, which contains the required functions.
class ARIABuilder():
     
     """  
     This functions saves sequence sets in text files, 
     separating sequences with lines.
     """
     def save_seqset(seqset, name): 
        with open(name+".txt", 'w') as f:
            for seq in seqset:
                f.write("%s\n" % seq)     
    
     """
     This functions is intended to preprocess the information in the CSV 
     files and to convert it into a group of sequence sets for further processing.
     """
     def preprocessing():
         
        if not os.path.exists('data'):
           os.makedirs('data')
                 
               
        r = pd.read_csv('data/resistance.csv')
        r.itertuples()
        r = r.values.tolist()
        
        p = pd.read_csv('data/promiscuity.csv')
        p.itertuples()
        p = p.values.tolist()
        
        v = pd.read_csv('data/virulence.csv')
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
                    
        if not os.path.exists('sequences/resistance'):
            os.makedirs('sequences/resistance')
        if not os.path.exists('sequences/promiscuity'):
            os.makedirs('sequences/promiscuity')
        if not os.path.exists('sequences/virulence'):
            os.makedirs('sequences/virulence')
            
        for i in range(len(resistant)):
            ARIABuilder.save_seqset(resistant[i], "sequences/resistance/"+r_mechanisms[i])
           
        for i in range(len(promiscous)):
            ARIABuilder.save_seqset(promiscous[i], "sequences/promiscuity/"+p_mechanisms[i])
            
        for i in range(len(virulent)):
            ARIABuilder.save_seqset(virulent[i], "sequences/virulence/"+v_mechanisms[i])

     # A simple function to show sets in terminal.    
     def show_list(element_list):
         
         print("----------------------------------")
         for element in element_list:
             print(element)
      
     # A simple function to show sets of sets in the terminal.  
     def show_dict(element_dict):
         
         print("----------------------------------")
         for key in element_dict.keys():
             print(key.upper()+": "+(", ".join(element_dict[key]))+".")
            
             
     #A simple function to load lists from text files.
     def load_file(path):
         
         return open(path).read().splitlines()
                   
       
     """
     This function loads the annotations on the sequences to analyze once they have been
     properly preprocessed and organized with the previous functions.
     """
     def load_tags():
         
          antibiotics = os.listdir("data/profiles")
          virulence_mechanisms = os.listdir("sequences/virulence")
          promiscuity_mechanisms = os.listdir("sequences/promiscuity")
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
          
          print(" ")
          print(" > DATA LOADED")
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
          print(" ")
          
          
          return resistance_mechanisms, promiscuity_mechanisms, virulence_mechanisms, class_num
          
     """     
     Once the tags are received, they are used to load and classify the sequences of 
     interest, which will act as a base to create target templates.
     """
     def load_sequences(r_classes, p_classes, v_classes):
         
          sequences = []
          
          for path in r_classes:            
              sequences.append(ARIABuilder.load_file("sequences/resistance/"+path+".txt"))
              
          for path in p_classes:       
              sequences.append(ARIABuilder.load_file("sequences/promiscuity/"+path+".txt"))
              
          for path in v_classes:            
              sequences.append(ARIABuilder.load_file("sequences/virulence/"+path+".txt"))
    
          sequence_num = 0
          
          for sequence_set in sequences:
              
              sequence_num += len(sequence_set)
      
          print("Total amount of sequences: ", sequence_num)
          
          return sequences
      
     """
     With a starting pool of DNA sequences, the system must filter those 
     that will never work. This implies those, for instance, that do not
     have a properly defined PAM sequence, which is fundamental for the
     CRISPR/Cas system to act.
     """
     def filter_sequences(sequences):
         
          filtered_sequence_num = 0
          
          filtered_sequences = []
          
          for sequence_set in sequences:
              
              filtered_sequence_set = []
              
              for seq in sequence_set:
                  
                  if ("ttta" in seq) or ("tttg" in seq) or ("tttc" in seq):
                      
                      filtered_sequence_set.append(seq)
                      filtered_sequence_num += 1
                    
              filtered_sequences.append(filtered_sequence_set)
             
      
          print("Sequences with PAMs: ", filtered_sequence_num)
                  
          return filtered_sequences
           
     """
      This is the core function that creates potential target candidates
      from a single sequences. To do so, it finds the initial position of
      the PAMs found, and extracts 30 upstream bases: thus, this includes
      both the 20 nucleotides target template per se, and some contextual
      information that will use for effectivity calculation.
     """
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
             
             template = seq[PAM-31:PAM-1]
             
             if template != '':
                 templates.append(template)
                                                     
         return templates

     """        
     This is the bulk function that, using the previous one,
     computes for each sequence in the filtered pool the 
     target candidates. Moreover, it also filters those
     candidates that do not present a proper GC content 
     in the spacer-complement to promote their general stability.
     """
     def create_templates(sequences):
         
         
         template_num = 0
         checked_template_num = 0
         
         target_dictionaries = []
         
         templates = []
         for seqset in sequences:
             
             templates_seqset = []
             
             target_dictionary = {}
             
             for seq in seqset:
                
                 seq_templates = ARIABuilder.generate_templates(seq)
                 
                 template_num += len(seq_templates)
                 
                 checked_seq_templates = []
                 
                 for template in seq_templates:
         
                     target = template[4:24]
                
                     gc = (target.count('c') + target.count('g'))/len(target)
                     
                     if 0.4 < gc < 0.8:
                         
                         checked_seq_templates.append(template)
                         checked_template_num += 1
                         target_dictionary[template] = seq
                     
                 if checked_seq_templates != []:
                      templates_seqset.append(checked_seq_templates)
                        
             templates.append(templates_seqset)
             target_dictionaries.append(target_dictionary)
       
             
         print("Templates generated: ",template_num)
         print("Checked templates: ", checked_template_num)
        
         return templates, target_dictionaries
     
     """
     This is the core function capable of evaluating a target template 
     future effectivity by looking at the sequence structure per se,
     but also contemplating the non-linear interactions of adyacent bases.
     To do so, it implements the mathematical function that Doench et al 
     produced with a logistic classifier, and incorporates the weights they
     provided in the Supplementary Table 9 of their paper
     Rational design of highly active sgRNAs for CRISPR-Cas9-mediated gene inactivation
     """
       
     def score_template(template):
                  
        seq_weights = [
  
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
           
        score =  0.59763615
                 
        target = template[4:24]
        
        gc = (target.count('c') + target.count('g'))/len(target)
        
        if gc == 0.5:
            w_gc = gc_weights[0]
        else:
            w_gc = gc_weights[round(gc)]
        
        score += abs(0.5-gc)*w_gc*len(target)
    
        for base, subkmer, w in seq_weights:
            if template[base:base+len(subkmer)] == subkmer:
                score += w
                
        score = 1.0/(1.0+math.exp(-score))
                
        return score
    
    
     """
     This is the bulk function that applies the previous one
     to all the templates produced. The idea is to leave only
     the best target template for each sequence, so there is
     one possibility per surviving marker.
     """
     def filter_templates(templates):
         
          filtered_template_num = 0
          
          filtered_templates = []
          
          for sequence_set in templates:
              
              filtered_templates_sequence_set = []
              
              for templates_seq in sequence_set:

                    scores = [0]*len(templates_seq)
                    
                    for i in range(len(templates_seq)):
                        
                        scores[i] = ARIABuilder.score_template(templates_seq[i])
       
                    template = templates_seq[scores.index(max(scores))]
                    filtered_templates_sequence_set.append(template)
                    filtered_template_num += 1
                    
              filtered_templates.append(filtered_templates_sequence_set)
             
      
          print("Filtered templates: ", filtered_template_num)
                  
          return filtered_templates
        
     """
     Once each sequence shows only one potential template,
     this function is used to select the Nth best candidates
     for each of the classes.
     """
            
     def select_templates(filtered_templates, N):
                  
          selected_template_num = 0
          
          selected_templates = []
          
          for i in range(len(filtered_templates)):
              
              score = [0]*len(filtered_templates[i])
              
              for j in range(len(filtered_templates[i])):
                  
                  score[j] = ARIABuilder.score_template(filtered_templates[i][j])
                  
              best_template_index = sorted(range(len(score)), key=lambda x: score[x])[-N:]
              
              selected_templates_for_class = []
              
              for index in best_template_index:
                  
                  selected_templates_for_class.append(filtered_templates[i][index])
              
              selected_templates.append(selected_templates_for_class)
              selected_template_num += len(selected_templates_for_class)
                  
 
          print("Selected templates: ", selected_template_num)   
          
          return selected_templates
      
      """
      With the proper templates selected, now this function 
      produced the array design by making their complement,
      transcribing them to RNA and coupling them with their marker.
      This process is repeated for each teamplate in each row,
      so in the end N^2 RNA spacer templates.
      """
     def create_biosensor_array(selected_templates, sequences, target_dictionaries):
         
          print(" ")
          print("Computing complements and transcribing...")
          print("Creating biosensor array...")
         
          biosensor_array = []
          
          for i in range(len(selected_templates)):
              
              array_row = []
              
              for j in range(len(selected_templates)):
              
                  complementary = Seq(selected_templates[i][j]).complement()
                  spacerRNA = complementary.transcribe()
                  array_row.append([spacerRNA, target_dictionaries[i][selected_templates[i][j]]])
              
              random.shuffle(array_row)   
              biosensor_array.append(array_row)
              
              
          return biosensor_array
      
      
     """
     This last function takes the array design, and it simply saves
     it as a text file explaining which position is requiered for 
     each biosensor, and what are the sequences involved.
     """
     def save_array(biosensor_array, r_tags, p_tags, v_tags):
         
          m_tags = r_tags+p_tags+v_tags
          print(" ")
          print("Saving biosensor array design...")
         
          design_instructions = []
          
          design_instructions.append("")
          design_instructions.append("B I O S E N S O R   A R R A Y   D E S I G N")
          design_instructions.append("___________________________________________")
          design_instructions.append("")
          
          for i in range(len(biosensor_array)):
              
              class_label = "Spacer Templates for "+m_tags[i]+" markers."
              
              design_instructions.append(class_label)
              design_instructions.append("-------------------------------------------")
              design_instructions.append("")
              
              for j in range(len(biosensor_array)):
                  
                  tag = "Row: "+str(i)+" Columm:"+str(j)
                  content = "RNA Spacer Template: "+ biosensor_array[i][j][0]
                  reference = "Target Marker: "+ biosensor_array[i][j][1]
                  
                  design_instructions.append(tag)
                  design_instructions.append(content)
                  design_instructions.append(reference)
                  design_instructions.append("")
                  
                  
                
          ARIABuilder.save_seqset(design_instructions, "biosensor_array_design")
                  
  
"""
This is the worfklow of the entire system.

1. Data is preprocessed and preparated.
2. Sequence pool is loaded from the previously generated files.
3. Sequences are filtered searching for PAM motifs.
4. Target templates for each sequence are generated.
5. The target templates are filtered by effectivity, leaving one per sequences.
6. The remaining templates are subjected to a selection process, so the Nth best of each class are selected.
7. The information provided is used to design the biosensors' spacers.
8. The design is saved in a txt file.
"""
          
if __name__ == "__main__":
       

    ARIABuilder.preprocessing()
    
    r_tags, p_tags, v_tags, N = ARIABuilder.load_tags()
    
    sequences = ARIABuilder.load_sequences(r_tags, p_tags, v_tags)
            
    filtered_sequences = ARIABuilder.filter_sequences(sequences)
    
    templates, target_dictionaries = ARIABuilder.create_templates(filtered_sequences)
    
    filtered_templates = ARIABuilder.filter_templates(templates)
    
    selected_templates = ARIABuilder.select_templates(filtered_templates, N)
        
    array_design = ARIABuilder.create_biosensor_array(selected_templates, sequences, target_dictionaries)
    
    ARIABuilder.save_array(array_design, r_tags, p_tags, v_tags)
    
    input("Press any key to close")
        
    
    

  
    
     
          
           
    
