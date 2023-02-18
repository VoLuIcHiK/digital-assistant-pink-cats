# Use an official OpenServer image as the base image
FROM ospanel/ospanel:latest

# Copy the project files from the current directory to the container's filesystem
COPY . /home/openserver/OSPanel/domains/project

# Expose port 80 for HTTP traffic
EXPOSE 80

# Start OpenServer and run the "project" folder
CMD ["/usr/bin/ospanel", "start", "project"]