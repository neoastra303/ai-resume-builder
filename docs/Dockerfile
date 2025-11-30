# Documentation Dockerfile

FROM nginx:alpine

# Copy documentation files
COPY ./docs /usr/share/nginx/html/docs
COPY ./README.md /usr/share/nginx/html/
COPY ./CONTRIBUTING.md /usr/share/nginx/html/
COPY ./LICENSE /usr/share/nginx/html/

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]