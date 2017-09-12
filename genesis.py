import json
import sys
import time
import requests

class Parity(object):
    def __init__(self, node_address, **kwargs):
        self.node_address = node_address
        super().__init__(**kwargs)

    def query(self, method, params=[]):
        headers = {"content-type": "application/json"}
        payload = {
            "method":method,
            "params":params,
            "id":1,
            "jsonrpc":"2.0"
        }
        response = requests.post(self.node_address, data=json.dumps(payload), headers=headers).json()

        if "error" in response:
            raise ChildProcessError("Node reported an error", response["error"])

        return response


    # def get_transaction_hashes(self, block):
    #     response = self.query("eth_getBlockByNumber", [block, False])
    #     transaction_hashes = response["result"]["transactions"]

    #     for transaction_hash in transaction_hashes:
    #         yield transaction_hash


    def get_block_by_number(self, block):
        return self.query("eth_getBlockByNumber", [block, False])
        

    def get_transaction_count(self, address):
        return self.query("eth_getTransactionCount", [address])


    def get_balance(self, address):
        return self.query("eth_getBalance", [address])


    def get_transaction_by_hash(self, hash):
        return self.query("eth_getTransactionByHash", [hash])

if __name__ == "__main__":
    node = Parity(sys.argv[1])
    never_spent = 0

    with open(sys.argv[2], 'r') as genesis_file:
        block = json.load(genesis_file)
        accounts = block["accounts"]
        for account in accounts:
            address = "0x" + account
            transaction_count = node.get_transaction_count(address)["result"]
            if transaction_count == "0x0":
                balance = int(node.get_balance(address)["result"], 16)
                never_spent += balance
                print(f"Running total, never spent: {never_spent / 10**18: ,f}")

    print(f"Final total, never spent: {never_spent / 10**18: ,f}")     
