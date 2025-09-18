FROM docker.io/nginx:stable

RUN apt-get update && apt-get install -y curl unzip openssl wget

# Download and install consul-template
# Check https://releases.hashicorp.com/consul-template/ for the latest version
ENV CONSUL_TEMPLATE_VERSION="0.30.0"
RUN wget -q https://releases.hashicorp.com/consul-template/${CONSUL_TEMPLATE_VERSION}/consul-template_${CONSUL_TEMPLATE_VERSION}_linux_amd64.zip && \
    unzip consul-template_${CONSUL_TEMPLATE_VERSION}_linux_amd64.zip -d /usr/local/bin && \
    rm consul-template_${CONSUL_TEMPLATE_VERSION}_linux_amd64.zip

# Create a directory for consul-template configurations and templates
RUN mkdir -p /etc/consul-template/templates \
           /etc/consul-template/config

# Copy the startup script into the container and make it executable
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Set the entrypoint to the new script
ENTRYPOINT ["/docker-entrypoint.sh"]

# Expose port 80 for HTTP traffic
EXPOSE 80
