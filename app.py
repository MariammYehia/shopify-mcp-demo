import os
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load .env file
load_dotenv()

SHOPIFY_STORE = os.environ.get("SHOPIFY_STORE")
SHOPIFY_TOKEN = os.environ.get("SHOPIFY_TOKEN")
PORT = int(os.environ.get("PORT", 8000))

# Create MCP app (default transport)
app = FastMCP("Shopify Demo MCP Server")

# --- Shopify request helper ---
def shopify_request(method, endpoint, params=None, data=None):
    url = f"https://{SHOPIFY_STORE}/admin/api/2024-07/{endpoint}"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json"
    }
    resp = requests.request(method, url, headers=headers, params=params, json=data)
    resp.raise_for_status()
    return resp.json()

# --- MCP tools ---
@app.tool()
def get_order(order_id: str):
    return shopify_request("GET", f"orders/{order_id}.json")

@app.tool()
def refund_order(order_id: str):
    return shopify_request("POST", f"orders/{order_id}/refund.json")

@app.tool()
def get_customer(customer_id: str):
    return shopify_request("GET", f"customers/{customer_id}.json")

@app.tool()
def get_product(product_id: str):
    return shopify_request("GET", f"products/{product_id}.json")

@app.tool()
def update_shipping_address(order_id: str, address: dict):
    data = {"order": {"id": order_id, "shipping_address": address}}
    return shopify_request("PUT", f"orders/{order_id}.json", data=data)

@app.tool()
def cancel_order(order_id: str):
    return shopify_request("POST", f"orders/{order_id}/cancel.json")

# --- Run the MCP server ---
if __name__ == "__main__":
    app.run(port=PORT)
