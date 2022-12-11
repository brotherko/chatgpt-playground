FROM node:16-alpine as build-stage
WORKDIR /tmp
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.22.1-alpine
WORKDIR /usr/share/nginx/html
COPY --from=build-stage /tmp/build .
ENTRYPOINT ["nginx", "-g", "daemon off;"]


