import hashlib
import json
from time import time
from time import sleep
import sqlite3 as sl
from ecdsa import SigningKey
import random

leadernode = ''
#No of transactions in a block = 2
class BlockChain(object):

    dict_obj={}
    elapsedTime_dictobj={}
    property_owner={}
    global leadernode
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.complete_transactions = []
        self.Users = []
        self.new_block(100, "Gensis block")

    def calculate_hash(self, hh):
        string_object = json.dumps(hh, sort_keys=True)
        trans_string = string_object.encode()

        raw_hash = hashlib.sha256(trans_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'merkel_root': '',
            'proof': proof,
            'transactions': self.pending_transactions,
            #Input of previous_hash necessary for genesis block / cryptographically linking the previous block
            'previous_hash': previous_hash or self.calculate_hash(self.chain[-1]),
        }
        if(len(self.pending_transactions) != 0):
            #Calculation of merkel root for the two transactions in the block
            block['merkel_root'] = self.calculate_hash(self.calculate_hash(self.pending_transactions[0]) + self.calculate_hash(self.pending_transactions[1]))
        #Confirming the pending_transactions
        for i in self.pending_transactions:
            self.complete_transactions.append(i)
        self.pending_transactions = []
        #Appending block to the list
        self.chain.append(block)
        return block
    
    def create_block(self):
        print("\nCreating a new block by Process of Leader Selection using Elapsed Time : ")
        # generate random number scaled to number of seconds in 1min
        # (1*60) = 60
        minTime=61
        for node in blockchain.elapsedTime_dictobj:
            #change 60 here accordingly to change the time range.
            rtime = int(random.random()*10)

            hours   = int(rtime/3600)
            minutes = int((rtime - hours*3600)/60)
            seconds = rtime - hours*3600 - minutes*60
            
            time_string = '%02d:%02d:%02d' % (hours, minutes, seconds)
            blockchain.elapsedTime_dictobj[node]= time_string
            # Keeping track of the node with minimum wait tiem
            if minTime>rtime:
                minTime=rtime
                leadernode=node

        print("\nDisplaying random times (in range of 1min) assigned to each node : ")
        print(blockchain.elapsedTime_dictobj)

        print("\nNodes sleeping (Time elapsing).....")
        sleep(float(minTime))
        #Reward for miner
        self.dict_obj[leadernode] += 69.0
        print("\nCreating new block")
        blockchain.new_block(minTime)

     #Validating the blockchain.
    def chain_valid(self):
        #Starting with the genesis block
        previous_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            #Current block
            block = self.chain[block_index]
            #Recalulating the hash of the previous block and matching it with the previous block hash 
            if block['previous_hash'] != self.calculate_hash(previous_block):
                return False
            block_index += 1
            #Assigning the previous block variable to current block
            previous_block = block
        return True  


    def add_Transaction(self, buyerID, sellerID, propertyID, amount):
        #Checking if Buyer and Seller and property are be registered, seller should own the property he wants to sell
            if(int(buyerID) in self.dict_obj) and (int(buyerID) != int(sellerID))and (int(sellerID) == 0 or (int(sellerID) in self.dict_obj)) and (int(sellerID) == 0 or int(propertyID) in self.property_owner) and (int(sellerID) == 0 or self.property_owner[int(propertyID)] == int(sellerID)):  
                #Checking if Buyer has sufficient amount to buy the property
                if(int(sellerID) == 0 or self.dict_obj[int(buyerID)] >= float(amount)):
                    Transaction = {
                        'buyerID': buyerID,
                        'sellerID': sellerID,
                        'propertyID': propertyID,
                        'amount': amount,
                        'timeStamp': time(),
                    }
                    self.pending_transactions.append(Transaction)
                    self.dict_obj[int(buyerID)] -= float(amount)
                    self.property_owner[int(propertyID)] = int(buyerID)
                    if(len(self.pending_transactions) < 2):
                        return Transaction
                    else:
                        #create block
                        self.create_block()
                else:
                    print('Transaction failed: Insuffiecient balance')
                    return
            elif(int(buyerID) not in self.dict_obj or int(sellerID) not in self.dict_obj):
                print('Buyer / seller not registered, register them first')
                return
            elif(int(buyerID) == int(sellerID)):
                print('Transaction failed: A user cannot be buyer and seller at the same time')
                return
            elif(int(propertyID) not in self.property_owner):
                print('Transaction failed: Property not registered under any user')
                return
            elif(self.property_owner[int(propertyID)] != int(sellerID)):
                print("Transaction failed: Seller doesn't own the property")
                return
            

    def display_Users(self):
        print('\nUsers: ')
        for i in self.Users:
            print(i)
    
    def display_blockchain(self):
        print('\nBlocks: ')
        for i in self.chain:
            print(i)

    def verify_transactions(self):
        pass

    def validate_user(self,public_key, signature, userId, userName):
        print("New Node is being validated before joining the other verified nodes...")
        #node verification
        msg=(userId + userName).encode()
        res = public_key.verify(signature, msg)
        print("Verified:", res )
        return res

    def Reg_User(self):
        print('Enter User id: ')
        userId = input()
        print('Enter User name: ')
        userName = input()
        print('Enter User amount: ')
        balance = input()
        #Check if user is already present
        for u in self.Users:
            if  u['userId'] == userId:
                print('User already present')
                return
        
        User = {
            'userId' : userId,
            'userName': userName,
            'balance': balance,
        }
        #signing the key for user verification
        msg= (userId + userName).encode()
        #Generating a random key as user's private key
        private_key = SigningKey.generate()
        #Corresponding companion key
        public_key = private_key.verifying_key
        #Signing the msg with user's private key
        sign = private_key.sign(msg)

        #validating the Node using public key
        if(self.validate_user(public_key, sign, userId, userName) is True):

            self.Users.append(User)
            #insert userId and balance in Bloackchain's dictionary object
            blockchain.dict_obj[int(userId)]=float(balance)
            blockchain.elapsedTime_dictobj[int(userId)]=0

            print("\nNew Node details added.\n")
        else:
            print("Invalid node\n")
        #Registering the properties preowned by user
        check = 1
        while(check == 1):
            print('Enter id of the property in possesion, press ! if you have no more properties left: ')
            inp = input()
            if(inp =='!'):
                check = 0
                break
            #If property is registered before, print error
            elif(int(inp) in self.property_owner):
                print('Failed: Property already exists')
            else:
                #Create a dummy transaction to register the property under the user
                self.add_Transaction(userId, 0, inp, 0)
                self.property_owner[int(inp)] = int(userId)

    def Transact(self):
        print('Enter the buyerID')
        buyerID = input()
        print('Enter the sellerID')
        sellerID = input()
        print('Enter propertyID')
        propID = input() 
        print('Enter the amount')
        amount = input()
        self.add_Transaction(buyerID, sellerID, propID, amount)

    def transaction_history(self):
        print('Enter the propertyID to see the transaction history')
        propID = input()
        if(int(propID) not in self.property_owner):
            print('Invalid propertyID')
            return
        print('Confirmed Transactions: ')
        #Searching for the property ID in the list of complete and pending transactions
        for i in self.complete_transactions:
            if i['propertyID'] == propID:
                print(i)
        print('Pending Transactions: ')
        for i in self.pending_transactions:
            if i['propertyID'] == propID:
                print(i)
        

    

blockchain = BlockChain()
loop =1
while(loop == 1):
    print('\nEnter 1 for registration, 2 to create a transaction, 3 to check transaction history of a property, 4 to display the blockchain, 5 to verify the blockchain, 6 to exit')
    c = int(input())
    if(c == 6):
        loop = 0
    elif(c == 1):
        blockchain.Reg_User()
    elif(c == 2):
        blockchain.Transact()
    elif(c == 3):
        blockchain.transaction_history()
    elif(c == 4):
        blockchain.display_blockchain()
        blockchain.display_Users()
        print('Balances of users: ')
        print(blockchain.dict_obj)
        print('Owners of properties:')
        print(blockchain.property_owner)
    elif(c == 5):
        if blockchain.chain_valid() == True:
            print('Blockchain is valid')
        else:
            print('Blockchain is not valid')
    
