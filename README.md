## Group information: 
Vishnu Praneeth Palavali - 2020A7PS0126H <br/>
Chetan  Akash Vankadara -  2020A7PS2196H <br/>
Srikanth Mangipudi -       2020A8PS1162H <br/>
Ch Sree Nihitha -          2020B4TS1384H <br/>


### Libraries and Installations needed: 
random - for using random library to assign random time values for each node with in a given specified time<br/>
ecdsa (Elliptic Curve Digital SIgnature Algorithm) - to create public and private keys for validating the new nodes<br/>
sqlite3 - for storing user details and modifying according to transactions<br/>
time - for generating timestamps and random time and sleep function<br/>
hashlib - for using SHA256 to hash the block<br/>
json - to convert the format of the message<br/>

Install ecdsa using `pip install ecdsa`

## Problem statement: 
 You buy a piece of land. Someone else claims to own the land. But the one who sold you the land
showed you the paperwork. The land registry office earlier said that the owner was rightful. Now
they say that they made a mistake – it was owned by the other person. You already paid for the
land – to the first person. The First person goes missing, how does anyone prove who changed
the land record?

## Features: 
1. New users can be registered with previously owned property. <br/>
2. The user should be able to buy and sell property. <br/>
3. To improve the security of blockchain, consensus algorithm (PoEt) has been implemented.<br/>
4. Merkle root is implemented to calculate hash of all the transactions in a block<br/>
5. Can view all the transaction history that is related to the property. <br/>

### Structure of Transaction: 
BuyerId, SellerId, PropertyId/name, Amount, Time stamp of the transaction. <br/>

### Structure of a block in blockchain: 
Timestamp, Merkle root, Hash of the previous block, Transactions(2), Proof, block index. <br/>

## Directions to use the BlockChain: 
To execute run python3 blockchain.py <br/> 
You will be given 6 options (1 to 6): Enter <br/>
'1' to register a new node and continue entering his properties. <br/>
'2' to create a transaction (Make sure there are two or more nodes before making a transaction) <br/>
'3' to check the transaction history of the property <br/>
'4' to display all the blocks of the blockchain <br/>
'5' to verify the blockchain (valid or not) <br/>
'6' to exit from the blockchain <br/> <br/>

---------------------------------------------------PoET Code Explanation---------------------------------------------------<br/>
A node  which wants to join the verified nodes has to be validated and it is done by creating private and public keys using the ECDSA library.
<br/>
The node forwards this key when requesting to join the network. The nodes that are already a part of the network verify this key.
<br/>
To select the leader of the nodes, or the node which creates the block which is linked to the existing blockchain, PoET algorithm initializes all the with a random time; the first one whose time expires becomes the winner. This means that it creates a new block. (Fairness of Algorithm is based on the randomness of the timers given to the nodes in this process.)
<br/>
Later this news is broadcasted to the remaining nodes. (In our implementation, to indicate the receiving of this news, we have reset the random time values of all the nodes to zero.)

<br/>

## Description of functions: 
  1. Reg_User() - This is a function used to take inputs from the user and validate. <br/>
    1. add_User(userId, userName, balance) - Adds the user and his properties to the users list. 
      1. validate_User(publickey, signature, userId, userName) - verifies the values of hash.  
  2. Transact() - This is a function used to take buyerId, sellerId, propertyId from the user. 
     1. add_Transact(buyerId, sellerId, propID, amount) - validates the transactions and adds it to pending list if it is correct. 
  3. transaction_history() - This function shows all the previous transactions. 
  4. display_blockchain() - This function is used to display all the blocks of the transaction. 
  5. chain_valid() - This function is used to check whether the blockchain is valid or not. 
  6. create_block() - Allots random times to each of the nodes and sleep for the minimum time (of the nodes) and calls new_block
    1. new_block(proof, prevhash = none) - calculate merkle roots and creates the block with index , timestamp, transactions, merkle root, proof, prevhash and cryptographically links it to previous block 
      1. calcate_hash(arg) - encrypts the given argument with SHA-256 and returns the hash value. 
      
  7. display_users() - This functions shows all the nodes.  
 
