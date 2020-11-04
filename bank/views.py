from django.shortcuts import render, HttpResponse, redirect

from web3 import Web3
import json
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:5000'))

# print(web3.isConnected())
# print(web3.eth.blockNumber)
# print(web3.eth.getBalance(''))

abi = json.loads('') #ABI code form remix
bytecode = ""  #byte code from remix
# contract = web3.eth.contract(address=address, abi=abi)

c1 = web3.eth.contract(abi=abi, bytecode=bytecode)
# print(contract.functions.getBalance().call())

web3.eth.defaultAccount = web3.eth.accounts[0]

tx_hash = c1.constructor().transact()

tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
contract = web3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi,
)

key = []  #list of ganache accounts private keys

def pay_fee(acc1,acc2,val,fee):
	account_1 = acc1 
	account_2 = acc2
	if(account_1 == web3.eth.accounts[0]):
		private_key = key[0]
	else:		
		private_key = key[val]

	nonce = web3.eth.getTransactionCount(account_1)

	tx = {
	    'nonce': nonce,
	    'to': account_2,
	    'value': web3.toWei(fee, 'ether'),
	    'gas': 2000000,
	    'gasPrice': web3.toWei('50', 'gwei'),
	} 
	signed_tx = web3.eth.account.signTransaction(tx, private_key)
	tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)


# Create your views here.

def hello(request):
	return render(request,"select.html")

def home(request):	
	isEnded = contract.functions.isEnded().call()
	if(isEnded==1):
		return redirect('/bank/auctioneer/result')
	else:	
		n = contract.functions.get_n_participants().call()
		# print(n)
		bid_list = []
		bidAmt_list = []
		for i in range(n):
			bid_list.append(contract.functions.viewBids(i).call())
		for addr in bid_list:
			bidAmt_list.append(contract.functions.getBids(addr).call())	
		res = []
		for i in range(n):
			res.append(str(bid_list[i]) +" - "+str(bidAmt_list[i])+" ETH")
		return render(request,"home.ejs", {'bid_list': res})

end_flag=0
def end(request):
	global end_flag
	top_bidder = contract.functions.getTopBidder().call()
	if(end_flag==0):
		n = contract.functions.get_n_participants().call()
		bid_list = []
		bidAmt_list = []
		for i in range(n):
			x = contract.functions.viewBids(i).call()
			if(x != top_bidder):
				bid_list.append(x)	
		for addr in bid_list:
			bidAmt_list.append(contract.functions.getBids(addr).call())	
		for i in range(len(bid_list)):
			for j in range(5):
				if(bid_list[i] == web3.eth.accounts[j]):
					pay_fee(web3.eth.accounts[0],bid_list[i],j,bidAmt_list[i]/10)
					break			
		highest_bid = contract.functions.getBids(top_bidder).call()
		highest_bid -= highest_bid/10
		for j in range(5):
				if(top_bidder == web3.eth.accounts[j]):
					pay_fee(top_bidder,web3.eth.accounts[0],j,highest_bid)
		tx_hash = contract.functions.setEnd().transact()
		web3.eth.waitForTransactionReceipt(tx_hash)
		end_flag = 1			
	
	top_bidder = str(top_bidder)+" - "+str(contract.functions.getBids(top_bidder).call()) + " ETH"

	return render(request,"result.ejs",{'winner' : top_bidder})