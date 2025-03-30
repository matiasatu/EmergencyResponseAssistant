# Build with:   docker build -t IMAGE_NAME .
# Run with:     docker run -p 3000:3000 --rm --name IMAGE_NAME IMAGE_NAME

FROM node:20-alpine

WORKDIR /usr/src/app

# COPY rollup.config.js ./
COPY package*.json ./

RUN npm install

COPY . .
# COPY ./public ./public

# RUN npm run build

EXPOSE 5173

ENV HOST=172.17.0.2
# RUN chown -R node:node /usr/src/app/src/

# USER node

CMD [ "npm", "run", "dev", "--", "--host"]