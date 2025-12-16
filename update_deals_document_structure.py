import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pprint import pprint

def main():
    load_dotenv()
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("CLIENT")]
    build_site_collection = db[os.getenv("BUILD_SITE_COLLECTION")]
    updated_deals = []

    with open("linkage.deals.json") as f:
        deals = json.load(f)
        for deal in deals:
            updated_deal = structure_updater(deal, build_site_collection)
            if updated_deal:
                updated_deals.append(updated_deal)

    with open("new-deals-linkage.json", "w") as f:
        json.dump(updated_deals, f, indent=4)

def structure_updater(deal, collection):
    build_site = deal.get("buildSite")
    result = collection.find_one({"_id": build_site})

    if not result:
        return None

    supplier = result.get("Supplier")
    deal["supplier"] = supplier

    return deal

if __name__ == "__main__":
    main()
