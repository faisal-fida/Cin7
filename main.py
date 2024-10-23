import json

from sync_order import sync_sale_order_to_cin7
from sync_sale import sync_sale_to_cin7

if __name__ == "__main__":
    with open("sale.json") as f:
        sale = json.load(f)
        # sale_response = sync_sale_to_cin7(sale)
        sale_response = "A"

        if sale_response:
            # sale_id = sale_response.get("ID", "")
            sale_id = "f443dbf6-b97e-4086-a430-7d3a4ba78aee"
            sale_order_response = sync_sale_order_to_cin7(sale, sale_id)

        # print(f"Sale Response: {sale_response}")
        print(f"Sale Order Response: {sale_order_response}")
