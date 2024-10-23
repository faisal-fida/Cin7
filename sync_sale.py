import json
import requests
import logging

from config import CIN7_API_URL, HEADERS
from typing import Dict

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

URL = CIN7_API_URL + "sale"


def get_address(sale: Dict, address_type: str) -> Dict:
    logging.info(f"Getting {address_type} address")
    address = {
        "Line1": sale.get(address_type, {}).get("address_1", ""),
        "Line2": sale.get(address_type, {}).get("address_2", ""),
        "City": sale.get(address_type, {}).get("city", ""),
        "State": sale.get(address_type, {}).get("state", ""),
        "Postcode": sale.get(address_type, {}).get("postcode", ""),
        "Country": sale.get(address_type, {}).get("country", ""),
    }

    if address_type == "shipping":
        address["Company"] = sale.get(address_type, {}).get("company", "")
        address["Contact"] = sale.get(address_type, {}).get("email", "")

    return address


def get_sale(sale_id: str) -> bool:
    logging.info(f"Fetching sale with ID: {sale_id}")
    response = requests.get(URL, headers=HEADERS, params={"ID": sale_id})

    if response.status_code != 200:
        logging.error(
            f"Failed to fetch sale with ID: {sale_id}, Status Code: {response.status_code}"
        )
        return False

    try:
        response = response.json()
    except json.decoder.JSONDecodeError:
        logging.error("Failed to decode JSON response")
        response = {}

    if response.get("ID") == sale_id:
        return True
    else:
        return False


def get_customer_id_by_email(email: str) -> str:
    logging.info(f"Fetching customer ID by email: {email}")
    url = CIN7_API_URL + "customer"
    response = requests.get(url, headers=HEADERS, params={"ContactFilter": email})

    if response.status_code == 200:
        response = response.json()
        customers = response.get("CustomerList", [])
        if customers and response.get("Total") == 1:
            return str(customers[0].get("ID"))
        else:
            logging.warning(f"No unique customer found for email: {email}")
            return None
    else:
        logging.error(
            f"Failed to fetch customer by email: {email}, Status Code: {response.status_code}"
        )
        return None


def sync_sale_to_cin7(sale: Dict) -> Dict:
    logging.info(f"Syncing sale to CIN7 with sale ID: {sale.get('id', '')}")
    billing_address = get_address(sale, "billing")
    shipping_address = get_address(sale, "shipping")

    if not sale.get("billing"):
        billing_address = shipping_address
    if not sale.get("shipping"):
        shipping_address = billing_address

    customer_email = sale.get("billing", {}).get("email", "")

    if not customer_email:
        logging.error("No email provided for the customer.")
        return {"error": "No email provided for the customer."}

    customer_id = get_customer_id_by_email(customer_email)

    if not customer_id:
        logging.error("No customer found with the given email.")
        return {"error": "No customer found with the given email."}

    customer_name = (
        sale.get("billing", {}).get("first_name", "")
        + " "
        + sale.get("billing", {}).get("last_name", "")
    )

    cin7_sale = {
        "ID": str(sale.get("id", "")),
        "Customer": customer_name,
        "CustomerID": customer_id,
        "Contact": customer_name,
        "Phone": sale.get("billing", {}).get("phone", ""),
        "Email": sale.get("billing", {}).get("email", ""),
        "DefaultAccount": "4000: Sales",
        "SkipQuote": True,
        "BillingAddress": billing_address,
        "ShippingAddress": shipping_address,
        "ShippingNotes": "",
        "TaxRule": "Auto Look Up",
        "TaxInclusive": sale.get("prices_include_tax", False),
        "Terms": "15 days",
        "PriceTier": "Tier 1",
        "ShipBy": sale.get("date_created", ""),
        "Location": "Main Warehouse",
        "SaleOrderDate": sale.get("date_created", ""),
        "LastModifiedOn": sale.get("date_modified", ""),
        "Note": sale.get("customer_note", ""),
        "CustomerReference": sale.get("id", ""),
        "CurrencyRate": 1.0,
        "SalesRepresentative": "DefaultSalesRep",
        "Carrier": sale.get("shipping_lines", [{}])[0].get("method_title", ""),
        "ExternalID": str(sale.get("id", "")),
        "AdditionalAttributes": {},
        "SaleType": "Simple",
    }

    if get_sale(str(sale.get("id", ""))):
        logging.info("Updating the sale")
        response = requests.put(URL, json=cin7_sale, headers=HEADERS)
    else:
        logging.info("Creating a new sale")
        response = requests.post(URL, json=cin7_sale, headers=HEADERS)

    try:
        response = response.json()
    except json.decoder.JSONDecodeError:
        logging.error("Failed to decode JSON response")
        response = None

    return response
