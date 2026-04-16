---
name: shopify-storefront
description: Set up a Shopify cart and provide a checkout link. Use when the user asks to buy a product, provides a Shopify product URL to purchase, or wants to add items to a cart on a Shopify store.
user-invocable: false
allowed-tools: Bash(curl *) mcp__human-required-store__search_shop_catalog mcp__human-required-store__update_cart mcp__human-required-store__get_cart
context: fork
---

# Shopify Storefront Checkout

Set up a cart with products and an optional discount code using the Storefront MCP, then give the user a checkout link to complete the purchase.

## Inputs

- **Product URL**: A Shopify product URL (e.g. `https://store.myshopify.com/products/cool-shirt`)
- **Discount code** (optional): Obtained from the `shopify-agent-discount` skill. Always check for one before proceeding.

## Flow

### 1. Find the product

Use `curl -s "<product_url>.json"` (strip any query parameters first, then append `.json`) to fetch the raw product JSON. If the user provided a `?variant=` query parameter, use that variant ID. Otherwise, pick the first variant from the response. The variant ID for the cart is `gid://shopify/ProductVariant/<id>`.

### 2. Create cart with product and discount

If you don't know the user's email and country code, ask them first. If you have access to a tool to ask questions to the user, use that. Otherwise, ask them normally via text.

Use `update_cart` with NO `cart_id` (creates a new cart). You MUST include the discount code in the `discount_codes` field when creating the cart — never tell the user to apply it themselves:

```json
{
	"add_items": [
		{
			"product_variant_id": "<variant_id>",
			"quantity": 1
		}
	],
	"discount_codes": ["<DISCOUNT_CODE>"],
	"buyer_identity": {
		"email": "...",
		"country_code": "..."
	}
}
```

Omit `discount_codes` only if no discount code was found. The checkout link from `get_cart` will already have the discount applied — the user should never need to enter it manually.

### 3. Get the checkout link

Call `get_cart` with the cart ID returned from `update_cart`. The response includes the checkout URL with the discount already applied.

### 4. Present to the user

Share the checkout link. If a discount was applied, mention it:

> I found a discount code and set up your cart! Complete your purchase here: {checkout_url}

If no discount was available:

> I've added the product to your cart. Complete your purchase here: {checkout_url}

## Output

Do not narrate each step. Make all tool calls silently and only produce user-facing output at the end (step 4), or earlier if something fails.
