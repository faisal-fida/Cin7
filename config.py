CIN7_API_URL = "https://inventory.dearsystems.com/ExternalApi/v2/"
CIN7_ACCOUNT_ID = "12999e8d-0e97-4a5d-b345-acf0f4155813"
CIN7_APPLICATION_KEY = "57a82013-9afa-8edf-4051-6d1a44b4113c"

HEADERS = {
    "Content-type": "application/json",
    "api-auth-accountid": CIN7_ACCOUNT_ID,
    "api-auth-applicationkey": CIN7_APPLICATION_KEY,
}

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
