from web3 import Web3
import json
import os
from datetime import datetime
from solcx import compile_source, install_solc
from dotenv import load_dotenv
from eth_account.messages import encode_defunct

class BlockchainHandler:
    def __init__(self, contract_address=None):
        # Load environment variables
        load_dotenv()
        
        # Connect to Ganache
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        
        # Check connection
        if not self.w3.is_connected():
            raise Exception("Failed to connect to Ganache")
            
        # Load contract ABI and address
        self.contract_address = contract_address
        self.contract_abi = None
        self.contract = None
        
        # Get private key from environment
        private_key = os.getenv('PRIVATE_KEY')
        if not private_key:
            raise Exception("Private key not found in .env file")
        # Remove '0x' prefix if present and ensure private key is valid
        self.private_key = private_key.replace('0x', '')
        if len(self.private_key) != 64:
            raise Exception("Invalid private key length")
            
        # If contract address is provided, load the contract
        if self.contract_address:
            self._load_contract()
        
    def _load_contract(self):
        """Load the contract using the stored address"""
        try:
            # Read ABI from compiled contract
            with open(os.path.join('blockchain', 'Attendance.sol'), 'r') as file:
                contract_source = file.read()
            
            compiled_sol = compile_source(
                contract_source,
                output_values=['abi'],
                solc_version='0.8.0'
            )
            contract_id, contract_interface = compiled_sol.popitem()
            self.contract_abi = contract_interface['abi']
            
            # Create contract instance
            self.contract = self.w3.eth.contract(
                address=self.contract_address,
                abi=self.contract_abi
            )
        except Exception as e:
            print(f"Error loading contract: {str(e)}")
            raise e
        
    def deploy_contract(self, contract_path):
        """Deploy the contract to Ganache"""
        try:
            # Install solc compiler if not already installed
            install_solc('0.8.0')
            
            # Read contract source
            with open(contract_path, 'r') as file:
                contract_source = file.read()
            
            # Compile contract
            compiled_sol = compile_source(
                contract_source,
                output_values=['abi', 'bin'],
                solc_version='0.8.0'
            )
            contract_id, contract_interface = compiled_sol.popitem()
            bytecode = contract_interface['bin']
            abi = contract_interface['abi']
            
            # Create contract
            Attendance = self.w3.eth.contract(abi=abi, bytecode=bytecode)
            
            # Get account from private key
            account = self.w3.eth.account.from_key(self.private_key)
            
            # Get transaction count for nonce
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            # Build constructor transaction
            constructor_txn = Attendance.constructor().build_transaction({
                'chainId': 1337,  # Default Ganache chain ID
                'from': account.address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                constructor_txn,
                private_key=self.private_key
            )
            
            # Send raw transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            print(f"Transaction hash: {tx_hash.hex()}")
            
            # Wait for transaction receipt
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Transaction receipt received")
            
            # Get contract address and create contract instance
            self.contract_address = tx_receipt['contractAddress']
            self.contract_abi = abi
            self.contract = self.w3.eth.contract(
                address=self.contract_address,
                abi=self.contract_abi
            )
            
            print(f"Contract deployed at: {self.contract_address}")
            return self.contract_address
            
        except Exception as e:
            print(f"Error deploying contract: {str(e)}")
            raise e
        
    def mark_attendance(self, name, hash_id):
        """Mark attendance on the blockchain"""
        try:
            if not self.contract:
                raise Exception("Contract not deployed")
                
            # Get account from private key
            account = self.w3.eth.account.from_key(self.private_key)
            
            # Build transaction
            txn = self.contract.functions.markAttendance(name, hash_id).build_transaction({
                'chainId': 1337,  # Default Ganache chain ID
                'from': account.address,
                'nonce': self.w3.eth.get_transaction_count(account.address),
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                txn,
                private_key=self.private_key
            )
            
            # Send raw transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Wait for transaction receipt
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"Error marking attendance: {str(e)}")
            raise e
            
    def get_attendance_count(self):
        """Get the total number of attendance records"""
        try:
            if not self.contract:
                raise Exception("Contract not deployed")
            return self.contract.functions.getAttendanceCount().call()
        except Exception as e:
            print(f"Error getting attendance count: {str(e)}")
            return 0 