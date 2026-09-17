FROM node:24-alpine

RUN apk upgrade --no-cache

WORKDIR /app

COPY package*.json ./

RUN npm ci --omit=dev

COPY server.js ./

USER node

EXPOSE 3002

CMD ["node", "server.js"]