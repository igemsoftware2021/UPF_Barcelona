# About AlphaMine


AlphaMine is a modular, simple and flexible Python-based genomics software. To perform its task, it does not depend on traditional sequence alignment but a much more efficient combination of word frequency-based methods and low dimensional clustering. The software can be easily integrated into computational pipelines, and it is intuitive to use and configure. It focuses on the autonomous analysis of large collections of prokaryotic genomes from a comparative perspective and relies on set theory operations.

 
AlphaMine is designed as a nested-class structure. Its core module, called Pangee, is the one directly manipulating the genomes, performing set operations, and constructing pangenomes. Then, the system is built on Pangee with the other parts, such as a preprocessor for data preparation, a command-line interface for better user control, or a managing mechanism to bridge between the higher-level instructions and the internal processes.

<p align="right">(<a href="#top">back to top</a>)</p>
