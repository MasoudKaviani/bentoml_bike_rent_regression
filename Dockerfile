FROM bentoml/model-server:latest

WORKDIR /bento
COPY . /bento

RUN pip install --no-cache-dir -r requirements.txt

RUN python build_bento.py
RUN bentoml build

ENTRYPOINT ["bentoml", "serve"]