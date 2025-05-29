CIN7_API_URL = "https://inventory.dearsystems.com/ExternalApi/v2/"
CIN7_ACCOUNT_ID = ""
CIN7_APPLICATION_KEY = ""

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
