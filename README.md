# Botanist Container

This container can host user applications, using the botanist CLI toolchain to control execution.

## You will need

* Docker (https://docker.io/)
* Python (see ../python/README.md)

## To build

Run this from **the parent directory** (`..`), not fron this directory:

    docker build \
        --tag botanist:latest \
        --file container/Dockerfile \
        .

Or run `tools/build` from this directory.
