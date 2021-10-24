import os
import sys
import re
from collections import Counter
import math
import numpy as np
import pandas as pd
from Bio import SeqIO
import pyrodigal

class AlphaMine():
    
    sim_thresh = 70
    len_margin = 0.1
    active = True
    
    def start():
        
        print("\n")
        print("       >  A L P H A   M I N E  <        ")
        print("________________________________________")
        print(" ")
        print("        Pangenomic Analysis Tool        ")
        print("----------------------------------------")
        print("\n")
        print("Welcome to AlphaMine!")
        print("\n")
        print("Type 'help' to see available commands")

        
        while AlphaMine.active:
            
            command = input()
            
            if command == "preprocess_AMR_data":
                
                AlphaMine.Commands.preprocess_AMR_data()
            
            if command == "find_pangenome":
                
                AlphaMine.Commands.find_pangenome()
           
            elif command == "find_resistome":
                
                AlphaMine.Commands.find_resistome()
                
            elif command == "help":
 
                AlphaMine.Commands.show_help()
                
            elif command == "stop":
                
                AlphaMine.active = False
                
            else:
                
                print("Unknown instruction")
                print("Type 'help' to see available commands")
            
          
    
    def loadingBar(count,total,size):
        
        percent = float(count)/float(total)*100
        sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/"+str(int(total)).rjust(3,'0') + ' [' + '='*int(percent/10)*size + ' '*(10-int(percent/10))*size + ']') 
        
    def save_seqset(seqset, name):
        
        with open(name+".txt", 'w') as f:
            for seq in seqset:
                f.write("%s\n" % seq)        
                  
    def preprocess():
        
        AlphaMine.Preprocessor.generate_seq_library()
            
    def pangenomize(genomes_path, pangenome_type):
        
        files = os.listdir(genomes_path)
                
        seq_paths = []
        seq_files = []
        
        for i in range(len(files)):
            
            if "seq" in files[i]:
                
                seq_files.append(files[i])
        
        for i in range(len(seq_files)):
            
              seq_paths.append(genomes_path+"/"+seq_files[i])
            
        print("")
        print("...")
        print("")
          
        print("Sending genome collection to pangee")
        
        print("")
        print("...")
        print("")
        
        pangenome = AlphaMine.Pangee.compute_pangenome(seq_paths, 
                                                       AlphaMine.sim_thresh, 
                                                       pangenome_type, 
                                                       AlphaMine.len_margin)
        
        return pangenome
        
    
        
    class Commands():
        
        def show_help():
            
            print("\n")
            print("preprocess_AMR_data")
            print("--------------------------------------")
            print("Use the raw FASTA files in 'data' directory to generate a sequence set library,")
            print("Needs: a 'genomes' subdirectory with the FASTA files. ")
            print(" > A 'genomes' subdirectory with the FASTA files. ")
            print(" > A 'genome_index' CSV file with FASTA file IDs and resistant/susceptible tags. ")
            print("Analyzes the data, filters the sequences to be exclusive and saves the results.")
            print("The result will be found in separate folders, r_genomes and s_genomes.")
            
            print("\n")
            print("find_pangenome: genome_path, pangenome_type")
            print("--------------------------------------")
            print("Constructs a pangenome for a collection of sequence sets.")
            print("Type 0 means core pangenome (set intersection).")
            print("Type 1 means complete pangenome (set union).")
            print("Constructs a pangenome for a collection of genomes.")
            print("Saves the result in a txt file.")
            
            print("\n")
            print("find_resistome")
            print("--------------------------------------")
            print("If there is a preprocessed collection of both resistant and susceptible genomes,")
            print("computes the resistome by subtracting their two pangenomes.")
            print("Saves the result in a txt file.")
            print("\n")
            
            
        def preprocess_AMR_data():
            
            try:
             
                 AlphaMine.preprocess()
                 
                 AlphaMine.start()
                 
            except Exception as e: 
                
                print("Sorry, there was a problem with the previous command...")
                print(e)
                
        def find_pangenome():
        
            try:
             
                 genomes_path = input("Genomes path? ")
                  
                 pangenome_type = input("Pangenome type? 0 for core, 1 for complete. ")
                 
                 pangenome = AlphaMine.pangenomize(genomes_path, pangenome_type)
                 
                 AlphaMine.save_seqset(pangenome, "pangenome")
                 
                 AlphaMine.start()
                 
            except Exception as e: 
                
                print("Sorry, there was a problem with the previous command...")
                print(e)
            
                 
        def find_resistome():
            
             try:
             
                resistant_pangenome = AlphaMine.pangenomize("r_genomes", 0)
                # susceptible_pangenome = AlphaMine.find_pangenome("s_genomes", 0)
                
                AlphaMine.save_seqset(resistant_pangenome, "resistant_pangenome")
                # AlphaMine.save_seqset(susceptible_pangenome, "susceptible_pangenome")
                
                print("Resistome computed!")
                
                AlphaMine.start()
                 
             except Exception as e:
                 
                print("Sorry, there was a problem with the previous command...")
                print(e)
        
    
        
    
    class Preprocessor():
        
        def fasta_to_seqset(filename, input_path, output_path, index):
            
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            
            try:
                
                path = input_path +  "/" + filename + "/" + filename +'.fna'
                
                files = open(path)
                fasta_sequences = SeqIO.parse(files,'fasta')
                seqlist = ''
                
                for fasta in fasta_sequences:
                    _, sequence =  fasta.id, str(fasta.seq)
                    seqlist = seqlist + sequence
                files.close()
                    
                genome = seqlist
                
            except FileNotFoundError:
                  
                pass
                
            if len(genome) > 20000:
                      
                pyro = pyrodigal.Pyrodigal()
                pyro.train(genome)
                genes = pyro.find_genes(genome)
                
                gene_seq_list = []
                gene_pos_list = []
            
                total_length = 0
        
                for gene in genes:
                    gene_seq_list.append(genome[gene.begin-1:gene.end-1])
                    gene_pos_list.append([gene.begin,gene.end])
                    total_length += len(genome[gene.begin-1:gene.end-1])  
                
                with open(output_path+str(index)+"seq"+".txt", 'w') as f:
                    for seq in gene_seq_list:
                        f.write("%s\n" % seq)
                        
                index += 1
                        
            else: 
                
                pass
             
                  
            return index
        
        
        def generate_seq_library():
            
            g_path = 'data/genomes'
            
            g_list = os.listdir(g_path)
            
            b = pd.read_csv('genome_index.csv')
            b.itertuples()
            b = b.values.tolist()
            
            b_list = []
            
            antibiotics = []
            antibiotics_genomes_S = []
            antibiotics_genomes_R = []
            
            for i in range(len(b)):
                
               if b[i][3] not in antibiotics:
                   
                   antibiotics.append(b[i][3])
            
            
            
            for i in range(len(antibiotics)):
                
                antibiotics_genomes_S.append([])
                antibiotics_genomes_R.append([])
            
            for i in range(len(b)):
                
               b_list.append(str(b[i][1]))
               
            present_genomes = []
            
            present_genomes = list(dict.fromkeys(b_list))
            
            
            only_resistant_genomes = []
            only_susceptible_genomes = []
                
            
            for i in range(len(b_list)):
                
                if b_list[i] in g_list:
                    
                    if b[i][3] in antibiotics:
                        
                        j = antibiotics.index(b[i][3])
                        
                        if b[i][4] == "Susceptible":
                            
                            exclusive = True
                            unique = True
                            
                            for k in range(len(antibiotics)):
                                
                                if b_list[i] in antibiotics_genomes_R[k]:
                                    
                                    exclusive = False            
                                
                            if b_list[i] in antibiotics_genomes_S[j]:
                                    
                                unique = False                        
               
                            if exclusive and unique:
                            
                                antibiotics_genomes_S[j].append(b_list[i])
                                
                                if b_list[i] not in only_susceptible_genomes:
                                    
                                    only_susceptible_genomes.append(b_list[i])
                                    
                            
                        
                        if b[i][4] == "Resistant":
                            
                            exclusive = True
                            unique = True
                   
                            for k in range(len(antibiotics)):
                                
                                if b_list[i] in antibiotics_genomes_S[k]:
                                    
                                    exclusive = False
                                
                            if b_list[i] in antibiotics_genomes_R[j]:
                                    
                                unique = False   
                                
                            if exclusive and unique:
                            
                                antibiotics_genomes_R[j].append(b_list[i])
                                
                                if b_list[i] not in only_resistant_genomes:
                                    
                                    only_resistant_genomes.append(b_list[i])
                                    
                 
            print("\n")
            
            
            r_genomes = len(only_resistant_genomes)
            s_genomes = len(only_susceptible_genomes)
            
            print("Total of available genomes: ", str(len(g_list)))
            print("Indexed genomes: ", str(len(present_genomes)))
            print("Indexed only-susceptible genomes: ", str(s_genomes))
            print("Indexed only-resistant genomes: ", str(r_genomes))
            print("Total of interesting genomes: ",str(r_genomes+s_genomes))
            
            
            print("Exporting indexed only-susceptible genomes...")
            
            index = 1
              
            for i in range(len(only_susceptible_genomes)):
                AlphaMine.loadingBar(i+1,s_genomes,3)
                index = AlphaMine.Preprocessor.fasta_to_seqset(only_susceptible_genomes[i], g_path, "s_genomes/", index)
            
            
            print("Exporting indexed only-resistance genomes...")
            
            index = 1
            
            for i in range(len(only_resistant_genomes)):       
                 AlphaMine.loadingBar(i+1,r_genomes,3)
                 index = AlphaMine.fasta_to_seqset(only_resistant_genomes[i], g_path, "r_genomes/", index)    
            

    class Pangee():
        
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
            
        
        def compare(pangenome_type, ref_genome, genome, sim_threshold, len_margin, lengths, length):
                              
            found = False
                    
            seq = 0
            
            if length in lengths[1]:
       
                index_ref = lengths[0].index(length)
                index_gen = lengths[1].index(length)
                
                seq1 = ref_genome[index_ref]
                seq2 = genome[index_gen]
                
                similarity = AlphaMine.Pangee.kengine(seq1,seq2)
             
                if similarity > sim_threshold:
                    
                    found = True
                    
                    lengths[1].pop(index_gen)
                
            if not found:
                      
                gene_margin = int(length*len_margin)
                
                for j in range(0, gene_margin):
                                                
                    if length+j in lengths[1]:
       
                        index_ref = lengths[0].index(length)
                        index_gen = lengths[1].index(length+j)
                
                        seq1 = ref_genome[index_ref]
                        seq2 = genome[index_gen]
                        
                        similarity = AlphaMine.Pangee.kengine(seq1,seq2)
                        
              
                        if similarity > sim_threshold:
                    
                            found = True
                            
                            lengths[1].pop(index_gen)
                            
                            break
                    
                    if length-j in lengths[1]:
       
                        index_ref = lengths[0].index(length)
                        index_gen = lengths[1].index(length-j)
                
                        seq1 = ref_genome[index_ref]
                        seq2 = genome[index_gen]
                
                        similarity = AlphaMine.Pangee.kengine(seq1,seq2)
    
         
                        if similarity > sim_threshold:
                    
                            found = True
                            
                            lengths[1].pop(index_gen)
                            
                            break
                        
            if found: 
                
                seq = seq1
                
                
            return [seq, lengths]
                        
        
        def analyze(pangenome_type, genome, ref_genome, sim_threshold, len_margin):
                  
               
           lengths = [[len(seq) for seq in ref_genome], [len(seq) for seq in genome]]
            
           trials = 0
           
           proto_pangenome = []
                        
           for i in range(len(lengths[0])):
               
               trials += 1
        
               AlphaMine.loadingBar(trials,len(lengths[0]),3)
        
               seq,lengths = AlphaMine.Pangee.compare(pangenome_type,
                                                      ref_genome, 
                                                      genome, 
                                                      sim_threshold, 
                                                      len_margin, 
                                                      lengths, 
                                                      lengths[0][i])
               
               proto_pangenome.append(seq)
              
           pangenome = []
                      
           for gene in proto_pangenome:
                                            
               if isinstance(gene, int) == False:
                   pangenome.append(gene)
         
           if abs(len(pangenome)-len(ref_genome)) > 4000:
                
                print(" ")
                print("WARNING: Aberrant genome found, skipping")
                pangenome = ref_genome
  
           return pangenome
                                    
        def pangenome_loadingBar(count,total,size,pangenome_size):
            percent = float(count)/float(total)*100
            sys.stdout.write("\r" + "Elements: " + str(int(pangenome_size)) + ". Progress: " +  str(int(count)).rjust(3,'0')+"/"+str(int(total)).rjust(3,'0') + ' |' + '='*int(percent/10)*size + ' '*(10-int(percent/10))*size + '|') 
            
        def compute_pangenome(genome_paths, sim_threshold, pangenome_type, len_margin):
        
            genomes = []
            genome_seqs = []
              
            print("")
            print("B U I L D I N G  C O R E  P A N G E N O M E")
            print("_________________________________________________")
            print(" ")
                
            print("Loading genomes")
            for i in range(0, len(genome_paths)):
                
                AlphaMine.loadingBar(i+1,len(genome_paths),3)
                
                seq_list = open(genome_paths[i]).read().splitlines()
                seqs = len(seq_list)
                genomes.append(seq_list)
                genome_seqs.append(seqs)
        
            print("")
            print("Selecting genome with smaller number of element candidates")
                    
            found = False
            
            too_short = 0
            
            while not found:
                
               ref_genome_index = genome_seqs.index(min(genome_seqs))
            
               if min(genome_seqs) < 4000:      
                   
                   genomes.pop(ref_genome_index)
                   genome_seqs.pop(ref_genome_index)
                   too_short += 1 
                  
               else:
                   
                   found = True
            
            ref_genome = genomes[ref_genome_index]
            
            print(str(too_short), "genomes had too few elements and were deleted")
            print("The reference minimal genome presents",str(len(ref_genome)),"elements")
            print(" ")
            print("Removing reference genome from collection")
          
            pangenome = ref_genome
            genomes.pop(ref_genome_index)
            genome_seqs.pop(ref_genome_index)
            
            print(" ")
            print("Current elements found in the core pangenome:", len(ref_genome))            
            print(" ")
            print("A N A L Y S I N G   G E N O M E S")
            print("-------------------------------------------------")
            print(" ")
            
            for i in range(len(genomes)):
                
                print(" ")
                print(str(i+1),"/",str(len(genomes)))
                print(" ")
                
                if len(pangenome) > 0:
                    pangenome = AlphaMine.Pangee.analyze(pangenome_type,
                                                         genomes[i], 
                                                         pangenome, 
                                                         sim_threshold, 
                                                         len_margin) 
    
                else: 
                    print(" ")
                    print("ERROR: No core shared elements found")
                
                
            if len(pangenome) > 0:
               
                print("")
                print("Pangenome built!")
        
            return pangenome
        
        


if __name__ == "__main__":
             
    AlphaMine.start()
        
        
   
