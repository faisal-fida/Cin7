from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CIN7_API_URL = "https://inventory.dearsystems.com/ExternalApi/v2/"
CIN7_ACCOUNT_ID = "12999e8d-0e97-4a5d-b345-acf0f4155813"
CIN7_APPLICATION_KEY = "57a82013-9afa-8edf-4051-6d1a44b4113c"

SYNC_STATUSES = [
    "processing",
    "on-hold",
    "delivered-not-paid",
    "paid-not-delivered",
    "installments",
    "pc-build-processing",
    "reservation",
]
EXCLUDE_STATUSES = ["draft", "pending-payment"]


def sync_order_to_cin7(order):
    headers = {
        "Content-type": "application/json",
        "api-auth-accountid": CIN7_ACCOUNT_ID,
        "api-auth-applicationkey": CIN7_APPLICATION_KEY,
    }
    # Create or update sales order in Cin7
    response = requests.post(f"{CIN7_API_URL}/SaleList", json=order, headers=headers)
    return response.json()


def create_credit_note_in_cin7(order_id):
    headers = {
        "Content-type": "application/json",
        "api-auth-accountid": CIN7_ACCOUNT_ID,
        "api-auth-applicationkey": CIN7_APPLICATION_KEY,
    }
    # Create a Credit Note and close the sales order in Cin7
    response = requests.post(
        f"{CIN7_API_URL}/CreditNote", json={"OrderID": order_id}, headers=headers
    )
    return response.json()


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    order_status = data.get("status")

    if order_status in EXCLUDE_STATUSES:
        return jsonify({"message": "Order status excluded from syncing"}), 200

    if order_status in SYNC_STATUSES:
        sync_order_to_cin7(data)

    if order_status == "completed":
        create_credit_note_in_cin7(data["id"])

    return jsonify({"message": "Order processed"}), 200


if __name__ == "__main__":
    app.run(port=5000)
