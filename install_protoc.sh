wget https://github.com/google/protobuf/releases/download/v3.4.0/protoc-3.4.0-linux-x86_64.zip
unzip protoc-3.4.0-linux-x86_64.zip -d protoc3 && \
mv protoc3/bin/* /usr/bin/ && \
mv protoc3/include/* /usr/include/ && \
rm -rf protoc*
