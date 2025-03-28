FROM bentoml/model-server:latest

RUN pip install -U pip

WORKDIR /bento
COPY requirements.txt /bento

RUN pip install --no-cache-dir -r requirements.txt

COPY . /bento

RUN python build_bento.py
RUN bentoml build

ENTRYPOINT ["bentoml", "serve"]