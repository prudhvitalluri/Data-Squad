# Data-Squad

The Application is launched by web app

app.py is the main flask application and it has the basemodels and templates which is routed by using app.py file. 



changing the below line before hosting the application.
if __name__ == "__main__":
    app.run(debug = True)
    
changing the below line before hosting the application.

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)


Docker commands to create image :
FROM jupyter/scipy-notebook
COPY ./app.py /deploy/
COPY ./requirements.txt /deploy/
COPY ./newfile.pkl /deploy/
COPY ./templates /deploy/templates
COPY ./Static /deploy/Static
WORKDIR /deploy/
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "app.py"]


* Commands to commit for AWS ec-2 :
sudo yum install docker
sudo dockerd
sudo docker pull datasquad/qspredictions:latest
sudo docker run -p 80:80 datasquad/qspredictions:latest

Ngrok Commands to execute for hosting as a public webapp : 
cmd:   ngrok config add-authtoken 2ChlR8d9qnFAYm1rCnc5rpi3i72_5TuyqQx2RpBdidFGXKXhM 
cmd:   ngrok http 80 



