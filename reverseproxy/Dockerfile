FROM nginx:alpine as reverseproxy

COPY nginx.conf /etc/nginx/nginx.conf

CMD nginx -g 'daemon off;'