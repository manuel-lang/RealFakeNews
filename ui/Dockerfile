FROM node:10
 
WORKDIR /usr/src/app
 
COPY package*.json ./
 
RUN npm install
 
COPY . .
 
EXPOSE 8083
 
CMD [ "npm", "start" ]