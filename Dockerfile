FROM python:3.11

RUN pip install -U pip

WORKDIR /bento
COPY requirements.txt /bento

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -U bentoml

COPY build_bento.py /bento
COPY service.py /bento
COPY bentofile.yaml /bento
RUN mkdir /bento/data
COPY data/hour.csv /bento/data/hour.csv

RUN python build_bento.py
RUN bentoml build

CMD ["bentoml", "serve"]