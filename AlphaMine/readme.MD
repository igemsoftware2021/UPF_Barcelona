# About AlphaMine


It is clear that antibiotic resistance is eminently complex by its nature, and that as knowledge about it increases, the number of possibilities and the multiple mechanisms involved becomes greater, especially regarding indirect interactions that may create the right conditions for resistance to emerge. In this context, it could be valuable to analyze the biological system from a bottom-to-top perspective, focusing on how the connections between simple elements bring out the dangerous capacities of resistant bacteria. Thus, it may be worth using approaches that seek to find from scratch those threads to pull at first: what may be seating the bases for resistance? That was the motivation to create AlphaMine.

![Demo File](https://github.com/igemsoftware2021/UPF_Barcelona/main/AlphaMine/animation.gif)

AlphaMine is a modular, simple and flexible Python-based genomics software. To perform its task, it does not depend on traditional sequence alignment but a much more efficient combination of word frequency-based methods and low dimensional clustering. The software can be easily integrated into computational pipelines, and it is intuitive to use and configure. It focuses on the autonomous analysis of large collections of prokaryotic genomes from a comparative perspective and relies on set theory operations.

 
AlphaMine is designed as a nested-class structure. Its core module, called Pangee, is the one directly manipulating the genomes, performing set operations, and constructing pangenomes. Then, the system is built on Pangee with the other parts, such as a preprocessor for data preparation, a command-line interface for better user control, or a managing mechanism to bridge between the higher-level instructions and the internal processes.

<p align="right">(<a href="#top">back to top</a>)</p>

## Defining a word frequency-based comparison algorithm

In the context mentioned above, below we propose an algorithm to compare sequences of the word frequency-based type. This will focus on reducing the sequences to be compared to two vectors of the same size, and calculating the angle to separate them, from which the similarity per se will be estimated.

We start from two sequences that we must compare. First, we must define a fixed size k for the words that we are going to create, the kmers. In the literature, there are fundamental mathematical relationships that allow us to estimate the optimal k from the size of the sequences that we are going to analyze, so we can leave this parameter defined. 

Having already done this, we generate for each of the sequences its own set of kmers. This consists of an iterative process of going through the positions of the sequence and taking the following k-1 elements to form all possible kmers.

With the derived set of each sequence, we calculate the union between both, and thus we obtain a new set. The total number of kmers that could exist in both sequences is contained in this new set. Taking each of its elements, and counting how many instances of these exist in both sequences, we will have created two vectors that represent the frequencies of the kmers. As the order has been defined by the union vector, which is unique, both vectors will be consistent.

At this point, we simply have to calculate the cosine distance between both vectors, and multiply the number obtained by 100. The result will be the estimate of the percentage of similarity between both sequences.


<p align="right">(<a href="#top">back to top</a>)</p>
