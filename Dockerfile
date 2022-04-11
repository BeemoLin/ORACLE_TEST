FROM ubuntu:18.04


RUN apt-get update \
    &&  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
    
RUN TZ=Asia/Taipei \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata 

RUN apt-get update && apt-get install -y --no-install-recommends git software-properties-common vim
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update

# Set the locale in container
RUN apt-get install -y locales
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN apt-get install -y libpq-dev build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y curl postgresql postgresql-contrib


# Installing Oracle instant client
WORKDIR    /opt/oracle
RUN        apt-get update && apt-get install -y libaio1 wget unzip \
            && wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip \
            && unzip instantclient-basiclite-linuxx64.zip \
            && rm -f instantclient-basiclite-linuxx64.zip \
            && cd /opt/oracle/instantclient* \
            && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci \
            && echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf \
            && ldconfig

RUN mkdir -p /home
WORKDIR /home

COPY src /home/src
COPY requirements.txt requirements.txt

# update pip
RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install -r requirements.txt


WORKDIR /home/

#ENTRYPOINT ["python3", "app.py"]

