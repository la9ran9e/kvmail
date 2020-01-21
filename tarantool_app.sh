#!/usr/bin/env bash

export $(cat .env)
${TARANTOOL_HOME}/src/tarantool app.lua
