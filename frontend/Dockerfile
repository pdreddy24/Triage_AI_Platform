FROM node:20-alpine AS build
WORKDIR /app
COPY frontend/package.json ./package.json
RUN npm install
COPY frontend ./
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf.template
COPY frontend/docker-entrypoint.sh /docker-entrypoint.d/99-env.sh
RUN chmod +x /docker-entrypoint.d/99-env.sh
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
