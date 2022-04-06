.PHONY: install extract automate install_geth run_node all

ETL_PATH=$(HOME)/blockchain-etl
TMP_CRONTAB=/tmp/temp-crontab

install:
	git clone https://github.com/Data-Xcelerator/blockchain-etl.git $(ETL_PATH) || echo blockchain etl already installed && \
	pip install -r $(ETL_PATH)/requirements.txt || { echo 'failed to install dependencies' ; exit 1; } && \
	pip install -r requirements.txt

cxtract_token_transfers:
	python3 bcetl/extract.py

cxtract_trnasactions:
	python3 bcetl/extract.py transaction

automate:
	echo "00 * * * * python3 $(ETL_PATH)/bcetl/extract.py 2>&1 | /usr/bin/logger -t CRON" >> $TMP_CRONTAB && \
	echo "00 * * * * python3 $(ETL_PATH)/blockchain-etl/bcetl/extract.py transaction 2>&1 | /usr/bin/logger -t CRON" >> $TMP_CRONTAB && \
	cat $TMP_CRONTAB | crontab -
	rm $TMP_CRONTAB

install_geth:
	sudo add-apt-repository -y ppa:ethereum/ethereum && \
	sudo apt update && \
	sudo apt install ethereum && \
	geth version || { echo 'failed to install geth' ; exit 1; }

run_node:
	nohup geth --cache=1024 &

all:
	make install_geth && make install && make run_node && make automate
