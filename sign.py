import sys
import json
import logging
import requests
from bittensor import wallet as btcli_wallet
from substrateinterface import Keypair

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Define color codes
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Prompt the user for wallet details
wallet_name = input(f"{CYAN}Enter wallet name (default: Coldkey): {RESET}") or "Coldkey"
wallet_path = input(f"{CYAN}Enter wallet path (default: ~/.bittensor/wallets/): {RESET}") or "~/.bittensor/wallets/"

logger.info(f"\nUsing wallet name: {wallet_name}")
logger.info(f"Using wallet path: {wallet_path}")

# Load your wallet
my_wallet = btcli_wallet(name=wallet_name, path=wallet_path)

# Load your private key (coldkey)
try:
    coldkey = my_wallet.get_coldkey()
    logger.info("Coldkey loaded successfully.")
except Exception as e:
    logger.error(f"Error loading coldkey: {e}")
    exit(1)

# Prompt for the message details to create the JSON
print(f"{CYAN}Enter the details for the vote message:{RESET}")
subnets: list[dict[str, int | float]] = []
# Example:
# subnets = [
#     {"subnet": 1, "percent": 50.0},
#     {"subnet": 2, "percent": 50.0},
# ]

while True:
    subnet_id = input(f"{CYAN}Enter subnet ID (or press Enter to finish): {RESET}")
    if not subnet_id:
        break
    try:
        subnet_id = int(subnet_id)
    except ValueError:
        print(f"{RED}Invalid subnet ID. Please enter an integer.{RESET}")
        continue

    percent = input(f"{CYAN}Enter percentage for subnet {subnet_id}: {RESET}")
    try:
        percent = float(percent)
    except ValueError:
        print(f"{RED}Invalid percentage. Please enter a number.{RESET}")
        continue

    subnets.append({"subnet": subnet_id, "percent": percent})

if not subnets:
    print(f"{RED}No subnets entered. Exiting.{RESET}")
    exit(1)

vote_message: str = json.dumps(subnets, indent=4)
print(f"{GREEN}Generated vote message:{RESET}")
print(vote_message)

# Ensure valid JSON
try:
    json_object = json.loads(vote_message)
    logger.info("Vote message JSON is valid.")
except json.JSONDecodeError as e:
    logger.error(f"\nInvalid JSON input: {e}")
    exit(1)

# Sign the message
signature = coldkey.sign(vote_message.encode("utf-8")).hex()
logger.info("Message signed successfully.")
print(f"{GREEN}Signature: {signature}{RESET}")

# Extract the public key from the coldkey
public_key = coldkey.public_key

# Create a new keypair from the public key
keypair_from_public_key = Keypair(ss58_address=coldkey.ss58_address)

# Verify the signature
is_valid = keypair_from_public_key.verify(vote_message.encode("utf-8"), bytes.fromhex(signature))
logger.info(f"Signature verification result: {is_valid}")
print(f"{GREEN if is_valid else RED}Signature valid: {is_valid}{RESET}")

# Prepare the data to send to the server
vote_data = {"vote_message": vote_message, "signature": signature, "hotkey_ss58": coldkey.ss58_address}

# Debug print to ensure correct payload
print(f"{GREEN}Vote data to send:{RESET}")
print(json.dumps(vote_data, indent=4))

# Send the data to the server endpoint
url = "http://api.minersunion.ai/votes/process_vote/"
headers = {'Content-Type': 'application/json'}
try:
    response = requests.post(url, headers=headers, json=vote_data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    print(f"{GREEN}Vote data has been successfully sent to the server.{RESET}")
    print(f"Server response: {response.json()}")
except requests.exceptions.RequestException as e:
    logger.error(f"Error sending data to server: {e}")
    print(f"{RED}Failed to send vote data to the server.{RESET}")

# Save the data to a file (optional, if you still want to keep the local file)
with open("vote_data.json", "w") as vote_file:
    json.dump(vote_data, vote_file)

print(f"{GREEN}Vote data has been saved to vote_data.json{RESET}")
