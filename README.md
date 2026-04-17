# AgentKit Shopify Demo

Unlock exclusive human-only discounts on Shopify stores using [AgentKit](https://docs.world.org/agents/agent-kit). Paste this README into a Claude Code session and Claude will handle the rest.

## Install

Prerequisites: [Node.js](https://nodejs.org/) (for the AgentKit CLI registration step).

```
/plugin marketplace add worldcoin/agentkit-shopify-demo
/plugin install agentkit-shopify@worldcoin-agentkit
```

After installing, run `/reload-plugins` so Claude picks up the new skills and MCP server.

## Usage

Once installed, just ask Claude:

> Help me purchase this product: https://humanrequired.shop/products/human-in-the-loop-hat

On your first run, Claude will walk you through one-time setup:

1. **Install dependencies** — Claude will install `uv` (Python package runner) if needed.
2. **Generate an agent key** — Claude will generate an Ethereum key pair and save it to `.agent-key`. It will show you the wallet address.
3. **Register in AgentBook** — Claude will ask you to run:
   ```sh
   npx --registry https://registry.npmjs.org @worldcoin/agentkit-cli register <your-agent-address>
   ```
   This proves your agent is backed by a real human. You'll verify with your World ID. See the [AgentKit docs](https://docs.world.org/agents/agent-kit/integrate) for details.

After registration, Claude will fetch the discount code, create a cart with the discount applied, and give you a checkout link.

## How it works

Two skills work together:

1. **`shopify-agent-discount`** — Calls the World discount API (`/api/verify`) to get a discount code for a product. Authenticates via SIWE (Sign-In with Ethereum) using the agent's key.
2. **`shopify-storefront`** — Uses the Shopify Storefront MCP (`humanrequired.shop/api/mcp`) to look up products, create a cart with the discount applied, and return a checkout link.

## Using with other frameworks

The `get-coupon.py` script is a standalone CLI tool:

```sh
PRIVATE_KEY=0x... agentkit-shopify/skills/shopify-agent-discount/get-coupon.py <product_url>
# prints the discount code to stdout
```

For the Shopify Storefront, connect to the MCP at `https://humanrequired.shop/api/mcp`.
