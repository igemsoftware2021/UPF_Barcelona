# About AlphaMine


It is clear that antibiotic resistance is eminently complex by its nature, and that as knowledge about it increases, the number of possibilities and the multiple mechanisms involved becomes greater, especially regarding indirect interactions that may create the right conditions for resistance to emerge. In this context, it could be valuable to analyze the biological system from a bottom-to-top perspective, focusing on how the connections between simple elements bring out the dangerous capacities of resistant bacteria. Thus, it may be worth using approaches that seek to find from scratch those threads to pull at first: what may be seating the bases for resistance? That was the motivation to create AlphaMine.

AlphaMine is a modular, simple and flexible Python-based genomics software. To perform its task, it does not depend on traditional sequence alignment but a much more efficient combination of word frequency-based methods and low dimensional clustering. The software can be easily integrated into computational pipelines, and it is intuitive to use and configure. It focuses on the autonomous analysis of large collections of prokaryotic genomes from a comparative perspective and relies on set theory operations.

 
AlphaMine is designed as a nested-class structure. Its core module, called Pangee, is the one directly manipulating the genomes, performing set operations, and constructing pangenomes. Then, the system is built on Pangee with the other parts, such as a preprocessor for data preparation, a command-line interface for better user control, or a managing mechanism to bridge between the higher-level instructions and the internal processes.

<p align="right">(<a href="#top">back to top</a>)</p>
