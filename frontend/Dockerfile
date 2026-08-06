FROM node:23-alpine

WORKDIR /frontend

COPY ./frontend/package.json /frontend/
COPY ./frontend/package-lock.json /frontend/

RUN npm install

COPY ./frontend /frontend/

EXPOSE 5173 

CMD ["npm", "run", "dev", "--", "--host"]