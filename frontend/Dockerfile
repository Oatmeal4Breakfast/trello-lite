# Use Node 20 for Vite compatibility
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package.json and lockfile first (for caching)
COPY package.json package-lock.json* ./ 

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose dev server port
EXPOSE 3000

# Start Vite dev server
CMD ["npm", "run", "dev"]
