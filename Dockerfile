FROM vaporsiriz/blockchain_election:0.2v

ADD requirements.txt /app/requirements.txt
WORKDIR /app

RUN apt-get update
RUN pip3 install -r requirements.txt
