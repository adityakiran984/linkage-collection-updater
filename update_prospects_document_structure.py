import os
import json
from pymongo import MongoClient
from pprint import pprint
from dotenv import load_dotenv



def main():
    load_dotenv()
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("CLIENT")]
    prospects_collection = db[os.getenv("PROSPECTS_COLLECTION")]

    updated_prospects = []

    with open("linkage.prospects.json", encoding="utf-8") as f:
        prospects = json.load(f)
        i=1
        for prospect in prospects:
            updated_prospect = structure_updater(prospect, prospects_collection)
            # pprint(updated_prospect)
            if updated_prospect:
                updated_prospects.append(updated_prospect)


    with open("new-prospects-linkage.json", "w") as f:
        json.dump(updated_prospects, f, indent=4)

def structure_updater(prospect, collection):
    first_name = prospect["firstName"]
    last_name = prospect["lastName"]
    email = prospect["email"]
    phone_number = prospect["phoneNumber"]

    prospect.pop("firstName")
    prospect.pop("lastName")
    prospect.pop("email")
    prospect.pop("phoneNumber")

    contact_dict = {}

    contact_dict["firstName"] = first_name
    contact_dict["lastName"] = last_name
    contact_dict["email"] = email
    contact_dict["phoneNumber"] = phone_number

    contacts = []
    contacts.append(contact_dict)
    prospect["contacts"] = contacts
    return prospect

if __name__ == "__main__":
    main()