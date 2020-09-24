FROM debian:buster-slim

# This needs to be built one directory up from here - Docker can't pull peer
# directories into the build context, so instead we assume all peer directories
# are children of the build context. Use the included build script, or run
#     docker build [...] --file container/Dockerfile .
# from the parent directory to build this image.
ADD container/prep /opt/botanist/container-prep
ADD python /opt/botanist/python

RUN /opt/botanist/container-prep/prepare

WORKDIR /app
USER app
ENTRYPOINT ["botanist", "container", "start", "--"]
CMD ["botanist", "bundle", "start"]
