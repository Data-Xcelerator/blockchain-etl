ETL_PATH=$HOME/blockchain-etl
TMP_CRONTAB=/tmp/temp-crontab
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt update
sudo apt install ethereum
geth version || { echo 'failed to install geth' ; exit 1; }
nohup geth --cache=1024 &
git clone https://Data-Xcelerator/blockchain-etl.git $ETL_PATH || echo blockchain etl already installed
pip install -r $ETL_PATH/requirements.txt || { echo 'failed to install dependencies' ; exit 1; }
echo "00 * * * * python3 $ETL_PATH/bcetl/extract.py 2>&1 | /usr/bin/logger -t CRON" >> $TMP_CRONTAB
echo "00 * * * * python3 $ETL_PATH/blockchain-etl/bcetl/extract.py transaction 2>&1 | /usr/bin/logger -t CRON" >> $TMP_CRONTAB
cat $TMP_CRONTAB | crontab -
rm TMP_CRONTAB=/tmp/temp-crontab
echo Success! Data should be saved in $HOME/data
