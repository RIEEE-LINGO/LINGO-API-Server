#!/usr/bin/env bash

# Note that, if you run this on a Mac with Apple silicon, it will not work if
# deployed to other machines. Use dockerize.sh if you need to do that.

# Update the version number if needed
docker build -t lingo-api-server:0.0.2 .