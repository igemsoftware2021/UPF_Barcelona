# -*- coding: utf-8 -*-
import tensorflow 
import pandas as p
import numpy as np
from  tensorflow.keras.models import Model
from  tensorflow.keras.layers import Input,Dense,Dropout,Flatten,Conv2D,BatchNormalization,LeakyReLU,MaxPooling2D
import os

 
    
"""
This is the class that act as a template for producing OmegaCore's Subunit.
It contains functions to generate them, load the data, create the datasets,
building their architecture, training, evaluating and exporting them.
"""
class OmegaSubunit():
 
 
    """
    Subunit generative method.
    
    1. Load the target profile and parameters.
    2. Load the training data.
    3. Create training and test set.
    4. Train.
    5. Evaluate.
    
    The export is done separately, by the main program.
    """
    
    def __init__(self, TARGET_PROFILE, BATCH_SIZE, LEARNING_RATE, DROP):
        
        self.TARGET_PROFILE = TARGET_PROFILE
        self.BATCH_SIZE = BATCH_SIZE
        self.LEARNING_RATE = LEARNING_RATE
        self.DROP = DROP
        self.N = None
        
        print("")
        print("TARGET PROFILE: ", self.TARGET_PROFILE)
        print("")
        
        print("")
        print("Loading data for ", self.TARGET_PROFILE)
        print("")
        try:
            data, labels = self.load_data()
        except Exception as e:
            print("ERROR: There was a problem loading the data")
            print(e)
            print(" ")
            
        print("")
        print("Creating trainset and testset")
        try:
            trainset, testset = self.load_data(data, labels)
            print("Done!")
        except Exception as e:
             print("ERROR: There was a problem creating the datasets")
             print(e)
             print(" ")
            
        print("")
        print("Training subunit")
        try:
            self.train_subunit(trainset, testset)
            print("Done!")
        except Exception as e:
             print("ERROR: There was a problem during training")
             print(e)
             print(" ")
             
        print("")
        print("Evaluating subunit")
        try:
            self.evaluate_subunit(testset)
            print("Done!")
        except Exception as e:
             print("ERROR: There was a problem during evaluation")
             print(e)
             print(" ")
        
        

    def read_CSV(filename):

        data = []
        data_elements = p.read_csv(filename)
        data_raw = list(data_elements.itertuples())
        print("Extracting total number of elements")
        num = len(data_raw)
        print(num)
        print("Creating ordered data list")
        for i in range(0,num):
            line = list(data_raw[i])
            data.append(int(line[1]))
                
        return data
       
    """
    Function to load the data.
    The tensors are extracted from the NumpyArray.
    The labels are obtained from its parent CSV.
    """
    def load_data(self):
        
        print("______________________________________________________________")
        print("Loading Complete Data Set")
        print("--------------------------------------------------------------")
        print("Loading DATA")
        data = np.load(self.TARGET_PROFILE+'.npy')
        raw_labels = self.read_CSV.read(self.TARGET_PROFILE+'.csv')
        print("--------------------------------------------------------------")
        print("Loading labels")
        labels = np.array(raw_labels)
        print(" ")
        
        return data, labels
     
          
    """
    Function to create the train and test set.
    75% of samples for the first.
    25% of samples for the second.
    Furthermore, the matrix dimensions are obtained for the next steps.
    Finally, the datasets are properly divided into batches.
    """
    def create_datasets(self, data, labels):
    
        ds_all = tensorflow.data.Dataset.from_tensor_slices((data,labels))
            
        data_test = []
        labels_test = []
        
        dimensions = self.data[0,:,:].shape
        
        self.N = dimensions[0]
        
        for i in range(len(self.data)):
            
            if i % 4 == 0:
                
                im = self.data[i,:,:]
                data_test.append(im)
                labels_test.append(self.labels[i])
        
        
        def is_test(x, y):
            return x % 4 == 0
        
        def is_train(x, y):
            return not is_test(x, y)
        
        recover = lambda x,y: y

        print("______________________________________________________________")
        print("Creating Training and Test Sets")
        print("--------------------------------------------------------------")
        print("Image resizing")
        
        ds_train = ds_all.enumerate() \
                            .filter(is_train) \
                            .map(recover)
        
        ds_test = ds_all.enumerate() \
                            .filter(is_test) \
                            .map(recover)
                        
        print("Samples in training set: "+str(sum(1 for _ in ds_train))) 
        
        print("Samples in test set: "+str(sum(1 for _ in ds_test))) 
        

        ds_train = ds_train.batch(batch_size=self.BATCH_SIZE, drop_remainder=True)
        ds_test = ds_test.batch(batch_size=self.BATCH_SIZE, drop_remainder=True)


        print("Batches in training set: "+str(sum(1 for _ in ds_train))+", each of them with "+str(self.BATCH_SIZE)+" samples.") 

        print("Batches in test set: "+str(sum(1 for _ in ds_test))+", each of them with "+str(self.BATCH_SIZE)+" samples.") 
        
        return ds_train, ds_test
       
    """
    This method is used to build the CNN architecture. 
    There are 3 threads, one for cross-class analysis,
    one for mono-class analysis and one for mixed analysis.
    Each thread presents the same structure, with three blocks of
    increasing filter size, including:
    1. The convolution per se, with its size adapted to the input tensor.
    2. Batch normalization for increaed stability.
    3. Dropout for more generalization.
    4. Max pooling for block-to-block transfer
    5. LeakyReLU activation function for better performance.
    """    
    def build_architecture(self):
    
        input_shape = Input(shape=(self.N, self.N, 1))
    
        monoclass_thread = Conv2D(4,(round(self.N/4),1),padding = 'same')(input_shape)
        monoclass_thread = BatchNormalization()(monoclass_thread)
        monoclass_thread = LeakyReLU()(monoclass_thread)
        monoclass_thread = MaxPooling2D(pool_size = (2,2))(monoclass_thread)
        monoclass_thread = Dropout(self.DROP)(monoclass_thread)
        
        monoclass_thread = Conv2D(8,(round(self.N/3),1),padding = 'same')(monoclass_thread)
        monoclass_thread = BatchNormalization()(monoclass_thread)
        monoclass_thread = LeakyReLU()(monoclass_thread)
        monoclass_thread = MaxPooling2D(pool_size = (2,2))(monoclass_thread)
        monoclass_thread = Dropout(self.DROP)(monoclass_thread)
        
        monoclass_thread = Conv2D(8,(round(self.N/2),1),padding = 'same')(monoclass_thread)
        monoclass_thread = BatchNormalization()(monoclass_thread)
        monoclass_thread = LeakyReLU()(monoclass_thread)
        monoclass_thread = MaxPooling2D(pool_size = (2,2))(monoclass_thread)
        monoclass_thread = Dropout(self.DROP)(monoclass_thread)
        
        crossclass_thread = Conv2D(4,(1,round(self.N/4)), padding = 'same')(input_shape)
        crossclass_thread = BatchNormalization()(crossclass_thread)
        crossclass_thread = LeakyReLU()(crossclass_thread)
        crossclass_thread = MaxPooling2D(pool_size = (2,2))(crossclass_thread)
        crossclass_thread = Dropout(self.DROP)(crossclass_thread)
        
        crossclass_thread = Conv2D(8,(1,round(self.N/3)),padding = 'same')(crossclass_thread)
        crossclass_thread = BatchNormalization()(crossclass_thread)
        crossclass_thread = LeakyReLU()(crossclass_thread)
        crossclass_thread = MaxPooling2D(pool_size = (2,2))(crossclass_thread)
        crossclass_thread = Dropout(self.DROP)(crossclass_thread)
        
        crossclass_thread = Conv2D(8,(1,round(self.N/2)),padding = 'same')(crossclass_thread)
        crossclass_thread = BatchNormalization()(crossclass_thread)
        crossclass_thread = LeakyReLU()(crossclass_thread)
        crossclass_thread = MaxPooling2D(pool_size = (2,2))(crossclass_thread)
        crossclass_thread = Dropout(self.DROP)(crossclass_thread)
                
        common_thread = Conv2D(4,(round(self.N/4),round(self.N/4)),padding = 'same')(input_shape)
        common_thread = BatchNormalization()(common_thread)
        common_thread = LeakyReLU()(common_thread)
        common_thread = MaxPooling2D(pool_size = (2,2))(common_thread)
        common_thread = Dropout(self.DROP)(common_thread)
        
        common_thread = Conv2D(8,(round(self.N/4),round(self.N/3)),padding = 'same')(common_thread)
        common_thread = BatchNormalization()(common_thread)
        common_thread = LeakyReLU()(common_thread)
        common_thread = MaxPooling2D(pool_size = (2,2))(common_thread)
        common_thread = Dropout(self.DROP)(common_thread)
        
        common_thread = Conv2D(8,(round(self.N/4),round(self.N/2)),padding = 'same')(common_thread)
        common_thread = BatchNormalization()(common_thread)
        common_thread = LeakyReLU()(common_thread)
        common_thread = MaxPooling2D(pool_size = (2,2))(common_thread)
        common_thread = Dropout(self.DROP)(common_thread)
    
    
        merged = tensorflow.keras.layers.concatenate([monoclass_thread,  crossclass_thread, common_thread], axis=1)
        merged = Flatten()(merged)
        
        out = Dense(16)(merged)
        out = BatchNormalization()(out)
        out = LeakyReLU()(out)
        out = Dropout(self.DROP)(out)
        
        out = Dense(1, activation='sigmoid')(out)
    
        ARCHITECTURE = Model(input_shape, out)
        
        ARCHITECTURE.compile(
            optimizer=tensorflow.keras.optimizers.Adam(learning_rate=self.LEARNING_RATE), loss='binary_crossentropy', metrics=["accuracy"]
        )
                  
        return ARCHITECTURE

    """
    This is the function to train the subunits. First builds the
    architecture, the creates patience and checkpoint callbacks,
    and then proceeds to fit the model.
    """ 
    def train_subunit(self, ds_train, ds_test):
        
        self.CNN = self.build_architecture()

        self.CNN.summary()
        
        patience_callback = tensorflow.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=10)
        
        checkpoint_callback = tensorflow.keras.callbacks.ModelCheckpoint(
            filepath='./weigth_checkpoint',
            save_weights_only=True,
            monitor='val_accuracy',
            mode='max',
            save_best_only=True)
    
        
        self.CNN.fit(ds_train, epochs=self.EPOCHS, validation_data = ds_test, verbose=1, callbacks=[checkpoint_callback, patience_callback])
        
        print("Training finished!")
        
        
    """
    This is methos is used to evaluate that the checkpoint
    loaded is reaching the expected, maximum validation accuracy.
    """ 
 
    def evaluate_subunit(self, ds_test):
        
        self.CNN.load_weights('./weight_checkpoint')     
        self.CNN.evaluate(ds_test, verbose=1)
        
    """
    This simple function is used to export the resulting model
    as an H5 file once the training and evaluation are finished.
    The model is exported with the name of the target profile/behavior
    it should detect, as this information is then used for building the
    report during inference.
    """ 
    def export_subunit(self):
        
        try:
            self.CNN.save(self.TARGET_PROFILE+'.h5')
        except Exception as e:
             print("ERROR: There was a problem exporting the subunit")
             print(e)
             print(" ")
        
        
 
        
      
