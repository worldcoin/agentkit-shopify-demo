---
name: shopify-storefront
description: Set up a Shopify cart and provide a checkout link. Use when the user asks to buy a product, provides a Shopify product URL to purchase, or wants to add items to a cart on a Shopify store.
user-invocable: false
allowed-tools: Bash(curl *)
context: fork
---

# Shopify Storefront Checkout

Set up a cart with a product and an optional discount code, then give the user a checkout link.

## Inputs

- **Product URL**: A Shopify product URL (e.g. `https://humanrequired.shop/products/cool-shirt`)
- **World ID discount code** (optional): Obtained from the `shopify-agent-discount` skill. Always check for one before proceeding.
- **Fixed discount code**: Always apply `AGENTSHIPPING` in addition to any World ID discount.

## Flow

### 1. Find the product

Use `curl -s "<product_url>.json"` (strip any query parameters first, then append `.json`) to fetch the raw product JSON. Pick the first variant from the response. Note the variant ID.

### 2. Build the checkout link

Construct the checkout URL directly. Always apply `AGENTSHIPPING`, and also apply the World ID discount if one was obtained. Multiple discount codes are comma-separated in a single `discount` parameter:

```
https://<shop-domain>/cart/<variant_id>:1?discount=AGENTSHIPPING,<WORLD_ID_DISCOUNT_CODE>
```

For example, with a World ID discount:
```
https://humanrequired.shop/cart/46991516106914:1?discount=AGENTSHIPPING,WORLD-ID-abc123
```

Without a World ID discount:
```
https://humanrequired.shop/cart/46991516106914:1?discount=AGENTSHIPPING
```

- `<variant_id>`: The numeric variant ID from step 1 (NOT the `gid://` format — just the number).
- `:1`: Quantity of 1.
- `?discount=AGENTSHIPPING`: Always included.
- `,<WORLD_ID_DISCOUNT_CODE>`: Append (comma-separated) only if a World ID discount code was obtained.

### 3. Present to the user

Share the checkout link. If both discounts were applied, mention it:

> I found a human-only discount and applied it along with free shipping! Complete your purchase here: {checkout_url}

If only the AGENTSHIPPING discount was applied (no World ID discount):

> I've applied a free shipping discount to your cart! Complete your purchase here: {checkout_url}

## Output

Do not narrate each step. Only produce user-facing output at step 3, or earlier if something fails.
