import json
import requests
import logging

from config import CIN7_API_URL, HEADERS
from typing import Dict

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def extract_line_item(item: Dict, tax: float) -> Dict:
    return {
        "ProductID": item.get("product_id", ""),
        "SKU": item.get("sku", ""),
        "Name": item.get("name", ""),
        "Quantity": item.get("quantity", 0),
        "Price": item.get("price", 0),
        "Discount": item.get("discount", 0),
        "Tax": tax,
        "AverageCost": 0,
        "TaxRule": "Auto Look Up",
        "Comment": item.get("comment", ""),
        "Total": item.get("total", 0),
    }


def sync_sale_order_to_cin7(sale: Dict, sale_id: str):
    logging.info(f"Syncing sale order to CIN7 for sale ID: {sale_id}")
    lines = sale.get("line_items", [])
    total_before_tax = sum(float(item.get("subtotal", 0)) for item in lines)
    tax = sum(float(item.get("subtotal_tax", 0)) for item in lines)

    payload = {
        "SaleID": sale_id,
        "CombineAdditionalCharges": False,
        "Memo": sale.get("customer_note", ""),
        "Status": "AUTHORISED",
        "Lines": [extract_line_item(item, tax) for item in lines],
        "AdditionalCharges": [],
        "TotalBeforeTax": total_before_tax,
        "Tax": tax,
        "Total": total_before_tax + tax,
    }

    print(payload)

    response = requests.post(CIN7_API_URL + "sale/order", json=payload, headers=HEADERS)

    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        logging.error("Failed to decode JSON response")
        return None
