import sqlite3
import json
import os
from api import Crypto

class Database:
    def __init__(self, name:str='database'):
        self.file_name = name
        self._init_database(file_name=self.file_name)
    
    def _init_database(self, file_name:str):
        if not os.path.exists(f"{file_name}.json"):
            data = {}
            with open(f"{file_name}.json", 'w') as database:
                json.dump(data, database, indent=4)
        self.file_name = self.file_name + '.json'
    
    def get(self):
        with open(self.file_name, 'r') as database:
            return json.load(database)
        
    def write(self, data:dict):
        with open(self.file_name, 'w') as database:
            json.dump(data, database)
  
  
class User:
    def __init__(self, user_id:int):
        self.user_id = str(user_id)
        
        self._db = Database() 
        self._init_user()
        
    def _init_user(self):
        data = self._db.get()
        if self.user_id not in data:
            data[self.user_id] = []
            self._db.write(data)
    
    def get_all_informations(self):
        data = self._db.get()
        return data[self.user_id]   
    
    def delete(self):
        data = self._db.get()
        del data[self.user_id]
        self._db.write(data)
            
    def get_all_transactions(self, all:bool=True):
        data = self._db.get()
        return data[self.user_id]
    
    def get_transaction(self, txid:str):
        data = self._db.get()
        for transaction in data[self.user_id]:
            if transaction[0].startswith(txid):
                return transaction
        return None
    
    def add_transaction(self, txid:str, coin_symbol:'Crypto', finished:bool, name:str):
        data = self._db.get()
        data[self.user_id].append((txid, {'name': name, 'coin_symbol': coin_symbol, 'finished': finished}))
        self._db.write(data)
        return True
        
    def del_transaction(self, txid:str):
        data = self._db.get()
        for i in range(len(data[self.user_id])):
            if data[self.user_id][i][0].startswith(txid) or data[self.user_id][i][0] == txid:
                data[self.user_id].remove(data[self.user_id][i])
                self._db.write(data)
                return True
        return False
        
                
if __name__ == '__main__':
    user = User(123)
    user.add_transaction(txid='1234',
                         coin_symbol=Crypto.BITCOIN,
                         finished=None)
    user.del_transaction('1234')
    user.delete()