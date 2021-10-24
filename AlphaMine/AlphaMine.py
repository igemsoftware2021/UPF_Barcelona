import os
import sys
import re
from collections import Counter
import math
import numpy as np
import pandas as pd
from Bio import SeqIO
import pyrodigal

# This is the main class that contains the entire system.
class AlphaMine():
    
    sim_thresh = 70
    len_margin = 0.1
    active = True
    
    """
    This a menu function designed to interface with the user 
    when AlphaMine is used in a standalone manner. It takes
    text inputs from the terminal, and sends them to the 
    Command Manager, the centralized system that starts
    the tasks when required.
    """
    
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
            
          
    # A support function to render the progress on an ongoing process.
    def loadingBar(count,total,size):
        
        percent = float(count)/float(total)*100
        sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/"+str(int(total)).rjust(3,'0') + ' [' + '='*int(percent/10)*size + ' '*(10-int(percent/10))*size + ']') 
        
    # A simple function to save sequence sets in text files.
    def save_seqset(seqset, name):
        
        with open(name+".txt", 'w') as f:
            for seq in seqset:
                f.write("%s\n" % seq)        
    
    # The link with the preprocessor.
    def preprocess():
        
        AlphaMine.Preprocessor.generate_seq_library()
            
    """
    The link to order Pangee a pangenomic coperation.
    It loads the files needed from the directory provided
    and prepares them for processing, together with 
    the right parameters.
    """
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
        
    """
    The Command Manager is the centralized structure responding to specific 
    instructions. It can work coupled with the user interface, in standalone mode,
    or just by taking AlphaMine as some module in a broader pipeline, a case
    in which the commands can be called directly.
    """    
    class Commands():
        
        # This instruction shows the possible operations to use.
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
            
        # This instruction allows the creation of a seqset library for further processing. 
        def preprocess_AMR_data():
            
            try:
             
                AlphaMine.preprocess()
                
                AlphaMine.start()
            
            except Exception as e: 
                
                print("Sorry, there was a problem with the previous command...")
                print(e)
                
        """
        This instruction allows the computation of the pangenome in a group of sequence sets.
        The user can specify if a complete or core pangenome is required, and the directory 
        where the data is found.
        """
        def find_pangenome():
        
            try:
             
                genomes_path = input("Genomes path? ")
                
                asking = True
                
                while asking:      
                    try:
                        pangenome_type = int(input("Pangenome type? 0 for core, 1 for complete. "))
                        asking = False
                    except:
                        print("ERROR: please, enter a valid pangenome type")
                
                pangenome = AlphaMine.pangenomize(genomes_path, pangenome_type)
                
                AlphaMine.save_seqset(pangenome, "pangenome")
                
                AlphaMine.start()
                 
            except Exception as e: 
                
                print("Sorry, there was a problem with the previous command...")
                print(e)
            
         
        """
        This instruction implements the algorithm for resistome commputation,
        using complete pangenomes, their intersection and a subtraction to the
        resistant pangenome to obtain the differential genes.
        """
        def find_resistome():
            
             try:
             
                resistant_pangenome = AlphaMine.pangenomize("r_genomes", 1)
                
                susceptible_pangenome = AlphaMine.pangenomize("s_genomes", 1)
                
                intersection_pangenome = AlphaMine.intersection(resistant_pangenome, susceptible_pangenome)
                 
                resistome = AlphaMine.subtract_B_to_A(resistant_pangenome, intersection_pangenome)
   
                AlphaMine.save_seqset(resistome, "resistome")
                
                print("Resistome computed!")
                
                AlphaMine.start()
                 
             except Exception as e:
                 
                print("Sorry, there was a problem with the previous command...")
                print(e)
        
    
    """
    This is the class that preparates the data for further processing.
    To do, it generates a library of sequences sets identified by
    a reference genome ID present in the original data. Thus,
    this information can then be used to guide all the operations
    that may be done after.
    """
    
    class Preprocessor():
        
            
        """
        This function is used to convert raw fasta files into sequences
        sets separated in units that have been identified as genes.
        To do so, it first assembles the entire sequence of the genome,
        and then applies Pyrodigal, a non-supervised ORF-finding
        module created by @althonos. Finally, it stores the resulting 
        sequence set into a text file with a specific ID.
        """
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
        
        
        """
        This is the bulk function that applies the procedure above
        to the entire dataset, so the library can be generated. In order
        to achieve the desired results, the system investigates the CSV
        with the genome annotations, so only those cases that are only
        Resistant or only Susceptible are selected, and properly separated
        in two different directories.
        """
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
         
            
    """
    Pangee is AlphaMine's core. This class
    contains all the tools to perform pangenomic and genomic
    operations based on sequence sets, so it is connected to 
    the rest of the system to recieve instructions and parameters.
    """
    class Pangee():
        
        
        """
        This is the alignment-free comparator, that analyzes
        the frequencies of different kmers and computes
        the cosine distance between the vectors constructed.
        The optimal kmer size is computed using a scale 
        law related to genome's information theory.'
        """
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
            
                
        
        """
        This function applies the progressive set reduction algorithm
        to construct core pangenomes, which are the theoretical set
        intersection between the candidate genomes.
        """
        def compare_for_core(ref_genome, genome, sim_threshold, len_margin, lengths, length):
                              
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
        
        
        """
        This function applies the progressive set extension algorithm
        to construct complete pangenomes, which are the theoretical set
        union between the candidate genomes.
        """
        def compare_for_complete(ref_genome, genome, sim_threshold, len_margin, lengths, length):
                                                    
            seq = 0
            
            not_found = 0
            analyzed = 0
      
            gene_margin = int(length*len_margin)
            
            for j in range(0, gene_margin):
                                            
                if length+j in lengths[1]:
   
                    index_ref = lengths[0].index(length)
                    index_gen = lengths[1].index(length+j)
            
                    seq1 = genome[index_ref]
                    seq2 = ref_genome[index_gen]
                    
                    similarity = AlphaMine.Pangee.kengine(seq1,seq2)
                    
                    analyzed += 1
                    
                    if similarity < sim_threshold:
                        
                        not_found += 1
                        
                        lengths[1].pop(index_gen)
                        
               
                if length-j in lengths[1]:
   
                    index_ref = lengths[0].index(length)
                    index_gen = lengths[1].index(length-j)
            
                    seq1 = genome[index_ref]
                    seq2 = ref_genome[index_gen]
            
                    similarity = AlphaMine.Pangee.kengine(seq1,seq2)
  
                    analyzed += 1
     
                    if similarity < sim_threshold:
                
                        not_found += 1
                        
                        lengths[1].pop(index_gen)
                                     
            if not_found == analyzed:
                
                if not_found > 0:
                
                    seq = seq1
       
            return [seq, lengths]
                        
        
        def analyze(pangenome_type, genome, ref_genome, sim_threshold, len_margin):
                 
            
           trials = 0
           
           if pangenome_type == 0:
               lengths = [[len(seq) for seq in ref_genome], [len(seq) for seq in genome]]
               proto_pangenome = []
           if pangenome_type == 1:
               proto_pangenome = ref_genome
               lengths = [[len(seq) for seq in genome], [len(seq) for seq in ref_genome]]
                        
           for i in range(len(lengths[0])):
               
               trials += 1
        
               AlphaMine.loadingBar(trials,len(lengths[0]),3)
               
               
               if pangenome_type == 0:
        
                   seq,lengths = AlphaMine.Pangee.compare_for_core(ref_genome, 
                                                          genome, 
                                                          sim_threshold, 
                                                          len_margin, 
                                                          lengths, 
                                                          lengths[0][i])
                   
                   
                   proto_pangenome.append(seq)
                   
              
               if pangenome_type == 1:    
                   
                    seq,lengths = AlphaMine.Pangee.compare_for_complete(ref_genome, 
                                                        genome, 
                                                        sim_threshold, 
                                                        len_margin, 
                                                        lengths, 
                                                        lengths[0][i])
                    
                    if isinstance(seq, int) == False:
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
        
        """
        This is the method implementent the subtraction.
        
        """  
        def A_minus_B(genomeA, genomeB):
        
           i = 0  
           difference = []
           for seqA in genomeA:   
               found = False
               AlphaMine.loadingBar(i+1,len(genomeA),3)
               i += 1
               for seqB in genomeB:
                   similarity = AlphaMine.Pangee.kengine(seqA,seqB)
                   if similarity > AlphaMine.sim_thresh:
                       found = True
                       break
               if not found:
                   difference.append(seqA)
                  
  
           return difference
                                    
        def pangenome_loadingBar(count,total,size,pangenome_size):
            percent = float(count)/float(total)*100
            sys.stdout.write("\r" + "Elements: " + str(int(pangenome_size)) + ". Progress: " +  str(int(count)).rjust(3,'0')+"/"+str(int(total)).rjust(3,'0') + ' |' + '='*int(percent/10)*size + ' '*(10-int(percent/10))*size + '|') 
       
        
        """
        This is the general function which manages the specific
        algorithm to compute a certain type of pangenome.
        
        """         
        def compute_pangenome(genome_paths, sim_threshold, pangenome_type, len_margin):
        
            genomes = []
            genome_seqs = []
            ref_genome = None
            
            print("Loading genomes")
            for i in range(0, len(genome_paths)):
                
                AlphaMine.loadingBar(i+1,len(genome_paths),3)
                
                seq_list = open(genome_paths[i]).read().splitlines()
                seqs = len(seq_list)
                genomes.append(seq_list)
                genome_seqs.append(seqs)
                
            found = False
            
            too_short = 0
            
            print("\nFiltering aberrant genomes")
            while not found:
                
               ref_genome_index = genome_seqs.index(min(genome_seqs))
            
               if min(genome_seqs) < 4000:      
                   
                   genomes.pop(ref_genome_index)
                   genome_seqs.pop(ref_genome_index)
                   too_short += 1 
                  
               else:
                   
                   found = True
                   
            print(str(too_short), "genomes had too few elements and were deleted")
    
                    
            if pangenome_type == 0:
                
                print("")
                print("B U I L D I N G    C O R E    P A N G E N O M E")
                print("_________________________________________________")
                print(" ")
                print("")
                print("Selecting genome with smaller number of element candidates")
                
                ref_genome_index = genome_seqs.index(min(genome_seqs))   
                ref_genome = genomes[ref_genome_index]
             
                print("The reference minimal genome presents",str(len(ref_genome)),"elements")
                print(" ")
                print("Removing reference genome from collection")
                
            if pangenome_type == 1:
                
                print("")
                print("B U I L D I N G    C O M P L E T E    P A N G E N O M E")
                print("_________________________________________________")
                print(" ")
                print("")
                print("Selecting genome with larger number of element candidates")
                
                ref_genome_index = genome_seqs.index(max(genome_seqs))   
                ref_genome = genomes[ref_genome_index]
                   
                print("The reference maximal genome presents",str(len(ref_genome)),"elements")
                print(" ")
 
                
            print("Removing reference genome from collection")
            
            genomes.pop(ref_genome_index)
            genome_seqs.pop(ref_genome_index)
            pangenome = ref_genome
  
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

    """
    This function is used to compute the intersection
    between two genomes as very simple core pangenome.
    
    """        
    def intersection(genome_A, genome_B):
            
        genomes = [genome_A, genome_B]
        genome_seqs = [len(genome_A), len(genome_B)]
        ref_genome = None
        
        print("Loading genomes")
          
       
        print("")
        print("C O M P U T I N G    I N T E R S E C T I O N")
        print("_________________________________________________")
        print(" ")
        print("")
        print("Selecting genome with smaller number of element candidates")
        
        ref_genome_index = genome_seqs.index(min(genome_seqs))   
        ref_genome = genomes[ref_genome_index]
        
        prob_genome_index = genome_seqs.index(max(genome_seqs))   
        prob_genome = genomes[prob_genome_index]
     
        print("The reference minimal genome presents",str(len(ref_genome)),"elements")
        print(" ")
    
        intersection = ref_genome
        
    
        print(" ")
        print("A N A L Y S I N G   G E N O M E S")
        print("-------------------------------------------------")
        print(" ")
        
    
        intersection = AlphaMine.Pangee.analyze(0,
                                             prob_genome, 
                                             intersection, 
                                             AlphaMine.sim_thresh, 
                                             AlphaMine.len_margin) 

        
        if len(intersection) > 0:
           
            print("")
            print("Intersection computed!")
    
        return intersection  
    
    """
    This function is used to compute the difference
    between two genomes, in the form:
    
    DIFFERENCE = GENOME_A - GENOME_B
    
    """
        
    def subtract_B_to_A(genome_A, genome_B):
                
        print("Loading genomes")
          
       
        print("")
        print("C O M P U T I N G    S U B T R A C T I O N")
        print("_________________________________________________")
        print(" ")
       
        print(" ")
        print("A N A L Y S I N G   G E N O M E S")
        print("-------------------------------------------------")
        print(" ")
        
    
        subtracted = AlphaMine.Pangee.A_minus_B(genome_A, genome_B) 
  
        if len(subtracted) > 0:
           
            print("")
            print("Subtraction computed!")
    
        return subtracted



if __name__ == "__main__":
             
              
    """
    To use AlphaMine in a standalone fashion,
    just call the start method and the interface will be 
    instanced as the system's control mechanisms.
    To use it as a module, just call the commands
    in the Command Manager with the parameters required.
    """
    AlphaMine.start()
        
        
   
        
   
