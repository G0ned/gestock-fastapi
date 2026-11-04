FROM node:23-alpine

WORKDIR /frontend

COPY ./frontend/package.json /frontend/
COPY ./frontend/package-lock.json /frontend/

RUN npm install

COPY ./frontend /frontend/

# Create React App sirve en el puerto 3000 con "npm start"
EXPOSE 3000

CMD ["npm", "start"]
