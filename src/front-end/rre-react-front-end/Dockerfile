# Use build argument for Node.js version
ARG NODE_VERSION

# pull official base image
FROM node:${NODE_VERSION}-alpine AS build

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json package-lock.json ./
RUN npm ci --silent

# add app
COPY . ./

# build the app
RUN npm run build

# production stage
FROM nginx:1.21.6-alpine

# copy the build output to the Nginx HTML directory
COPY --from=build /app/build /usr/share/nginx/html

# expose port
EXPOSE 80

# start nginx
CMD ["nginx", "-g", "daemon off;"]
