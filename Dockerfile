FROM vaporsiriz/blockchain_election:0.3v

ADD requirements.txt /app/requirements.txt
WORKDIR /app

RUN apt-get update
RUN pip3 install -r requirements.txt

ADD ./conf/supervisor_server.conf /etc/supervisor/supervisord.conf
ADD ./conf/uwsgi.ini /app
ADD ./conf/nginx.conf /etc/nginx/conf.d/

EXPOSE 8000

