#!/usr/bin/env bash

# Run the server interactively, with security disabled.
docker run\
  -p 8000:8000\
  -e ENABLE_SECURITY=NO\
  -e DEFAULT_USER_ID=1\
  -it\
  --name lingo-server\
  --mount type=bind,source="$(pwd)"/lingoServiceAccountKey.json,target=/app/lingoServiceAccountKey.json\
  lingo-api-server:0.0.2
