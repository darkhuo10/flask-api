#FROM python:3.10-slim

#WORKDIR /usr/src/app
#COPY APIRest ./
#RUN pip install --no-cache-dir -r requirements.txt
#EXPOSE 8080
#CMD ["python", "app.py"]


FROM python:3.8.18
RUN mkdir /app
WORKDIR /app
COPY APIRest ./
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py", "runserver"]
