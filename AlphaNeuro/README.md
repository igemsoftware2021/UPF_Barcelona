# WELCOME TO ARIA's ALPHANEURO!
In this repository you will find the set of notebooks that we have used to create AlphaNeuro for the iGEM 2021 competition:

![alt text](https://2021.igem.org/wiki/images/3/33/T--UPF_Barcelona--alphaneuro.GIF)

Organization:

  1. Model Training: This folder contains the notebooks used to train the different models for Promiscuity, Virulence and Resistance. Each of the sections contains the particular 
  notebook and the data to be used. Keep in mind that you will need to change the paths of the data and your desired location for the output.
  We would also like to remember that inside the notebooks there are more guidelines on how to run the code and further explanation of the function of each cell.
  Specific details of each model:
    
  1A. Main Discriminator: Contains the separate data and specific cells of code to generate the final data to be input in the network. If you wish to run the 3-class version,you
  should remove the file "essential.txt" from your data folder. In case of the 4-class model, no further changes are needed.

  1B. Promiscuity: The notebook contains a cell to generate the data with the labels from raw fasta files in aminoacid sequence, however, the csv final data file is already
  provided in the folder for simplification. Hence, that cell can be omited.

  1C. Virulence: The final csv is provided and the code contains all guidelines necessary.

  1D. Resistance: The initial data is provided consisting of multiple separate csv files. The code contains cells that allow to join this files in the inputs necessary. It will 
  give you two different csv files. As explained in the notebook, one will serve for training with the resistance mechanisms and the other will keep the antibiotic names.
  
  2. Classification Network: This folder contains the whole assembly of models that allow you to predict sequences from input csv files of your choice. If you do not wish to train
  the models in section 1, pre-trained models are also provided for all the networks to be used.
  The results are displayed in 3 different ways:
  
  2A. Results of the sequences belonging to each class and sub-class or mechanisms can be displayed in the console via print.
  
  2B. Alternatively, you can generate 2 different output CSV files. The first one will give you the predicted label name for each input sequence while the second encodes the
    labels in different colormaps (RGB values).
