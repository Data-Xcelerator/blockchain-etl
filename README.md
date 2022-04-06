Scripts for extracting, transforming and loading data from Fullnode on Ehtereum and Binance Smart Chain.

## How it works

Current scripts extract 2 different types of data.

* Token transfers
* Transactions

Script will collect all the data for the given hour (rounded down) and hour earlier.
Eg if it is 15:03 scripts will collect the data for 14:00-15:00. Data is saved in

* `data/extracted/token_transfers/[date]/[hour-ago]-[current-hour].csv`
* `data/extracted/transactions/[date]/[hour-ago]-[current-hour].csv`

## Prerequisites

We assume the you have `geth` installed and already running blockchain node.
However if not you can install and start it by running

```
make install
make run_node
```

**Important:** This will start a full Ehtereum blockchain node, that requirements
Big computational power and disk space. Be aware what are you doing.

## Install requirements

```
pip install -r requirements.txt
```

## Run Scripts

To run script for extracting token data

```
python extract.py tokens
```

To run script for extracting transfers data

```
python extract.py tokens
```

## Automation

Assuming you have server running on AWS VM (or any other). All you need is to
ssh into the VM, clone the repo and run `make all` command. Eg

```
ssh -i "very_secret.pem" ubuntu@ec2-01-23-456-789.compute-1.amazonaws.com
git clone https://github.com/Data-Xcelerator/blockchain-etl && cd blockchain-etl
make all
```

This will take care of

* Installing geth
* Starting the Ethereum node
* Install remaining dependencies
* Setup cron Job that runs hourly
* Save the data in the `/data` directory

## Debugging

blockchain logs saved in `nohup.out`

```
tail -f nohup.out
```

Script logs are saved in `/var/log/syslog`

```
tail -f /var/log/syslog
```
