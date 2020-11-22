import datetime
import json
import hashlib
from flask import Flask , jsonify

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1 , previous_hash = '0') #Genesis Block (For GB proof and previous_hash are arbitary values)

    def create_block(self, proof , previous_hash):
        block = {"index":len(self.chain)+1,
                  "timestamp" : str(datetime.datetime.now()),
                  "proof" : proof,
                  "previous_hash" : previous_hash  }

                #Previous_hash and proof we get after mining a block

        self.chain.append(block) #Appending this newly created block to the universal chain
        return block #returning because to display in postman


    def get_previous_block(self):
        return self.chain[-1]


    #Now we will be writing the proof of work which miners need to solve to get the proof so that this proof
    # is requird for the create_block function as an argument

    def proof_of_work(self,previous_proof): #To solve the proofOfWork we need the prviousProof
        new_proof = 1
        check_proof = False #Base case.. when correct proof is got it is changed into True
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() #Just for non symmetric things
            if hash_operation[:4]=='0000':
                check_proof = True
            else:
                new_proof+=1

        return new_proof  #This is the proof which is accepted by the create block function


    def hash(self,block):
        encoded_block = json.dumps(block , sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1 #For iterating stuff
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]!='0000':
                return False
            previous_block = block
            block_index+=1
        return True


