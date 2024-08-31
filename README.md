## How to Vote with Your Stake

Before you proceed, please read the following important note:

### ⚠️ **Important Warning:**
**DO NOT RUN CODE ON YOUR MACHINE THAT YOU HAVE NOT AUDITED FIRST!** While the provided code is safe, it's essential to follow the adage: _"Verify, don’t trust."_ Always review any code before running it, especially on a machine that holds your wallet. The last thing we want is a repeat of the hack that occurred earlier this year.

---


### Voting Options:

#### 1. Vote via [app.minersunion.com](https://app.minersunion.com) (Easiest)
- **Requirement:** Ensure your wallet is connected through the Chrome extension.

#### 2. Vote via `sign_endpoint.py` (For Users with Wallets on `btcli`)
- **Step-by-Step Instructions:**
  1. Download and run the `sign_endpoint.py` script using the following command:
     ```bash
     curl -o sign.py https://raw.githubusercontent.com/minersunion/voting/main/sign.py && python3 sign.py
     ```
  2. Follow the on-screen instructions to cast your vote for the subnet weights

---


### How it works:

#### 1. Signs a JSON string of text with your Bittensor wallet

The raw JSON looks like this:
```json
[
  {"subnet": 1, "percent": 50.0},
  {"subnet": 2, "percent": 50.0}
]
```

When it is stringified to sign, it looks like this:
`"[{\"subnet\": 1, \"percent\": 50.0}, {\"subnet\": 2, \"percent\": 50.0}]"`

#### 2. Records the signed message in our database

When the vote has been signed successfuly, we then save it securely in our database with a http POST request that looks like this:

```python
vote_data = {
  "vote_message": "[{\"subnet\": 1, \"percent\": 50.0}, {\"subnet\": 2, \"percent\": 50.0}]", 
  "signature": "", 
  "hotkey_ss58": coldkey.ss58_address
}
```


### Security Review

#### 1. Loading the Wallet
The script begins by loading a wallet that contains the private key (coldkey) necessary for signing the message. The wallet is identified by a user-specified name and path.

#### 2. Generating the Vote Message
The user inputs subnet IDs and associated percentages, which are compiled into a JSON structure representing the vote message. This message is then stringified to create a raw JSON string ready for signing.

#### 3. Signing the Vote Message
The script securely signs the JSON string of the vote message using the private key (coldkey) from the wallet. This signing process ensures that the message cannot be tampered with without detection, as the signature would no longer match.

#### 4. Verifying the Signature
To ensure the integrity of the signed message, the script verifies the signature using the corresponding public key. This verification step confirms that the message was signed with the correct private key and has not been altered.

#### 5. Preparing and Sending Data to the Server
The script packages the vote message, the signature, and the associated public key (in SS58 format) into a JSON object. This data is then securely transmitted to a server via an HTTPS POST request.

#### 6. Optional Local Storage
For record-keeping or backup purposes, the script optionally saves the signed data to a local file (`vote_data.json`). This step ensures that a copy of the signed message is available locally for reference or audit purposes.

This process securely signs a vote message, verifies its authenticity, and submits the signed message to a server, ensuring that the vote is both authenticated and securely recorded.
