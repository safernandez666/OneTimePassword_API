FROM python:3.6-slim

RUN python3 -m pip install --upgrade pip

ENV TZ=America/Buenos_Aires

RUN mkdir /code  
WORKDIR /code  
ADD . /code/ 

RUN pip install -r /code/requirements.txt  

EXPOSE 5000

CMD [ "python3", "/code/app.py" ]