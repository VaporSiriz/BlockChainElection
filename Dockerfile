FROM vaporsiriz/blockchain_election:0.1v

ADD requirements.txt /app/
WORKDIR /app

RUN apt-get update
RUN apt-get install -y python-dev libmysqlclient-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt