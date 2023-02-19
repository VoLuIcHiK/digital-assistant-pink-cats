FROM php:apache

# Install necessary packages
RUN apt-get update && apt-get install -y wget unzip libfreetype6-dev libjpeg62-turbo-dev libpng-dev libzip-dev

# Install necessary PHP extensions
RUN docker-php-ext-install pdo_mysql mysqli gd zip

# Set the working directory to /var/www/html
WORKDIR /var/www/html

# Copy the project files from the current directory to the container's filesystem
COPY . /var/www/html

RUN chown -R www-data:www-data /var/www/html/chatbot2/chatbot/chats && \
    chmod -R 775 /var/www/html/chatbot2/chatbot/chats

# Expose port 80 for HTTP traffic
EXPOSE 80

# Start Apache
CMD ["apache2-foreground"]