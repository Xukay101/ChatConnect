FROM node:20-slim

WORKDIR /react-vite-app

EXPOSE 3000

COPY package.json ./

RUN npm install --silent

COPY . ./

CMD ["npm", "run", "dev"]
