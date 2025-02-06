FROM python:3.12

ADD mfaAPI.py .

RUN pip install -r requirements.txt