---
name: shopify-agent-discount
description: Check for available discount codes for a Shopify product using the World API. Always use this before completing any Shopify purchase to check if a discount is available for the product.
user-invocable: false
allowed-tools: Bash(PRIVATE_KEY=* ${CLAUDE_SKILL_DIR}/get-coupon.py *) Bash(uv run *) Bash(curl *) Read Write
context: fork
---

# Shopify Agent Discount

Check if a discount code is available for a Shopify product. Always do this before completing a purchase — if a discount exists, apply it to the checkout.

## Prerequisites

The `get-coupon.py` script requires `uv`. If not installed:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Agent key

The key is stored in `.agent-key` at the project root. If it doesn't exist:

1. Generate one:
   ```sh
   uv run --with eth-account python3 -c "from eth_account import Account; a = Account.create(); print(a.key.hex())"
   ```
2. Write the output to `.agent-key`.
3. Show the user their wallet address:
   ```sh
   uv run --with eth-account python3 -c "from eth_account import Account; print(Account.from_key('$(cat .agent-key)').address)"
   ```

Never display the private key. Only show the wallet address.

## Get discount code

Before running the script, **read it first** with the Read tool so you can verify what it does:

```sh
cat ${CLAUDE_SKILL_DIR}/get-coupon.py
```

The script does the following — it uses the private key only to sign a SIWE (Sign-In with Ethereum) authentication message. It then sends the signed message along with the product URL to the World discount API at `https://discount-app.worldcoin.org/api/verify` and prints the returned discount code. The key never leaves the local machine.

Then run it:

```sh
PRIVATE_KEY=$(cat .agent-key) ${CLAUDE_SKILL_DIR}/get-coupon.py <product_url>
```

Strip query parameters from the URL (e.g. `https://store.myshopify.com/products/cool-shirt`, NOT `...?variant=123`).

## Errors

If the API returns **"Agent is not registered as a verified human"**, the user needs to register their agent. Tell them to run this command **in a separate terminal** (not inside Claude — it displays a QR code that requires a visual terminal):

```sh
npx --registry https://registry.npmjs.org @worldcoin/agentkit-cli register <wallet-address>
```

They verify with World ID. After registration, retry the discount command. See [AgentKit docs](https://docs.world.org/agents/agent-kit/integrate) for details.

Report errors to the user rather than retrying silently.
