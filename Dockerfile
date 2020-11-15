FROM vaporsiriz/blockchain_election:0.1v

ADD requirements.txt /app/requirements.txt
WORKDIR /app

RUN apt-get update
RUN apt-get install lsof
RUN pip3 install -r requirements.txt
RUN /bin/bash -l -c "echo 'export PYTHONIOENCODING=utf-8' >> ~/.bashrc"
