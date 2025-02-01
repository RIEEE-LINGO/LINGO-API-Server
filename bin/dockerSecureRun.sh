#!/usr/bin/env bash

# Run the server interactively, with security enabled.
docker run\
  -p 8000:8000\
  -it\
  --name lingo-server\
  --mount type=bind,source="$(pwd)"/lingoServiceAccountKey.json,target=/app/lingoServiceAccountKey.json\
  lingo-api-server:0.0.2
