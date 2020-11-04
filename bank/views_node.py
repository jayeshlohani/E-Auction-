from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from web3 import Web3
import json
from . import views
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:5000'))
# print(web3.isConnected())
# print(web3.eth.blockNumber)
# print(web3.eth.getBalance(''))

key = [] #list of ganache accounts private keys

def pay_fee(acc1,acc2,fee):
	account_1 = acc1 
	account_2 = acc2
	if(account_1 == web3.eth.accounts[0]):
		private_key = key[0]
	else:		
		private_key = key[ID]

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


################

ID = 0
contract = views.contract
# Create your views here.
def home(request,id=None):
	# print(id)
	global ID
	ID = id
	return render(request,"home_node.ejs")

def get_amount(request):
	isEnded = contract.functions.isEnded().call()
	if(isEnded==1):
		return redirect('/bank/auctioneer/result')
	else:
		# web3.eth.defaultAccount = web3.eth.accounts[ID]
		amt = int(request.POST.get('amt'))
		# print(type(amt))
		tx_hash = contract.functions.placeBid(web3.eth.accounts[ID],amt).transact()
		web3.eth.waitForTransactionReceipt(tx_hash)
		pay_fee(web3.eth.accounts[ID],web3.eth.accounts[0],amt/10)
		# n = contract.functions.get_n_participants().call()
		# print(n)
		# return render(request,"home.ejs")
		url = "/bank/bidder/"+str(ID)
		return redirect(url)

def withdraw(request,id=None):
	# print(id)
	isEnded = contract.functions.isEnded().call()
	if(isEnded==1):
		return redirect('/bank/auctioneer/result')
	else:	
		Id = id
		top_bidder = contract.functions.getTopBidder().call()
		# print(top_bidder)
		print(id)
		if(top_bidder == web3.eth.accounts[id]):
			tx_hash = contract.functions.withdraw(web3.eth.accounts[id]).transact()
			web3.eth.waitForTransactionReceipt(tx_hash)
		else:
			bid = contract.functions.getBids(web3.eth.accounts[id]).call()
			pay_fee(web3.eth.accounts[0],web3.eth.accounts[id],bid/10)
			tx_hash = contract.functions.withdraw(web3.eth.accounts[id]).transact()
			web3.eth.waitForTransactionReceipt(tx_hash)
		return redirect('/bank')

