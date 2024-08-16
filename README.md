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
     curl -o sign_endpoint.py https://raw.githubusercontent.com/minersunion/supertensor/main/to_migrate/src/voting/sign.py && python3 sign_endpoint.py
     ```
  2. Follow the on-screen instructions to cast your vote with your stake.

---

