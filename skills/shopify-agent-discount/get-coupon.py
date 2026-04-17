#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "eth-account",
#     "siwe",
#     "requests",
# ]
# ///

import sys
import os
import json
import uuid
import base64
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

import requests
from eth_account import Account
from eth_account.messages import encode_defunct
from siwe import SiweMessage

ENDPOINT = os.environ.get("ENDPOINT", "https://discount-app.worldcoin.org/api/verify")
CHAIN_ID = os.environ.get("CHAIN_ID", "eip155:480")

if len(sys.argv) < 2:
    print("Usage: ./get-coupon.py <product_url>", file=sys.stderr)
    sys.exit(1)

product_url = sys.argv[1]

private_key = os.environ.get("PRIVATE_KEY")
if not private_key:
    print("PRIVATE_KEY env var is required", file=sys.stderr)
    sys.exit(1)

account = Account.from_key(private_key)
domain = urlparse(ENDPOINT).hostname
numeric_chain_id = int(CHAIN_ID.split(":")[1])

nonce = uuid.uuid4().hex
now = datetime.now(timezone.utc)
issued_at = now.isoformat()
expiration_time = (now + timedelta(minutes=5)).isoformat()

siwe_message = SiweMessage(
    domain=domain,
    address=account.address,
    uri=ENDPOINT,
    version="1",
    chain_id=numeric_chain_id,
    nonce=nonce,
    issued_at=issued_at,
    expiration_time=expiration_time,
)

message = siwe_message.prepare_message()
signed = account.sign_message(encode_defunct(text=message))
signature = "0x" + signed.signature.hex()

payload = {
    "domain": domain,
    "address": account.address,
    "uri": ENDPOINT,
    "version": "1",
    "chainId": CHAIN_ID,
    "type": "eip191",
    "nonce": nonce,
    "issuedAt": issued_at,
    "expirationTime": expiration_time,
    "signature": signature,
}

header_value = base64.b64encode(json.dumps(payload).encode()).decode()

res = requests.post(
    ENDPOINT,
    json={"product_url": product_url},
    headers={"agentkit": header_value},
)

data = res.json()

if not res.ok:
    print(f"Error: {data.get('error', 'Unknown error')}", file=sys.stderr)
    sys.exit(1)

print(data["discount_code"])
