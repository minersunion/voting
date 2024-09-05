## How to Vote for Subnet Weights with Your Stake

Before you proceed, please read the following important note:

<br>

### ⚠️ **Important Warning:**
**DO NOT RUN CODE ON YOUR MACHINE THAT YOU HAVE NOT AUDITED FIRST!** While the provided code is safe, it's essential to follow the adage: _"Verify, don't trust."_ Always review any code before running it, especially on a machine that holds your wallet. The last thing we want is a repeat of the hack that occurred earlier this year.

---
<br>

### Voting Options:

#### 1. Vote via [app.minersunion.com](https://app.minersunion.com) (Easiest)
- **Requirements:** Ensure your wallet is connected through the Chrome extension.

#### 2. Vote via `Python` (For Users with Wallets on `btcli`)
- **Requirements:** 
  - Linux or WSL
  - Python 3.10+


<br>
<br>

# Method 1: Vote via web app

User-friendly web app using your Bittensor compatible Chrome wallet extension.

YouTube demo: https://youtu.be/_0fVJ4FeyJ8?si=f3O2Vc1pOjFL8Zia


<br>
<br>

# Method 2: Vote via Python script

### Setup and run:

1. Clone the repository:
    ```sh
    git clone https://github.com/minersunion/voting.git
    cd voting
    ```

2. Create a Python venv:
    ```sh
    sudo apt install python3-venv -y
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
   ```

4. Run the python script:
    ```sh
    python sign.py
    ```

5. Follow instructions in your terminal

<br>

### How it works:

---

#### 1. Signs a JSON string of text with your Bittensor wallet

The raw JSON now includes a timestamp and looks like this:
```json
{
  "timestamp": "2024-09-05T20:36:56.716393+00:00",
  "weights": [
    {"subnet": 1, "percent": 50.0},
    {"subnet": 45, "percent": 50.0},
  ]
}
```

When it is stringified to sign, it looks like this:
`"{\"timestamp\": \"2024-09-05T20:36:56.716393+00:00\", \"weights\": [{\"subnet\": 1, \"percent\": 50.0}]}, {\"subnet\": 45, \"percent\": 50.0}]}"`

#### 2. Records the signed message in our database

When the vote has been signed successfully, we then save it securely in our database with an HTTP POST request that looks like this:

```python
vote_data = {
  "vote_message": "{\"timestamp\": \"2024-09-05T20:36:56.716393+00:00\", \"weights\": [{\"subnet\": 28, \"percent\": 50.0}, {\"subnet\": 45, \"percent\": 50.0}]}", 
  "signature": "faked85a263fdf7e410345a378baa8e694279b0c7069c89d6bfa9bd5ab42701defda054509540d38f2b71794faefff5483911ea554aad2878b61c2cf3fa01a80", 
  "hotkey_ss58": "fakezayCxXifibJyUcFrfjzqpdH1pQdqQRiKFaw9v9vfake"
}
```

### Security Review

#### 1. Loading the Wallet
The script begins by loading a wallet that contains the private key (coldkey) necessary for signing the message. The wallet is identified by a user-specified name and path.

#### 2. Generating the Vote Message
The user inputs subnet IDs and associated percentages, which are compiled into a JSON structure representing the vote message. This message now includes a timestamp and is then stringified to create a raw JSON string ready for signing.

#### 3. Signing the Vote Message
The script securely signs the JSON string of the vote message using the private key (coldkey) from the wallet. This signing process ensures that the message cannot be tampered with without detection, as the signature would no longer match.

#### 4. Verifying the Signature
To ensure the integrity of the signed message, the script verifies the signature using the corresponding public key. This verification step confirms that the message was signed with the correct private key and has not been altered.

#### 5. Preparing and Sending Data to the Server
The script packages the vote message, the signature, and the associated public key (in SS58 format) into a JSON object. This data is then securely transmitted to a server via an HTTPS POST request.

#### 6. Optional Local Storage
For record-keeping or backup purposes, the script saves the signed data to a local file (`vote_data.json`). This step ensures that a copy of the signed message is available locally for reference or audit purposes.

This process securely signs a vote message, verifies its authenticity, and submits the signed message to a server, ensuring that the vote is both authenticated and securely recorded.