if __name__ == "__main__":
    
   
    """
    This the workflow of the entire system.
    
    1. Load the data available and define the potential
    subunits that may be trained by creating a profile list.
    
    2. If there are not profiles available, inform the user
    and stop the execution.
    
    3. If there are profiles, ask the user if they want
    to generate the corresponding subunits.
    
    4A. If yes, start the training cycle, producing one
    trained subunit per profile and exporting it.
    
    4B. If not, stop execution.
    
    """
    
 

    print(" ")
    print(" ----------------------------------------")
    print(" W E L C O M E   T O   O M E G A C O R E")
    print(" ----------------------------------------")
    print(" ")
    
    print(" ")
    
    try:
    
        profiles = os.listdir("profiles")
        
        if len(profiles) == 0:
            
            print("No profile data available, stopping...")
            
        else:
            
            print("These are the profiles detected: ")
            
            print(" ")
                 
            for profile in profiles:
                      
                print(profile)
                
            print(" ")
            
            option = input("Start ensemble generation? y/n ")
    
            if option == 'y':
                
                print(" ")        
                print("G E N E R A T I N G   S U B U N I T S")
                print(" ")        
                
                for profile in profiles:
                    
                    print(" ")
                    
                    print("> Generating subunit to detect ",profile)
                    print("_____________________________________________________________")
                    print(" ")
                    
                    Subunit = OmegaSubunit(profile, 10, 0.00025, 0.5)
                    
                    print(" ")
                    print("Exporting subunit...")
                    print("_____________________________________________________________")
                    print(" ")
                    
                    Subunit.export_subunit()
                    
    except:
    
        print("No profile founds, stopping...")
                
        
    print(" ")
    input("Press any key to exit")
    
