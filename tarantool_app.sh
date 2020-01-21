#!/usr/bin/env bash

export $(cat .env)
~/tarantool/src/tarantool app.lua
