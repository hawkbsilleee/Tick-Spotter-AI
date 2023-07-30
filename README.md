# Tick-Spotter-AI
Backend (convolutional neural networks) for TickSpotter. 

## Project Description
Building a user interface for the CNN I trained to detect ticks in MLS. First, I'd like to retrain my model 
on more training data (that I got over the summer via webscraping) and improve its accuracy by tuning 
its hyperperameters. Then, I'd like to build a website to host the model. Users can visit this website, upload an image, and get predictions from my CNN. If I have time at the end, I want to increase the number of variables my nueral net takes as inputs. Right now it only takes an input image of a tick and outputs the species of tick, but ultimately I wan't the model to be able to output a likelihood that the given tick carries disease based on an image of the tick, but also variables like the location where the tick was found and how long it had been engourged.   

## Project Outcomes
List the outcomes and more specific indicators (bullet points) that your project will address.
- Abstraction: method and class structures in Flask. Managing different files running back end (python) + 
front end (html, css, javascript)
- Data analysis: datascraping tick databases includes processing json and csv files to get image files but also labels like the species and location 
- Writing 


## Project Outline
Outline the overall structure of your code.  What is the file structure?  What classes will be created?  What functions?  What is the basic process your code uses to run?

data_prep.py is the main file in this directory. It generates/organizes the dataset by accessing public tick and skin datasets, and recording the metadata in various .csv files. 

data_analysis.ipynb analyzes and graphs the distrubition of data in the current dataset, including statistics like the representation of images per class. 

model.ipynb does the machine learning, including the train, test, split of the dataset, the constructing of the CNN model, and the actual training of the model. In the future I will also do some in-depth model perfomance analysis, which will probably take place in this file.

The datasets directory stores all the .csv files which represent the images in the dataset and their attributes. Some of the files correspond to the public datasets that were used in the creation of TickSpotter's dataset, and the other csv pertain to mapping the TickSpotter dataset. 

.ipynb_checkpoints is a folder that contains the model's weights at each epoch of training.

Finally, the final training weights and full image datasets are stored on a seperate hard drive that is node included in this repository. 

## Project Timeline
Use this timeline to map out your daily goals.  To start these goals should be the major steps in your project.  They might be a little sketchy at first, but as you work through the project, you should update your goals to be more and more specific.  Your goal for the next class should be the most specific goal.

Use "Not Started", "On track", "Behind", or "Ahead" to keep track of the status of each goal.

### Thursday May 25 - **DUE DATE**
**GOAL** --> Project Complete and Presented to Class
*STATUS* --> On track

## Tuesday May 23
**GOAL** --> Start building tick spotter site 
*STATUS* --> Started developing website. Finished training rudementry CNN model.  

### Friday May 19
**GOAL** --> 
*STATUS* --> Continued working on CNN (decided to focus more on the quality of 
the AI model than web development/TickSpotter UI)

## Wednesday May 17
**GOAL** --> 
*STATUS* --> Continued working on CNN

### Monday May 15
**GOAL** --> 
*STATUS* --> Continued working on CNN

### Thursday May 11
**GOAL** --> 
*STATUS* --> Finished gathering non-tick data, started working on CNN. 

### Tuesday May 9
**GOAL** --> Finish training improved CNN on new dataset with tuned hyperperams
*STATUS* --> Continued working on compiling non-tick data. 

### Friday May 5
**GOAL** --> 
*STATUS* --> Working on compiling non-tick data. Also did data anaylsis on existing tick data.

### Wednesday May 3
**GOAL** --> 
*STATUS* --> Finished tick image component of the dataset. Need to compile non-tick data. 

### Monday May 1
**GOAL** --> Finalize improved tick (image) database 
*STATUS* --> Behind


