FROM node as node-builder

COPY . /home/node/app

WORKDIR /home/node/app/frontend

RUN yarn install
RUN yarn build

FROM python:3

RUN mkdir /app && mkdir /app/public

COPY . /app/
COPY  --from=node-builder /home/node/app/static /app/static

WORKDIR /app

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "manage.py", "runserver" ]
