#Deriving the latest base image
FROM mcr.microsoft.com/playwright:v1.18.1-focal


#Labels as key value pair
LABEL Maintainer="mohammadjavad.farahnak"

WORKDIR /data/src
#to COPY the remote file at working directory in container
ADD . /data/src
RUN pip3 install -r requirements.txt
RUN playwright install chromium

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD ["python", "-u","app.py"]
