<div id="top"></div>


# Introduction

In this directory are the three main modules that make up Omega.

OmegaCore is the system that generates the neural networks that would be responsible for providing the analytical power.
IRIS is the multiplatform computer vision application that automatically processes samples, extracts important information and outsources it via the internet. OmegaServer is the server-client inference system that can load OmegaCore neural networks, and use them to run remote analysis for samples sent by instances of the IRIS application.


<!-- TABLE OF CONTENTS -->
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#About OmegaCore">OmegaCore</a>
       <ul>
        <li><a href="#Data-Organization">Data Organization</a></li>
        <li><a href="#Convolutional-Neural-Network Subunit Architecture">Convolutional Neural Network Subunit Architecture</a></li>
        <li><a href="#Subunit-Generation-Workflow">Subunit Generation Workflow</a></li>
      </ul>
    </li>
     <li>
      <a href="#About-IRIS">IRIS</a>
       <ul>
        <li><a href="#The-artificial-vision-system">The artificial vision system</a></li>
        <li><a href="#The-application">The application</a></li>
      </ul>
    </li>
    <li>
      <a href="#About-OmegaServer">OmegaServer</a>
       <ul>
        <li><a href="#Design-of-the-Communication-Architecture">Design of the Communication Architecture</a></li>
        <li><a href="#Creation-of-the-Inference-Server">Creation of the Inference Server</a></li>
        <li><a href="#Request-based-Communication-Protocol">Request-based Communication Protocol</a></li>
      </ul>
    </li>
    
 
    
  </ol>


# About OmegaCore

Alpha systems are intended to provide useful knowledge, but to fulfill our purpose we need a way to embed said knowledge in a platform that, with sufficient generalizability, can turn it into power to analyze reality and predict what its properties are. This is the premise behind Omega, but it is precisely OmegaCore that embodies this definition in its purest form.

