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
- **Discount code** (optional): Obtained from the `shopify-agent-discount` skill. Always check for one before proceeding.

## Flow

### 1. Find the product

Use `curl -s "<product_url>.json"` (strip any query parameters first, then append `.json`) to fetch the raw product JSON. Pick the first variant from the response. Note the variant ID.

### 2. Build the checkout link

Construct the checkout URL directly:

```
https://<shop-domain>/cart/<variant_id>:1?discount=<DISCOUNT_CODE>
```

For example:
```
https://humanrequired.shop/cart/46991516106914:1?discount=WORLD-ID-abc123
```

- `<variant_id>`: The numeric variant ID from step 1 (NOT the `gid://` format — just the number).
- `:1`: Quantity of 1.
- `?discount=<DISCOUNT_CODE>`: Append only if a discount code was obtained. Omit the parameter entirely if there is no discount.

### 3. Present to the user

Share the checkout link. If a discount was applied, mention it:

> I found a human-only discount and built your cart! Complete your purchase here: {checkout_url}

If no discount was available:

> Here's your checkout link: {checkout_url}

## Output

Do not narrate each step. Only produce user-facing output at step 3, or earlier if something fails.
