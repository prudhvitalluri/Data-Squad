FROM jupyter/scipy-notebook


COPY ./app.py /deploy/
COPY ./requirements.txt /deploy/
COPY ./newfile /deploy/
COPY ./templates /deploy/templates
COPY ./Static /deploy/Static
COPY ./Completed_model.joblib /deploy

WORKDIR /deploy/
RUN pip3 install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "app.py"]