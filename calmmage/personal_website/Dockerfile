# Use an official Node.js runtime as the base image
FROM node:21-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package.json ./

# Install the dependencies in the container
RUN npm install
RUN npm i sharp

# Copy the rest of the application to the working directory
COPY . .

EXPOSE 9006

ENV PORT 9006
# set hostname to any interface
ENV HOSTNAME "0.0.0.0"

RUN npm run build

# Run the application
CMD ["npm", "run", "start"]
