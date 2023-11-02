###########################################
# Project:    Watch detection             #
# Author:     Alfonso Medela              #
# Contact     alfonso@alfonsomedela.com   #
# Copyright:  alfonsomedela.com           #
# Website:    https://alfonsomedela.com   #
###########################################

FROM python:3.7-slim

RUN mkdir /streamlit

COPY requirements.txt /streamlit

WORKDIR /streamlit

RUN pip install -r requirements.txt

COPY . /streamlit

EXPOSE 8018

CMD ["streamlit", "run", "main.py",  "--server.port", "8018"]