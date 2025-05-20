# Etapa 1: Build com Node
FROM node:20 AS build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Garante que os arquivos do vite tenham permissão de execução
RUN chmod +x node_modules/.bin/vite

# Coloca node_modules/.bin no PATH
ENV PATH="/app/node_modules/.bin:$PATH"

RUN npm run build

# Etapa 2: Servir com Nginx
FROM nginx:alpine AS production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
