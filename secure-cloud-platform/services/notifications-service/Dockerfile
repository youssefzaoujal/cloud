FROM node:24-alpine3.22

WORKDIR /app

COPY package*.json ./

RUN npm ci --omit=dev

COPY server.js ./

USER node

EXPOSE 3002

CMD ["node", "server.js"]