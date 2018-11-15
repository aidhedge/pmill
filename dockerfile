FROM python:3.6
EXPOSE 5000
ENV INSTALL_PATH /

RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH
COPY . .
RUN pip install -r requirements.txt
