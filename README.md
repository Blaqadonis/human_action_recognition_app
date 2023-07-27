# Human Action Recognition Service

### Powered by 🅱🅻🅰🆀


![image](https://github.com/Blaqadonis/human_action_recognition_app/assets/100685852/10e0cc3b-b7ac-4f5d-a535-425c3d823001)






This is my 2023 MLOPs Zoomcamp course project.


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

Human Action Recognition (HAR) aims to identify human behavior. It has a wide range of applications, and therefore has been attracting increasing attention in the field of computer vision. Human actions can be represented using various data modalities, such as RGB, skeleton, depth, infrared, point cloud, event stream, audio, acceleration, radar, and WiFi signal, which encode different sources of useful yet distinct information and have various advantages depending on the application scenarios.


Consequently, lots of existing works have attempted to investigate different types of approaches for HAR using various modalities.


This project was just to build an Image Classification Model using CNN that classifies several human actions, and to turn this to a product service, using some ML/DevOps tools while observing industry best practices, as completion of the course - MLOPs Zoomcamp 2023 hosted by 
[DataTalksClub](https://www.linkedin.com/search/results/all/?fetchDeterministicClustersOnly=true&heroEntityKey=urn%3Ali%3Aorganization%3A71802369&keywords=datatalksclub&origin=RICH_QUERY_SUGGESTION&position=0&searchId=0157507a-27bf-439c-b717-8394da03a0fb&sid=6~t) 


## Downloading the data:

The data is quite heavy hence the link. Click the link below to begin download of the zip file. Extract all contents of zip file in your local directory.

 [Click Here.](https://dphi-live.s3.eu-west-1.amazonaws.com/dataset/Human+Action+Recognition-20220526T101201Z-001.zip)

## Running this service:

Everything here runs locally. If you want to try out the service, follow the steps below (You will require Git Bash CLI for the following commands):
1. Create a virtual environment. I used ```python version 3.10.11``` 
2. To create an environment with that version of python using Conda: ```conda create -n <env-name> python=3.10.11```
    Just replace ```<env-name>``` with any title you want.
3. Next:   ```conda activate <env-name>``` to activate the environment.
4. Navigate into the local directory where you extracted the zip file at. 
5. Clone this repository ``` git clone https://github.com/Blaqadonis/human_action_recognition_app.git ```
6. Run ```pip install -r requirements.txt``` to install all necessary external dependencies.
7. Create a directory and name it ```data```. Inside it cut and paste ```train``` directory and ```Training_set.csv```. This is only important if you want to run the notebook.
8. Create a directory and name it ```output```. This is important if you want to run batch deployment.
9. Cut ```test``` directory and paste into ```batch``` directory. For educative purposes, I will be using ```Testing_set.csv``` for scheduled deployment. Cut and paste that file in the ```batch``` directory.
 


 **CAVEAT:**  Use this to spin up the MLflow server:   
   ```mlflow server --backend-store-uri sqlite:///local_server.db --default-artifact-root ./artifacts --host localhost --port 5000```

   This will create a directory ```artifacts``` on your local machine, as well as the database ```local_server.db```. **Wait! Do not spin it up yet until you are ready to track runs and make use of the MLflow server. This is very important.**
  


### 1. Running the container (Dockerfile)


First, you need to have docker installed on your system. I am using a windows machine, and I have docker desktop installed on my system. If you do not have that then you should try doing that first. If you are all set and good, then proceed.
1. Navigate to ```webservice``` directory. 
2. Run ```docker build -t <service-name>:v1 .```
3. Replace ```<service-name>``` with whatever name you wish to give to the service, to build the image.
4. Run the service:    ```docker run -it --rm -p 9696:9696 <service-name>:latest```


**NOTE:** I am running this on Windows hence Waitress. If your local machine requires Gunicorn, I think the Dockerfile should be edited with something like this:


```
FROM python:3.10-slim-buster

RUN pip install -U pip 

WORKDIR /app

COPY [ "predict.py", "HARmodel_main.h5", "requirements.txt", "./" ]

RUN pip install -r requirements.txt

EXPOSE 9696 

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]
 ```


If the container is up and running, 
5. Open up a new terminal. Reactivate the Conda environment. 
6. Run ```python test.py <image-url>```


   **NOTE:**  Replace ```<image-url>``` with the url of the image you are trying to predict the human activity in it.
7. Edit it as much as you want and try out predictions on some other images of humans performing any of the 14 activities listed above.



### 2. Simple web service (server managed locally with Flask)
  
Still inside the webservice directory, you need to:    
1. Run  ```python predict.py``` to start this service.
2. Perhaps you want to use a Web Service Gateway Interface (WSGI) like Waitress or Gunicorn:
   
   ```waitress-serve --listen=0.0.0.0:9696 predict:app```           **OR**      

   ```gunicorn --bind=0.0.0.0:9696 predict:app```

3. After starting this service, open up a new terminal. Run ```python test.py <image-url>```


   **NOTE:**  Replace ```<image-url>``` with the url of the image you are trying to predict the human activity in it.
7. Edit it as much as you want, and try out predictions on some other images of humans performing any of the 14 activities listed above, to use the service.



### 3. Web service hosted and managed on MLflow servers

Still inside the webservice directory, 
1. Navigate to server.
2. Spin up the MLflow server using the command mentioned earlier.
3. Run:   ```python tracking_predict.py``` in one terminal, followed by  ```python tracking_test.py <image-url>```


   **NOTE:**  Replace ```<image-url>``` with the url of the image you are trying to predict the human activity in it.


   **Caveat:** ```register_model.py```  is a script that enters your model into the mlflow registry when you run
   
4. ```python register_model.py ```

 



### 4. Batch mode (Scheduling)


1. Navigate to ```batch```. Ensure that  ```test``` and  ```Testing_set.csv``` ,from the zip file, exist here. Also create a directory called  ```output```. This is for saving the output predictions locally. Your run will not be completed if you omit any of these steps.
2. Spin up Prefect server with  ```prefect server start```
3. In another window, set its configuration to local ```prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api```
4. Spin up the MLflow server.
5. Create and start a process pool with  ```prefect worker start -p <name_of_pool> -t process```
6. Replace ```<name_of_pool>``` with any title you want for your work pool.
7. Run:   ```python batch.py Testing_set.csv <MLflow Run ID>``` to initiate a flow. 
8. Schedule a deployment using CRON    ```python batch_deploy.py```


   I created a separate file which is just ```batch.py``` but with extra stuff. This file ```custom_batch.py``` can send you notifications straight to your inbox about the status of the run. It also contains a 
   report about the predictions for documenting. To run this, you require an email account password. This app password will provide access to your email account without revealing your actual account password. 
   For more on this >>> [Google.](https://support.google.com/mail/answer/185833?hl=en)



   If you now have your email app password, 

9. Run   ```python custom_batch.py Testing_set.csv <MLflow Run ID> update-me <your_email_address> <email_app_password>``` to initiate a flow.
   
   Replace ```<MLflow Run ID>``` with your MLflow Run ID. Same to ```<your_email_address>```  and ``` <email_app_password>``` too. 

10. Schedule a deployment    ```python custom_batch_deploy.py Testing_set.csv <MLflow Run ID> update-me <your_email_address> <email_app_password>```


    Deployment is currently scheduled to run on the first day of every month at midnight. However, you can edit the scheduled date to whenever you wish the deployment to be done. To do this, 

11. Open  ```batch_deploy.py``` with a text editor and adjust the CRON digits.


    For more on CRON, [Click Here.](https://crontab.guru/)






### 5. Monitoring


Navigate to that directory and run the notebook. Generate an Evidently report. Check for data and concept drifts.


Try this out with family, friends, colleagues, neighbours, and let me know how to improve on it.

