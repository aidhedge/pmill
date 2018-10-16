FROM python:3.6
EXPOSE 4830
ENV INSTALL_PATH /

RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH
COPY ./run.py run.py
COPY ./input.ipynb input.ipynb
COPY ./output.ipynb output.ipynb
# RUN pip install -r requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install jupyter
RUN python3 -m pip install papermill
# COPY ./src ./api