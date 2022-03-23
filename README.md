Scripts for extracting, transforming and loading data from Fullnode on Binance Smart Chain.
This should in theory work with any other network, but is tested on BSC only.

## Prerequisites

* Make sure you have access Binance Smart Chain Fullnode
  * To run your own node follow instuctions https://docs.binance.org/smart-chain/developer/fullnode.html
  * Alternatevaly you can use QuickNode, Moralis or any of your choice

## Install requirements

```
pip install -r requirements.txt
```

## Environment variables

Node Provider is by default set to `file:///home/ubuntu/node/geth.ipc`,
assuming you are running BSC node of your own. You can change that by setting
`PROVIDER_URL` or updating .env file Eg:

```
PROVIDER_URL=https://speedy-nodes-nyc.moralis.io/1234567890/bsc/mainnet
CHAIN_NETWORK=ethereum
```

## Run Scripts

```
python extract.py
```
