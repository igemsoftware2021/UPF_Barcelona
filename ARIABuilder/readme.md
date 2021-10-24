# About ARIABuilder

Other Alpha systems explained are useful because they allow us to find valuable information among large amounts of data, and that is key. However, this is not enough to achieve our goal, which is to provide analytical power to deal with the problem. In other words, we need a system that allows the information found to be translated into a tool applicable to the real world, which can be exploited in the laboratory through synthetic biology.

ARIABuilder is precisely that bridge between computationally produced knowledge and the technological capacity of the laboratory. It is a simple system that, taking as input the set of sequences found by AlphaMine and classified by AlphaNeuro, would design the necessary detection matrix to analyze dangerous pathogens. This includes both the layout of the structure itself and the templates of the biosensors that it will include. ARIABuilder is implemented as a class, in such a way that it can be easily integrated as one more mechanism in other structures. It has several small specialized functions, and the main function is to run the entire build process.

Once the data has been prepared, all the sequences are loaded in an organized manner. The sequence lists for each class are collected in packages associated with resistance, promiscuity, and virulence. Having this, some filtering is applied. First, we seek to select for those sequences that are only associated with a specific mechanism, to maximize their specificity. As there are many cases in which this is not possible, there will be classes that will be left empty. Thus, the process is repeated for these exceptions, looking for those sequences that interact with the minimum of mechanisms.

With an initial set of sequences, it is necessary to perform second filtering to evaluate the feasibility of its detection. That is why we seek the presence of PAMs (protospacer adjacent motifs) that can guide the future CRISPR/Cas. As in our case, we work with CRISPR / Cas12, the PAMs that interest us are TTTG, TTTC, and TTTA. If none of these motifs are found in the sequence analyzed, it is eliminated from the group of candidates. Otherwise, the position in which they have been found is saved, and these sequences are preserved.

 
## Target template generation and filtering
 
With the PAMs located, it is time to generate all the target candidate templates. The procedure consists of going to the position where the PAM begins, and taking the immediately preceding 30-mer, in such a way that we not only collect a potential spacer-complementary region of 20 elements, but we also take a small number of adjacent bases, both upstream and downstream. This will be key for the next step.

The above procedure means that for each class we have a list of sequences and for each sequence a list of candidate target templates. So, the next thing we need is a mechanism to evaluate the effectiveness of a certain template, since this will be the way to optimize the spacers finally produced. To achieve this, we use two criteria.

On the one hand, for a matter of pure stability, we evaluate whether the templates contain a proportion of GC content contained in a range between 0.4 and 0.8.

On the other hand, we have decided to implement, in an experimental way, the algorithm for a function known as Doench Score, which was presented in the work "Rational design of highly active sgRNAs for CRISPR-Cas9-mediated gene inactivation" and that, as its title indicates, acts as a metric of the effectiveness of a given single guide RNA. This mechanism uses different parameters, which change according to the GC content, to evaluate both the influence of the target sequence's structure itself and that of the non-linear interactions that emerge from its adjacent context.


## Implementing a Doench Score computing function
This predictive function is the product of training a logistic regression classification model with effectivity data. That is why, even understanding that the parameters that we have used are thought for CRISPR/Cas9 and therefore we cannot apply it in the production phase (we use CRISPR/Cas12), we believed that it was useful to incorporate it since as the work explains that the training is generalizable, we could thus open the door to developing an analogous process with the data for CRISPR/ Cas12, or any other type, having only to substitute the weights of the logistic regression classifier.

The function within ARIABuilder that implements its calculation is relatively simple: first, we have incorporated the parameters shown in the supplementary material of the referenced paper, with the appropriate indexing. These parameters associate the presence of certain bases in specific positions with previously defined weights, in addition to providing additional weights according to the GC content (one for high, and one for low) and a base sum value. Thus, after receiving an objective sequence to analyze, we separate the spacer from the adjacent context and calculate its GC content, in such a way that we choose the high-level parameter if it exceeds 0.5 and the low-level parameter otherwise.

Once the GC check is done, we modify the base score according to this criteria, and we begin to add the contribution of each of the positions, with their respective weights. After finishing, we pass the score the sum through the logistic function, and thus we obtain the final score, which is what we return: the more effective the target sequence, the closer the value will be to 1, and the lower the closer to 0.


## Final target template selection
After having defined an evaluation mechanism, we select the best target for each sequence (if there is more than one). Now that each sequence presents only the best option that we have been able to find, we repeat this selection process at the level of each class, leaving only the N-best candidates. The selected candidates are then converted to the complementary sequence and transcribed into RNA.

 
## Array design and discussion
 
Now, there will be N spacer templates for each of the N classes, so we have all the necessary components to build the NxN square matrix. To do this, a row is assigned to each mechanism, arranged in contiguous blocks for resistance, virulence, and promiscuity. Subsequently, one of the spacer templates is added to each of the cells in a row. The specific position is defined randomly, to avoid a biosensor effectiveness bias in the inference phase. Finally, a file is exported for each of the templates, showing the sequence of the spacer in question and names as the position of the cell it would occupy: the array has been generated.

Nevertheless, this whole approach is focused on the effectiveness of gRNA as a proof of concept, but we believe that it is necessary to put a strong emphasis on avoiding false positives and interference in our problem, and that is why we are currently studying how to incorporate Kengine to carry out a specificity analysis, in which we generate a score that rewards those templates that diverge the most from the rest.
