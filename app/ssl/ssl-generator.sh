#!/bin/bash

# Usage (ex): bash ssl-generator.sh server-python
# $1 == keyfile name (ex: server-python)

if [ -a /usr/bin/openssl ] ; then

    if [ -n "$1" ] ; then
        echo -e "\nFilename: $1\n"
        read -p "SSL Password (use speacial characters, for better security): " pass
        echo    
        echo -e "\n* Generating RSA Private Key ($1.key)"
        sudo openssl genrsa -des3 -out "$1".key -passout pass:"$pass" 2048
        echo -e "\n* Generating Certificate Signing Request ($1.csr)"
        sudo openssl req -batch -new -key "$1".key -out "$1".csr -config ssl-config -passin pass:"$pass"
        echo -e "\n* Removing passphrase from RSA Private Key ($1.key)"
        cp "$1".key "$1".key.org
        sudo openssl rsa -in "$1".key.org -out "$1".key -passin pass:"$pass"
        rm "$1".key.org
        echo -e "\n* Generating Self-Signed Certificate ($1.crt)"
        sudo openssl x509 -req -days 365 -in "$1".csr -signkey "$1".key -out "$1".crt
        echo
    else
        echo -e "\n Must pass [certificate name]. Ex.: $0 server-apache \n"
        exit 0
    fi

else
    echo -e "\nMust install openssl package. Exiting...\n"
fi
