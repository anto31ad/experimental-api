#!/bin/sh

CONSUL_HOST=${CONSUL_HOST:-"consul-server"}
CONSUL_PORT=${CONSUL_PORT:-"8500"}
NGINX_TEMPLATE_FILE=${NGINX_TEMPLATE_FILE:-"/etc/consul-template/templates/nginx.conf.ctmpl"}
NGINX_CONFIG_FILE=${NGINX_CONFIG_FILE:-"/etc/nginx/nginx.conf"}

# Correct way: use -exec to start and manage the Nginx process.
# When the template changes, consul-template will send a SIGHUP signal to the child process.
/usr/local/bin/consul-template \
    -consul-addr="${CONSUL_HOST}:${CONSUL_PORT}" \
    -template="${NGINX_TEMPLATE_FILE}:${NGINX_CONFIG_FILE}" \
    -exec "/usr/sbin/nginx -g 'daemon off;'"