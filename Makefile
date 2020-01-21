TARANTOOL_HOME?=~/tarantool
PYTHON?=python3.6
VPYTHON?=./venv/bin/${PYTHON}

build:
	apt install -y build-essential cmake make coreutils sed \
	 autoconf automake libtool zlib1g-dev \
	 libreadline-dev libncurses5-dev libyaml-dev libssl-dev \
	 libunwind-dev libicu-dev \
	 python python-pip python-setuptools python-dev \
	 python-msgpack python-yaml python-argparse python-six python-gevent
	git clone --recursive https://github.com/tarantool/tarantool.git -b 1.10 ${TARANTOOL_HOME} || :
	cd ${TARANTOOL_HOME} && cmake . && make
	
	${PYTHON} -m venv venv
	${VPYTHON} -m pip install wheel
	${VPYTHON} -m pip install --no-cache-dir -r requirements.txt

start_tarantool_app:
	${TARANTOOL_HOME}/src/tarantool app.lua

stop_tarantool_app:
	kill -s QUIT $$(cat tarantool.pid)
