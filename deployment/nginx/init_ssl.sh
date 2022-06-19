#!/bin/bash

if [[ -f deployment/certs/cert.pem && -f deployment/certs/key.pem ]]; then
    echo "SSL Certificates already generated"
else
    openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -keyout deployment/certs/key.pem -out deployment/certs/cert.pem
fi