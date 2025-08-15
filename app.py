import os
import requests
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load our .env file (Shopify store + token)
load_dotenv()

SHOPIFY_STORE = os.environ.get("SHOPIFY_STORE")
SHOPIFY_TOKEN = os.environ.get("SHOPIFY_TOKEN")

# Create the MCP app
app = FastMCP("Shopify Demo MCP Server")


# Function to make requests to Shopify
def shopify_request(method, endpoint, params=None, data=None):
    url = f"https://{SHOPIFY_STORE}/admin/api/2024-07/{endpoint}"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json"
    }
    resp = requests.request(method, url, headers=headers, params=params, json=data)
    resp.raise_for_status()
    return resp.json()
    

# --- MCP tool ---
@app.tool()
def get_order(order_id: str):
    """
    Get details for an order by Shopify order ID.
    Example: get_order("123456789")
    """
    return shopify_request("GET", f"orders/{order_id}.json")

@app.tool()
def refund_order(order_id: str):
    """
    Refund an order by Shopify order ID.
    Example: refund_order("123456789")
    """
    return shopify_request("POST", f"orders/{order_id}/refund.json")
@app.tool()
def get_customer(customer_id: str):
    """
    Get customer details by Shopify customer ID.
    Example: get_customer("987654321")
    """
    return shopify_request("GET", f"customers/{customer_id}.json")
@app.tool()
def get_product(product_id: str):
    """
    Get product details by Shopify product ID.
    Example: get_product("123456")
    """
    return shopify_request("GET", f"products/{product_id}.json")
@app.tool()
def update_shipping_address(order_id: str, address: dict):
    """
    Update the shipping address for an order.
    Address example:
    {
        "first_name": "John",
        "last_name": "Doe",
        "address1": "123 Street",
        "city": "Dublin",
        "province": "Leinster",
        "zip": "D02X285",
        "country": "Ireland"
    }
    """
    data = {"order": {"id": order_id, "shipping_address": address}}
    return shopify_request("PUT", f"orders/{order_id}.json", data=data)

@app.tool()
def cancel_order(order_id: str):
    """
    Cancel an order by Shopify order ID.
    Example: cancel_order("123456789")
    """
    return shopify_request("POST", f"orders/{order_id}/cancel.json")

# --- Run the MCP server ---
if __name__ == "__main__":
    # Use host 0.0.0.0 and the port provided by Render
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
