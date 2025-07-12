import json


def restructure_product_creation_data(data, files):
    print("Request data received for restructure:", data)

    product_data = {
        "ProductID": data.get("ProductID"),
        "ProductCode": data.get("ProductCode"),
        "ProductName": data.get("ProductName"),
        "ProductImage": files.get("ProductImage"),
        "HSNCode": data.get("HSNCode"),
        "IsFavourite": data.get("IsFavourite", "false").lower() == "true",
        "Active": data.get("Active", "false").lower() == "true",
        "variants": [],
    }

    # ✅ Parse variants JSON string
    variants_json = data.get("variants")
    if variants_json:
        try:
            parsed_variants = json.loads(variants_json)
            for idx, variant in enumerate(parsed_variants):
                variant["image"] = files.get(f"variant_image_{idx}")
                product_data["variants"].append(variant)
        except json.JSONDecodeError:
            print("⚠️ Invalid JSON for variants field")

    return product_data
