<div id="top"></div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project"> About ARIA's Software</a>
    <li><a href="##AlphaMine">AlphaMine</a></li>
    <li><a href="##AlphaNeuro">AlphaNeuro</a></li>
    <li><a href="##ARIABuiler">ARIABuilder</a></li>
    <li><a href="##OmegaCore">OmegaCore</a></li>
    <li><a href="##IRIS">IRIS</a></li>
    <li><a href="##OmegaServer">OmegaServer</a></li>
  </ol>
</details>


# About ARIA's Software
 
When dealing with antibiotic resistance, the key consists of properly assisting those who fight for the patients' health in the frontline. To do so, we consider it is necessary to effectively integrate, characterize and synthesize information. Why? Because by using the proper techniques to turn this knowledge into a strong analytic power, tools can be created and deployed to help health workers guide and execute the diagnostic, therapeutic, and managing processes that save lives.

That is precisely the cornerstone of ARIA's computational work, which we called Alpha and Omega. As the letters of the ancient alphabet from which they take their name, these two pieces draw the beginning and the end of a translational paradigm; two sides of the same coin that, if completed, could face this extremely complicated problem from start to finish.

To materialize Alpha's and Omega's implementation, we have developed a collection of autonomous modules. Here, you will find a brief presentation for each of the systems developed.

 
 
# Alpha
 
On the one hand, Alpha modules are focused on transforming data into distinct forms of valuable and usable knowledge. Here, each of them is presented in their own separate directory.

   
## AlphaMine
An alignment-free genomic analysis system that can build core, shell, and cloud prokaryotic pangenomes by applying set-theory operations to genome collections. Based on word frequency methods and low-dimensional clustering, the system allows finding commonalities and differences between genomes, with no external support, and in a fast, flexible fashion. Thus, it can be used for the discovery and characterization of genomic subsystems.

## AlphaNeuro
An ensemble of 1D Convolutional Neural Networks that can be trained to identify whether an input DNA sequence is relevant for antibiotic resistance or pathogeny. If that is the case, it further analyzes if its role is specially related to a given resistance strategy, a virulence path, or some DNA-sharing mechanism. Its architecture has been conceived to be easily scalable to new cases, with more training data.

## ARIABuilder
A biosensor-designing system that, given a set of DNA markers, uses word frequency methods and construction rules to produce an optimized collection of gRNA target sequence templates for CRISPR/CAS detection. Each sequence is focused on a specific marker, so the system organizes the templates in a matrix-like structure defined by functional classes: the Antibiotic Resistance Inference Array.
 
 
# Omega
On the other hand, Omega modules are intended to generate easy-to-use analytic power, predictive and diagnostic capabilities. The three systems are found on the 'Omega' directory.


## OmegaCore
A system to generate ensembles of lightweight 2D Convolutional Neural Networks that can be trained to analyze the emergence of resistant or pathological profiles in ARIA samples. To do so, each network subunit is focused on identifying the appearance of a particular dangerous behavior, based on the presence or absence of specific markers. By going through each of the subunits, the sum of behaviors detected in the sample can be combined into the pathogen’s resistance profile.


## IRIS
A computer vision system embedded into a cross-platform application. Intended to act as the bridge between ARIA’s computational mechanisms and the user, its goal is to automatically extract the key information from ARIA samples, to reduce such data into simple binary matrixes, and to send it to the internet for further processing. Its source code is developed to facilitate its compilation for Windows, Linux, macOS, Android, and iOS.


## Omega Server
An experimental client-server approach to couple IRIS with OmegaCore, and by doing so, to make possible the access to ARIA’s computational systems as a ready-to-use inference service. To do so, it focuses on a managing platform that can process requests coming from IRIS clients, analyze them with OmegaCore, and prepare a result report that is sent by email to the user.

 
 
# Proof of Concept, testing and integration
 
From our point of view, a suitable pipeline to integrate these systems could be the one shown in our integrated proof-of-concept proposal. Nevertheless, each of these modules is conceived to be wired and re-wired following different configurations, all according to the specific needs of the context. By building this puzzle-like environment, in which the modules can be combined and escalated in different ways, we seek the flexibility and robustness required for such a tremendous task, imagining a mechanism that can deal with the wide variety of real cases that may exist in real clinical settings.



