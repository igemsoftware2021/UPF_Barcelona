# About AlphaMine


It is clear that antibiotic resistance is eminently complex by its nature, and that as knowledge about it increases, the number of possibilities and the multiple mechanisms involved becomes greater, especially regarding indirect interactions that may create the right conditions for resistance to emerge. In this context, it could be valuable to analyze the biological system from a bottom-to-top perspective, focusing on how the connections between simple elements bring out the dangerous capacities of resistant bacteria. Thus, it may be worth using approaches that seek to find from scratch those threads to pull at first: what may be seating the bases for resistance? That was the motivation to create AlphaMine.

![AlphaMine](animation.gif)

AlphaMine is a modular, simple and flexible Python-based genomics software. To perform its task, it does not depend on traditional sequence alignment but a much more efficient combination of word frequency-based methods and low dimensional clustering. The software can be easily integrated into computational pipelines, and it is intuitive to use and configure. It focuses on the autonomous analysis of large collections of prokaryotic genomes from a comparative perspective and relies on set theory operations.

 
AlphaMine is designed as a nested-class structure. Its core module, called Pangee, is the one directly manipulating the genomes, performing set operations, and constructing pangenomes. Then, the system is built on Pangee with the other parts, such as a preprocessor for data preparation, a command-line interface for better user control, or a managing mechanism to bridge between the higher-level instructions and the internal processes.


## Rationale

Let us imagine that we want to identify the genetic elements related to a certain function in a family of species.

 
We have a subgroup of those species, R, in which we observe the functionality per se, while another subgroup S does not show it. Subsequently, one way to find potential candidates would be to start isolating those genetic components that are only found in the genomes of subgroup R and never appear in S or vice versa. Why? Well, those that only appear in R could be directly exerting the function of interest, while those that only appear in S could be inhibiting the first: in one way or the other, the possibility of studying them could be enlightening.

 
Replace R and S with "Resistant" and "Susceptible" to a specific antibiotic, and the result of this approach will be a pool of genetic elements that may be supporting antibiotic resistance, by their action or absence. Consequently, this seems logical first step to understand, from bottom to top, this dangerous threat emerges. But, what is this "group of genetic elements characteristic of some type of organisms"? A collective super-genome? Be that as it may, something like this is necessary to make the approach possible.


<p align="right">(<a href="#top">back to top</a>)</p>


## On the pangenome
   
Fortunately, genomics brings us a powerful concept that perfectly fits this key definition. The pangenome, or supragenome, describes the entire set of genes shared by a clade, a group of species, and it is a useful tool to unveil their insides beyond the traditional notion of "discrete", well-separated organisms. A complete pangenome can be divided into three different components: the core pangenome (genes shared by the entire clade), the shell pangenome (genes shared by two or more species in the clade), and the cloud pangenome (genes unique to one of the clade's species).

 
If you know the pangenome, you gain a deeper understanding of the studied species' true nature. In that way, to materialize the methodology mentioned before, it is necessary to build a system capable of constructing the pangenomes for different collections of bacterial strains and to properly operate with them, so the elements of interest can be finally isolated.

<p align="right">(<a href="#top">back to top</a>)</p>

## Computing pangenomes

As explained in the rationale, the idea of all this approach is to analyze a collection of bacterial strains: by comparing the ones that resist the antibiotic of interest and the ones that do not, the goal is to isolate what genetically differentiates them for further analysis. In the following subsections, a series of generalized algorithms associated to this task is defined. They are focused on implementing the basic set operations studied before, on the construction of all the types of pangenomes described and finally on how to apply all the concepts to solve the task.
 
The process is practically identical when computing the complete pangenome and the three components mentioned above: core, shell, and cloud. There are some minor details changing, and different strategies to minimize the workload, but this makes possible to design the approaches needed to compute the four types of pangenome.

Start with a group of N genomes, which we call the library. Define one of them as reference, and eliminate it from the library. Depending on the desired type of pangenome, the specific choice and subsequent steps diverge.

On the one hand, we have the complete pangenome. Select as reference the genome with the highest number of sequences. For each sequence in the analyzed set, it is checked whether there is an ortholog the reference set. When there is not, a negative is counted. If after finishing the loop there are as many negatives as elements in the reference set, it means that the sequence in question is new, so it is added to the reference set. On the contrary, if there are fewer negatives, this implies some orthology is detected, so the sequence is already present. In that way, with more and more iterations, the size of the reference set becomes larger. Thus, at the last iteration, the resulting set will be a pangenome that contains all those sequences that appeared in each of the input genomes.

On the other hand, for the core pangenome, select as reference the genome with the smallest number of sequences. Each time that a sequence of reference appears to have an ortholog in the set analyzed, it is included in the selected group and the search for that genome stops. If that is not the case, the sequence is excluded. In this case, when updating, the size of the reference set becomes smaller. Thus, at the last iteration, the resulting set will be a pangenome that contains only those genes presented orthology across the entire collection of input genomes.

 
   
## Resistome-finding Algorithm

Start with two groups of genomes: resistant and susceptible to the antibiotic. To avoid excluding any potential candidate, first construct the complete pangenome for each class, which means to compute the union of all the genomes belonging to the group in question. Once both pangenomes are obtained, compute the intersection between them. Then, on the one hand, subtract the intersection to the resistant pangenome. 

The result will be the resistome. This is the set of all sequences that only appear on resistant strains. On the other hand, subtract the intersection to the susceptible pangenome. The result will be the vulnerome. This is the set of all sequences that only appear on susceptible strains. 

Having obtained both the resistome and the vulnerome, the task of finding potential candidates is solved.

   
<p align="right">(<a href="#top">back to top</a>)</p>


## Defining a word frequency-based comparison algorithm

In the context mentioned above, below we propose an algorithm to compare sequences of the word frequency-based type. This will focus on reducing the sequences to be compared to two vectors of the same size, and calculating the angle to separate them, from which the similarity per se will be estimated.

We start from two sequences that we must compare. First, we must define a fixed size k for the words that we are going to create, the kmers. In the literature, there are fundamental mathematical relationships that allow us to estimate the optimal k from the size of the sequences that we are going to analyze, so we can leave this parameter defined. 

Having already done this, we generate for each of the sequences its own set of kmers. This consists of an iterative process of going through the positions of the sequence and taking the following k-1 elements to form all possible kmers.

With the derived set of each sequence, we calculate the union between both, and thus we obtain a new set. The total number of kmers that could exist in both sequences is contained in this new set. Taking each of its elements, and counting how many instances of these exist in both sequences, we will have created two vectors that represent the frequencies of the kmers. As the order has been defined by the union vector, which is unique, both vectors will be consistent.

At this point, we simply have to calculate the cosine distance between both vectors, and multiply the number obtained by 100. The result will be the estimate of the percentage of similarity between both sequences.


<p align="right">(<a href="#top">back to top</a>)</p>

