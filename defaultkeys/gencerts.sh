# turingtest.eu

openssl genrsa -out server.key 2048
openssl req -key server.key -new -out server.csr
openssl x509 -signkey server.key -in server.csr -req -days 365 -out server.crt
