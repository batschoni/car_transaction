import hashlib as hasher
import datetime as date

class block:
    #Die __init__ Definition sind die Werte welche direkt der Klasse zugeordnet werden Block(index, timestamp,...)
    #Die Werden dann an die weiter definition übergeben. self nimmt dabei keinen Wert an, sondern gibt einfach!
    #die Variablen von Block() weiter
    #Die 4 Eingaben werden an den sha Algorithmus übergeben, aufgrund dieser er den Hashcode für jeden Block generiert
  def __init__(self, index, data, previous_hash):
    self.index = index
    #self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()
  
  def hash_block(self):
    #Kreiert ein leeres Hash Objekt nach dem sha256 Alorithmus
    #Führt updates am sha objekt durch, aufgrund der Eingaben
    #.encode war nötig durch die Umstellung von Python 2 auf 3
    sha = hasher.sha256()
    sha.update(str(self.index).encode('utf-8') + 
               #str(self.timestamp).encode('utf-8') + 
               str(self.data).encode('utf-8') + 
               str(self.previous_hash).encode('utf-8'))
    return sha.hexdigest()
    #Der erste Block (genesis Block) muss manuell kreiert werden

def create_genesis_block():
    # Manually construct a block with
    # index zero and arbitrary previous hash
    return block(0, date.datetime.now(), "Genesis Block", "0")

def next_block(last_block, transactions):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  this_data = transactions
  this_hash = last_block.hash
  return block(this_index, this_timestamp, this_data, this_hash)
    