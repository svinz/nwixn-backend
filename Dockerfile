FROM python:latest as base
WORKDIR /usr/src/app
COPY ./src/requirements.txt ./

RUN pip install -U --no-cache-dir pip setuptools wheel && \
    pip install --no-cache-dir Cython && \ 
    pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1

FROM base as debug
RUN pip install ptvsd
COPY ./src ./
CMD ["python", "-m", "ptvsd", "--host" , "0.0.0.0" , "--port", "5678", "--wait", "main.py" , "-config", "configfile.yml" ]
#--ssl-cert-file certs/chain.svinz.crt.pem --ssl-key-file certs/svinz.key.pem --ca certs/ca.rootCA.crt.pem
# amqps://bouvet.itsinterchange.eu:5671
# amqps://interchange-test.nordicway.net:5671
FROM base as prod
COPY ./src ./

#CMD [ "python","server.py" ]