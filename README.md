# Human Action Recognition Service by 🅱🅻🅰🆀


![image](https://github.com/Blaqadonis/human_action_recognition_app/assets/100685852/10e0cc3b-b7ac-4f5d-a535-425c3d823001)






This is my MLOPs Zoomcamp 2023 cohort's course project.


## Understanding the service:
This is a classification service. It reads an image and classifies the human activity in it as one of the following: 


       sitting   
       using laptop
       hugging
       sleeping
       drinking
       clapping
       dancing
       cycling
       calling
       laughing
       eating
       fighting
       listening to music
       running, and
       texting 
    
    
Data collated for these 14 actions only.  


## Problem Statement:

Human Action Recognition (HAR) aims to identify human behavior. It has a wide range of applications, and therefore has been attracting increasing attention in 


the field of computer vision. Human actions can be represented using various data modalities, such as RGB, skeleton, depth, infrared, point cloud, event stream, 


audio, acceleration, radar, and WiFi signal, which encode different sources of useful yet distinct information and have various advantages depending on the 


application scenarios.


Consequently, lots of existing works have attempted to investigate different types of approaches for HAR using various modalities.


This project was just to build an Image Classification Model using CNN that classifies several human actions, turn this to a production pipeline, try out 



different deployment modes, and to make use of some of the MLOPs tools we used in MLOPs Zoomcamp 2023 cohort course for the completion of the course hosted by 
[DataTalksClub](https://www.linkedin.com/search/results/all/?fetchDeterministicClustersOnly=true&heroEntityKey=urn%3Ali%3Aorganization%3A71802369&keywords=datatalksclub&origin=RICH_QUERY_SUGGESTION&position=0&searchId=0157507a-27bf-439c-b717-8394da03a0fb&sid=6~t) 


## Downloading the data:

The data is quite heavy hence the link. Click the link to begin download of the zip file. Extract all contents of zip file in your local directory.

 [Click Here.](https://dphi-live.s3.eu-west-1.amazonaws.com/dataset/Human+Action+Recognition-20220526T101201Z-001.zip)

## Running this service:

Everything here runs locally. If you want to try out the service, follow the steps below:

Before you proceed, create a virtual environment. I used ```python version 3.10.11``` 

To create an environment with that version of python using Conda: ```conda create -n <env-name> python=3.10.11```

Just replace ```<env-name>``` with any title you want. 

Next:


 ```conda activate <env-name>``` to activate the environment.

Navigate into the local folder where you extracted the zip file at. 

Clone this repository ``` git clone https://github.com/Blaqadonis/human_action_recognition_app.git ```
 

Run ```pip install -r requirements.txt``` to install all necessary external dependencies.


 
Next, spin up the MLflow server with:

```mlflow server --backend-store-uri sqlite:///local_server.db --default-artifact-root ./artifacts --host localhost --port 5000```

This will create a folder ```artifacts``` on your local machine, as well as the database ```local_server```.



### 1. Running the container (Dockerfile)


First, you need to have docker installed on your system. I am using a windows machine, and I have docker desktop installed on my system. 


If you do not have that then you should try doing that first. If you are all set and good, then proceed.


Navigate to webservice directory.


Next, Run ```docker build -t <service-name>:v1 .```


Replace ```<service-name>``` with whatever name you wish to give to the service, to build the image.


Then run the service:    ```docker run -it --rm -p 9696:9696 <service-name>:latest```


NOTE: I am running this on Windows hence Waitress. If your local machine requires Gunicorn, I think the Dockerfile should be edited with something like this:


```
FROM python:3.10-slim-buster

RUN pip install -U pip 

WORKDIR /app

COPY [ "predict.py", "HARmodel_main.h5", "requirements.txt", "./" ]

RUN pip install -r requirements.txt

EXPOSE 9696 

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]
 ```


If the container is up and running, open up a new terminal. Reactivate the Conda environment. 


Run ```python test.py```


NOTE: ```test.py``` is an example of data you can send to the ENTRYPOINT to interact with the service. This data is expected to be an image url.


Edit it as much as you want and try out predictions on some other images of humans performing any of the 14 activities listed above.



### 2. Simple web service (server managed locally with Flask)
  
Still inside the webservice directory, you need to run:    ```python predict.py``` to start this service.

Open up a new terminal. Run ```python test.py``` to interact with the service.


### 3. Web service hosted and managed on MLflow servers

Still inside the webservice directory, 


run ```python tracking_predict.py``` in one terminal, followed by 


```python tracking_test.py``` in another terminal.




**Caveat** ```register_model.py```  is a script that enters your model into the mlflow registry when you run 


```python register_model.py ```

 



### 4. Batch mode (Scheduling)


Navigate to batch directory. Spin up Prefect server with  ```prefect server start```


In another window, set its configuration to local ```prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api```


Next, create and start a process pool with  ```prefect worker start -p <name_of_pool> -t process```



Replace ```<name_of_pool>``` with any title you want for your work pool.


Run:  


```python batch.py <path/to/Testing_set.csv> <MLflow Run ID>``` to initiate a flow. 



Then schedule a deployment using CRON    ```python batch_deploy.py```


Replace ```<path/to/Testing_set.csv>``` with path to your test file, and ```<MLflow Run ID>``` with your MLflow Run ID.


For educative purposes, I am using the test data for offline batch deployment.


Deployment is currently scheduled to run every month at midnight. However, you can edit the scheduled date to whenever you wish the deployment to be done. 


To do this, open  ```batch_deploy.py``` with a text editor and adjust the CRON digits.


For more on CRON, [Click Here.](https://crontab.guru/)






Try this out with family, friends, colleagues, neighbours, and let me know how to improve on it.

