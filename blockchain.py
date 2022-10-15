import hashlib
import json
import random
import time
import datetime
from uuid import uuid4
class Dexter_Blockchain(object):
    def __init__(self):
        #Initially the chain is empty
        self.chain = []
        #The current transactions go into this list
        self.current_transactions = []
        #Stores the amount each participant has in the blockchain
        self.balance = []
        #All the validated transactions go into this list
        self.validated_transactions = []
        self.flag = 0
        self.fog = 0
        self.indi = 0
        self.mine = 0
        self.minimum = 1000000
    def new_block(self,previous_hash=None):
        if(len(self.chain)==0):
            #Creates the genesis block
                block = {
                'index':len(self.chain) + 1,
                'timestamp':datetime.datetime.now(),
                'transactions':self.validated_transactions[:3],
                'previous_hash':0
            }
                self.chain.append(block)
                del self.validated_transactions [:3]
                #Reset the list of transactions 
                self.current_transactions = []
                print("This is the new block that got created!!")
                print(block)

        else:
        #Creates a new block and adds it to the chain.
             block = {
                'index':len(self.chain) + 1,
                'timestamp':datetime.datetime.now(),
                'transactions':self.validated_transactions[:3],
                'previous_hash':hash(self.chain[-1])
            }
             self.chain.append(block)
             del self.validated_transactions [:3]
            #Reset the list of transactions 
             self.current_transactions = []
             print("This is the new block that got created!!")
             print(block)
    def Customers_Data(self):
        self.mine = 0
        #We store the data of who owns how much in the list
        try:
            Participant = str(input("Enter the name of the participant: "))
            fund = float(input("Enter the value of currency you own: "))
            self.balance.append({
                            'Participant':Participant,
                            'Balance': fund,
                            }
                        )
            self.mine = 1
        except:
            #If the user enters wrong format of the input
            print("Enter the correct format of data!")
    def Print_Customers_data(self):
        #Prints the data of the currency each participant has
        for index in range(len(self.balance)):
                for key in self.balance[index]:
                    print(self.balance[index][key])


    def create_transaction(self):
        self.mine = 0
        #Taking the inputs of the transaction data
        try:
            sender = str(input("Enter the name of the sender: "))
            recepient = str(input("Enter the name of the receiver: "))
            amount = float(input("Enter the amount to be transferred: "))
            self.current_transactions.append({
                        #Transaction ID is a random number generated for the unique identification of the transaction
                        'Transaction_ID':str(uuid4()).replace('-', ''),
                        'Timestamp':datetime.datetime.now(),
                        'Sender':sender,
                        'Recipient':recepient,
                        'Amount': amount,
                    })
            print("The transaction is added to the current pool of transactions")
            print("........validating the following transaction")
            self.mine = 1
        except:
                #If the user does not enter the correct format of data
                print("Enter the correct format of data!!")
            
    def validate_transaction(self):
        self.flag = 0
        #We search for the sender in the customer's list 
        for high in range(len(self.balance)):
                    if(self.current_transactions[-1]["Sender"]==self.balance[high]["Participant"]):
                        for low in range(len(self.balance)):
                            #We search for the recipient in the customer's list
                            if(self.current_transactions[-1]["Recipient"]==self.balance[low]["Participant"]):
                                #If the amount to be transferred is less than the sender's balance, the transaction is invalidated
                                if(self.current_transactions[-1]["Amount"]>self.balance[high]["Balance"]):
                                    self.flag = 0;
                                    print("This transaction is invalid")
                                else:
                                   #If the amount to be transferred is more than the sender's balance,the transaction is validated and the required operations take place
                                    self.balance[high]["Balance"]-=self.current_transactions[-1]["Amount"]
                                    self.flag  = 1
                                    self.balance[low]["Balance"]+=self.current_transactions[-1]["Amount"]
                                    self.validated_transactions.append(self.current_transactions[-1])
                                    print("The transaction with the transaction ID " + self.current_transactions[-1]["Transaction_ID"] + " is validated")
       
                           
 #Proof of Elapsed time consensus algorithm uses a random timer based lottery system in order to decide the participant for the creation of the block.
    def Create_Timer(self):
            #Assigning a random timer to each of the nodes in the network
            self.minimum = 1000000
            for i in range(len(self.balance)):
                #Generating a random number using the random package of Python.We consider the number(wait time) to be between 30 and 300 seconds.
                n=random.randint(10,50)
                self.balance[i]['wait-time'] = n
                #Finding out the minimum wait time 
                self.minimum = min(self.minimum,n)
            #All the nodes go to sleep according to their wait time.As the one who wakes up first gets elected,we need the timer to go to sleep for the minimum wait time.
            print("Acheiving consensus.........................")
            #We keep the program to sleep for the specified minimum wait time in order to know the leader
            time.sleep(self.minimum)
    def Print_Leader(self):
            #We find the participant who got the least wait time
            for i in range(len(self.balance)):
                if(self.balance[i]['wait-time']==self.minimum):
                    print(self.balance[i]['Participant'],"has the least wait time and is elected as the leader for this round of consensus.")
   
  
   
#Used to validate the blockchain
def chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            #Compare the hash of the previous block and the attribute of the previous hash in the present block 
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_block = block
            block_index+=1
        return True

def hash(block):
        #Creating a SHA-256 hash of a block
        #We must make sure that the dictionary is ordered,or we will have inconsistent hashes
        block_string = json.dumps(block,sort_keys = True,default=str).encode()
        return hashlib.sha256(block_string).hexdigest()
@property
def last_block(self):
        #Returns the last block in the chain
        return self.chain[-1]

blockchain = Dexter_Blockchain()
menu = {}
menu['1']="Add a new node to the blockchain network" 
menu['2']="Create a new transaction"
menu['3']="Print the data of who owns how much"
menu['4']= "Print the existing blocks"
menu['5'] = "Exit the program"
while True: 
        options=menu.keys()
        print("Hello Dexter!!!!!!!")
        for choice in options: 
            print (choice,menu[choice])
        selection = input("Select the required operation:")
        if selection == '1':
            blockchain.Customers_Data()
            if(blockchain.mine==1):
                print("The following person was successfully added to the network")
        elif selection == '2':
            blockchain.create_transaction()
            if(blockchain.mine == 1):
                blockchain.validate_transaction()
                wish = input("Do you want the receipt of this transaction?  Yes/No  ")
                if(wish.capitalize()=="Yes"):
                        print(blockchain.validated_transactions[-1])
                else:
                        print("Thank you and visit again!")
           
    #Since the capacity of each block is three transactions 
            if(len(blockchain.validated_transactions)>=3):
                if(len(blockchain.chain)==0):
                    #Creating a Genesis Block
                    blockchain.Create_Timer()
                    blockchain.Print_Leader()
                    blockchain.new_block()
                else:
                    blockchain.Create_Timer()
                    blockchain.Print_Leader()
                    blockchain.new_block()

      

        elif selection=='3':
            blockchain.Print_Customers_data()
        elif selection=='4':
            print(blockchain.chain)
        elif selection=='5':
            break
        else:
            print("Invalid option selected!")