![alt text](https://2021.igem.org/wiki/images/0/01/T--UPF_Barcelona--omegacore_anim.GIF)

OmegaCore is a system that seeks to capture, from a bottom-up approach, how the dangerous behaviors of resistant bacteria emerge through the potential interactions of their constituent mechanisms. For this, it focuses on generating lightweight Convolutional Neural Networks (CNN), the so-called subunits, which are trained to separately evaluate the absence or presence of each of the behaviors of interest: that is, whether or not the whole is the sum of its parts. 

To achieve this, the system will be fed with simulated detection matrices, resulting from probing the genomes of interest with the design provided by ARIABuilder. The result of the process will be a collection of subunits (one for each situation of interest) as self-contained models, which can then be incorporated into an inference module. In this way, by adding the verdict of each one of these subunits, the inference module would determine the complete resistance profile of the sample in question.

<p align="right">(<a href="#top">back to top</a>)</p>

## Data Organization

To perform the training correctly, the system will need the input data to be arranged in a specific way. Specifically, a directory per behavior is required. These behaviors can be resistances to different antibiotics, the development of multiple pathological activities, or distinct levels of genetic-sharing capabilities material. Within each folder, there must be a NumpyArray that contains the tensors of the detection arrays that exhibit this behavior and of the arrays that do not. In addition, the NumpyArray must be accompanied by a CSV that includes the one-hot encoding specifying whether each tensor is positive or negative. 

This implies that matrices can coexist in several classes since those that are positive in one will be negative in another and vice versa. Ideally, the negative examples should be selected from the widest possible variety of positives from the other classes, to promote the specificity of the trained subunits. Regarding the division between training and validation data, it is not necessary to add it, since OmegaCore will apply it automatically for each class. 

The mechanism that we propose to generate the matrices consists of a simple script that creates a tensor of zeros, takes as input the design made by ARIABuilder, loads the genome of interest, and checks if there is a region for each template with sufficient complementarity. If yes, change the corresponding position of the tensor to 1, otherwise, go to the next one. The result would finally be exported as a proper detection matrix, and a specific one-hot encoding based on how the genome was labeled. Repeating this methodology, the whole NumpyArrays and CSVs would be built.

<p align="right">(<a href="#top">back to top</a>)</p>

## Convolutional Neural Network Subunit Architecture

Due to the simplicity of the input information that reaches each of the subunits, their architecture is very light, although it has peculiarities. As the input layer, we take a single channel tensor with the size of the detection array. Next, we copy said tensor in three threads that go in parallel. The first use square filters, the second horizontal filters, and the third vertical filters. Why are we doing this? Well, because we want the subunits to study specifically the correlations between array markers that participate in the same mechanism (rows of the matrix, horizontal filter), array markers that affect different mechanisms (columns of the matrix, filter vertical), and mixed groups of both (rows and columns, square filter). 

Each of the threads is practically identical in structure, being made up of the same basic blocks: Convolution to process the content of a subregion, BatchNormalization to promote stability, LeakyReLu activation function for greater efficiency, MaxPooling for transfer between blocks, and dropout to increase generalizability. Each thread consists of two of these blocks, the first with smaller filters and the second with larger filters. At the end of each thread, the results are concatenated and converted to a vector, which is passed through a small layer of dense neurons. The output is normalized and finally introduced into a sigmoid function, which produces the final result: how likely is the behavior in question to emerge for that set of input markers. With this, we intend to help the subunits to infer in a holistic way the latent probability distributions behind the patterns, trying to capture and interpret the maximum of key nuances.

<p align="right">(<a href="#top">back to top</a>)</p>

## Subunit Generation Workflow

The subunit generation process follows these steps. First, the total number of classes to be analyzed is loaded. Next, the main loop that trains the neural networks is started, which will be executed as many times as classes have been detected. In each iteration, the dataset belonging to the class being analyzed is loaded and divided into two subsets: 75% for training and 25% for validation. Some of the loaded arrays are shown in the terminal for review, and then relatively small batches are generated. Once this is done, the model is defined and compiled. 

Subsequently, a callback focused on validation accuracy is established to stop training if there is no improvement in a certain number of epochs, and another callback is defined to checkpoints during the process, also preserving the best results in validation accuracy. Having prepared all this, we proceed with the training per se. When finished, the evolution of the accuracy for training and validation is shown on the terminal to see if overfitting has occurred. The last model checkpoint is loaded, and its accuracy is re-evaluated with the validation set to check if it is correct. 

Finally, the confusion matrix is displayed, the model is exported as an H5 file, ready for integration into another module. The iteration is completed, so a new training cycle for the next class.

<p align="right">(<a href="#top">back to top</a>)</p>




# About IRIS

With Alpha, we explored the possibility of turning data into useful information, and of translating that information into tools that can be practically brought into the lab. With OmegaCore, we have focused on how to convert this information into analytical power capable of evaluating the results produced by our bio-tools. The next step, then, consists of preparing an accessible interface with which the user can interact with all these systems. 

![alt text](https://2021.igem.org/wiki/images/4/4e/T--UPF_Barcelona--iris_anim.GIF)

This is the main objective of IRIS, the cross-platform application that we are developing to automatically scan the results of the detections and send them to the rest of Omega. In line with this premise, we divided the development of IRIS into two complementary stages: building the artificial vision system and generating the source code of an application that can be easily compiled on the different OS. 

<p align="right">(<a href="#top">back to top</a>)</p>

## The artificial vision system

The artificial vision system is built around the well-known OpenCV library, specifically in its Python version. Applying different computer vision techniques, the system uses the device's camera to locate the array in question, analyze its content and extract a binary matrix with positive and negative detections in the correct positions.  Next, we explain in detail the workflow of the system. 

After initializing, the system accesses the first available camera on the device, extracts its resolution, and calculates the position of the frame center. Then it defines a series of flow control variables and load parameters such as the detection array dimensions (rows and columns). Once this is done, the system enters the main loop. 

In each iteration of the loop, different specialized functions will be called to perform all the required tasks (these functions are explained in more detail in subsequent sections). On the one hand, what the user experiences are just a continuous, real-time video signal with different indicators depending on the situation. On the other hand, lots of processes start to happen internally. 

First, a frame is captured and passed to a search function that detects whether or not there is an array on the image. If affirmative, the frame is sent to the analysis function that evaluates each of the cells, while if negative, the execution continues. Regardless of the previous steps, a drawn on the frame with the approximate size and position that the matrix should present, as well as a small text indicating how it should be oriented. 

All this signaling is then displayed on the video signal in real-time as a guide to assist the user when making the detection. Subsequently, a control function is called to measure whether the user inputs. Finally, there is the last management structure that, based on the result of the control function, externalizes the matrix obtained, stops the execution of the program, or allows the whole cycle to start over. 

The array search function operates in real-time, constantly, taking as input each captured frame and using different transformations to determine if the detection array appears or not. If found, it applies the second block of transformations to separate it from the background, reorient it, and process it for later analysis. 

As a first step, the system turns the frame to black and white and applies a Gaussian filter to homogenize the similar intensity areas and blur the secondary edges. Next, adaptive thresholding is applied to binarizes the image, simplifying the geometric shapes that appear. Once this is done, the system searches for the contours of the different geometric shapes and filters all those that occupy less than 10% of the image. At this point, the surviving geometric shapes are used to generate rectangles that contain them. 

From these rectangles, those whose ratio between width and height is not close to 1 are filtered: that is, we leave only the squares. Finally, the square with the largest area of all those that have passed the filter is selected. This entire procedure is carried out to distinguish the detection array, which is square, from other possible artifacts. The area criterion is applied because, in the guide that we show on the screen, the system is instructing the user to locate the camera at the necessary distance so that its area precisely meets the established criteria. Through these series of conditions, an attempt is made to maximize selectivity when distinguishing the matrix from its environment. 

If all the previous process does not work, the system is indicated that there is no recognizable array in the field of vision, and therefore the participation of the function ends for the current iteration. On the contrary, if the array has indeed been found, we proceed with its extraction. To achieve this, a binary mask is created in which the edges that have been detected for the matrix are drawn, and its content is filled, leaving the shadow of the matrix in the mask as ones, and the rest as zeros. Thanks to this, an AND operation can be applied to eliminate the entire background from the original image: the pixels of the image that correspond to the matrix are multiplied by 1, remaining constant, while those of the background are multiplied by 0, disappearing. 

After doing this, the angle of deviation found in the detection array is used to compute a rotation matrix, which will be applied as an affine transformation to fix the alignment of the object in question. The result: a real-time automatic stabilization system that corrects the orientation of the matrix so that it is always aligned with the screen. After this, the matrix is directly cropped from the rest of the mask, resized, and ready for analysis.
 
The analysis function also runs in real-time, but only while the presence of a detection array is being detected. Once it receives the preprocessed mask, it refines the edges and, executes another Grayscale + Gaussian Filter + Adaptive Thresholding transformation bloc. This results in a binary image that only shows intensity contrasting regions, as the lines conforming the array or the stains in the positive cells. 

At this point, knowing the number of rows and columns in the array and thanks to the angle correction made before, a simple grid can be generated so that its cells overlap with those of the array. Next, for each of these cells in the binary image, the number of non-null pixels is evaluated. Because of how the transformations are parameterized, those cells where there is a region with intensity contrast have a greater number of non-null pixels. Thus, by establishing a counting threshold, the system can distinguish when a cell is positive and when it is negative, and this information can be transferred into a binary matrix: the output of the system.

<p align="right">(<a href="#top">back to top</a>)</p>
 
## The application
 
Once we have the central component to carry out the artificial vision process, we need to build a structure that enables its deployment and connection with the rest of Omega. Wanting to solve this problem, we have been developing a source code that acts as a template for a cross-platform application, implemented to be compiled on the main operative systems found both on personal computers and mobile devices.
 
To achieve this, we used the Kivy library as the heart of IRIS. Kivy is a set of open-source tools for the development of applications and user interfaces that can be run on Linux, Windows, OS X, Android, iOS, and Raspberry Pi, allowing to generate a common code that, with minimal adaptations, can later be compiled and distributed on all these platforms. In addition, Kivy has its own graphic engine, high flexibility when it comes to communicating and integrating with other subsystems, and a wide community of developers that supports and expands it. For all these reasons, we decided to base the IRIS infrastructure on this library.
 
At the user experience level, the application shows three buttons: one to activate the camera, another to take captures, and another to stop its execution. In addition, when the camera is active, the real-time video is shown. Finally, a slot is also displayed on the screen to write the contact address that will be sent to Omega along with the processed data.
 
Regarding its ins and outs, the functionality and structure of the application are distributed as a series of classes.
 
The main class contains a method to build the interface and orchestrate the app's general workflow, being also able to stop its execution. Each of the buttons is assigned to a specific control variable, and also a clock is used for the cyclical execution of the artificial vision system and the associated subsystems.
 
The processing class contains the artificial vision system per se, with the properties and attributes explained above, and with links to communicate with the rest of the components.
 
Finally, the interface class is responsible for communicating the highest-level structures of the application, such as user interaction, with the computer vision system. This includes the rendering mechanisms that show the video signal on the screen (with specific Kivy methods, based on textures), the management of control variables according to internal processes and the data produced by the artificial vision system, the measurement of user inputs, or operating the communications module with which IRIS links to Omega.

<p align="right">(<a href="#top">back to top</a>)</p>


# About OmegaServer

OmegaCore is the source of analytical power that we need, and IRIS is the window allowing the user to translate reality into a problem on which said power can be applied. However, none of this makes any real sense if we do not build a bridge between both parties, between the human and the machine. 
 
Faced with this situation, our proposal goes through OmegaServer, an inference system in the cloud that contains the OmegaCore subunits already trained, and that is capable of communicating over the internet with the IRIS application.

![alt text](https://2021.igem.org/wiki/images/7/79/T--UPF_Barcelona--omegaA_anim.PNG)
 
With this, the idea is allowing the user to make analysis requests to Omega directly, just with the device and an internet connection.  To do so, IRIS captures the array, processes it, and we include a communication module that automatically sends the detection matrix together with an email contact address to the OmegaServer. The last then runs its analysis and sends back a written report with the results as an email.
 
Following this strategy, we consider the computational load can be better controlled and managed. Furthermore, such a structure allows for improvements in the prediction mechanisms that could be made rapidly effective for all users in a centralized way, which is key for an early development stage as ours. We have called this infrastructure prototype the Omega Architecture. In the following subsections, we explain the details and principles of its various modules.

<p align="right">(<a href="#top">back to top</a>)</p>

## Design of the Communication Architecture

The Omega Architecture is nothing more than a very simple mechanism based on sockets, which seeks to test a client-server communication between IRIS and an inference module incorporating OmegaCore’s subunits. But what is a socket? Well, the definition can change a lot depending on the context, but a socket can be understood as a structure that allows two different processes, even separated on two different machines, to exchange any flow of data, generally in a reliable, orderly, and packetized manner. Thus, these are interfaces that can work with the TCP/IP Internet protocols to enable effective communication between various devices over the network. As this is a very flexible and powerful technology, and Python integrates different native tools to manage sockets, we decided to use them as the cornerstone for our communication system. 

The first step was to adapt IRIS’ communication module for this purpose. Thus, we added a socket-based connection configuration, and two threads to run in parallel: one to receive data, and the other one to send it. The response thread listened for incoming data packets and decoded them expecting to find strings, so depending on the instruction received one specific process could be started. One of the processes, for instance, was to send the detection array, which involved using pickles to transform the objection into a stream of bytes, so it could be properly transmitted.  The writing thread simply waited for input, and when ready, encoded and sent it. Once IRIS was ready, the next step was to build the other side of the coin.

<p align="right">(<a href="#top">back to top</a>)</p>

## Creation of the Inference Server

The OmegaServer is a program that runs on a machine separated from the device on which IRIS is installed, and that is in charge of processing analysis requests coming from it. To achieve this, the system integrated a reception module to link with IRIS through the internet, a communication module to manage interactions with it and with the user, a processing module to interpret the instructions it received and carry out the pertinent tasks, and an inference module with which to analyze the incoming data and provide the desired response.   

The reception module used the socket to accept an incoming connection from IRIS. If that was the case, the system saved the reference to the client and its address, so it could be used later. Then, it starts a client-specific managing thread. The communication module, which is the function executed in the managing thread, waits for instructions from IRIS: if they are received, they are passed to the processing module, if not, it is assumed that the connection is lost, so the client data and reference are removed, and the managing process is stopped. 

Now, the processing module decodes the incoming messages and evaluates whether they are strings or not. If they are, the module will interpret them as commands, acting in a very similar way to the one shown in IRIS’s communication module. However, if the input is not a string, it is assumed that the package is in fact the detection array. Thus, the message is decoded in an alternative way, using pickles, and the tensor is then sent to inference. 

The inference module simply loads the models one by one and organizes them in a dictionary. Each model name is the target profile it should detect, so in that way, they are properly tagged. After that, its input is independently passed to each of the subunits, and the outputs are stored as a one-hot encoded vector, which is then returned. Thus, the communication module could use the information in this vector to prepare an email (using the email, smtplib, and ssl libraries) that was sent to the requester, informing on what behaviors had been identified on the sample

<p align="right">(<a href="#top">back to top</a>)</p>

## Request-based Communication Protocol

For the architecture that we have proposed to work, the communication needed to be carried out in an organized and structured way. This is important since, as the system is designed, the data to be exchanged is different depending on the situation, so both parties must be prepared to receive it properly. Furthermore, eventually, the OmegaServer would have to manage several instances of IRIS, which makes this managing issue even more complicated. 

Bearing this in mind, we proposed a simple communication protocol that would guarantee the correct sending of the necessary data, structured in the form of requests. The procedure followed these steps: first, IRIS established a direct connection with OmegaServer and started the two parallel processes: sending and receiving. Consequently, OmegaServer generated another process to handle its communication with IRIS. When IRIS performed a capture, it sent a request starting command to OmegaServer,  which answered back to IRIS asking for a contact address. 

Then, IRIS transmitted the user's contact address and a label to identify it as an email, so OmegaServer responded with an array request.  When IRIS received such instruction, it encoded the array as bytes and sent it as a data stream to OmegaServer, which decoded the message and continued with the inference process. Once this was done, IRIS closed the connection: the request had been completed.

<p align="right">(<a href="#top">back to top</a>)</p>

