FROM node:17.2-alpine

RUN [ "mkdir", "-p", "/usr/src/app" ]

WORKDIR /usr/src/app

ENV PATH /usr/src/app/node_modules/.bin:$PATH

COPY package.json /usr/src/app/package.json

COPY package-lock.json /usr/src/app/package-lock.json

RUN [ "npm", "install", "--production" ]

COPY . /usr/src/app
