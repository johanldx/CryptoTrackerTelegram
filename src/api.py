import blockcypher
import requests

class Crypto:
    BITCOIN = 'btc'
    ETHEREUM = 'eth'
    LITECOIN = 'ltc'
    def __init__(self):
        pass

class Blockchain:
    def __init__(self, api_key:str):
        self.api_key = api_key
    
    def check_transaction(self, transaction_id:str, coin_symbol:'Crypto'):
        try:
            details = blockcypher.get_transaction_details(transaction_id, coin_symbol, self.api_key)
        except:
            return None
        return details
    
    def convert(self, coin_symbol:'Crypto', amount:int):
        return blockcypher.from_base_unit(amount, coin_symbol)
        
if __name__ == '__main__':
    bc = Blockchain('BLOCKCYPHER_API_KEY')
    print(bc.crypto_to_eur(Crypto.BITCOIN, 0.12))