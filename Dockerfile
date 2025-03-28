FROM bentoml/model-server:latest

RUN pip install -U pip

WORKDIR /bento
COPY requirements.txt /bento

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -U bentoml

COPY build_bento.py /bento
COPY service.py /bento
COPY bentofile.yaml /bento

RUN python build_bento.py
RUN bentoml build

CMD ["bentoml", "serve"]