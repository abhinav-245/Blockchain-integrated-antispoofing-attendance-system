from blockchain.blockchain_handler import BlockchainHandler
from dotenv import load_dotenv
import os
import json

def save_contract_address(address):
    with open('contract_address.json', 'w') as f:
        json.dump({'address': address}, f)

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize blockchain handler
    blockchain = BlockchainHandler()
    
    # Deploy contract
    contract_path = os.path.join('blockchain', 'Attendance.sol')
    contract_address = blockchain.deploy_contract(contract_path)
    
    if contract_address:
        # Save contract address
        save_contract_address(contract_address)
        print(f"Contract successfully deployed at: {contract_address}")
    else:
        print("Failed to deploy contract")

if __name__ == "__main__":
    main() 