import os
import json

def extract_important_features(data):
    try:
        return {
            "createdBy": data.get("createdBy", None),
            "createdByUser": {
                "name": data.get("createdByUser", {}).get("name", None),
                "email": data.get("createdByUser", {}).get("email", None),
                "phone": data.get("createdByUser", {}).get("phone", None)
            },
            "createdDate": data.get("createdDate", None),
            "transactionId": data.get("transactionId", None),
            "amount": data.get("amount", None),
            "status": data.get("status", None),
            "entryType": data.get("entryType", None),
            "user": {
                "name": data.get("user", {}).get("name", None),
                "email": data.get("user", {}).get("email", None),
                "phone2": data.get("user", {}).get("phone2", None),
                "status": data.get("user", {}).get("status", None),
                "newRegister": data.get("user", {}).get("newRegister", None)
            },
            "userBank": {
                "accountName": data.get("userBank", {}).get("accountName", None),
                "accountNumber": data.get("userBank", {}).get("accountNumber", None),
                "totalCashout": data.get("userBank", {}).get("totalCashout", None),
                "totalBalance": data.get("userBank", {}).get("totalBalance", None)
            },
            "companyBank": {
                "accountName": data.get("companyBank", {}).get("accountName", None),
                "accountNumber": data.get("companyBank", {}).get("accountNumber", None),
                "totalCashout": data.get("companyBank", {}).get("totalCashout", None),
                "totalBalance": data.get("companyBank", {}).get("totalBalance", None)
            }
        }
    except Exception:
        return {
            "createdBy": None,
            "createdByUser": {"name": None, "email": None, "phone": None},
            "createdDate": None,
            "transactionId": None,
            "amount": None,
            "status": None,
            "entryType": None,
            "user": {"name": None, "email": None, "phone2": None, "status": None, "newRegister": None},
            "userBank": {"accountName": None, "accountNumber": None, "totalCashout": None, "totalBalance": None},
            "companyBank": {"accountName": None, "accountNumber": None, "totalCashout": None, "totalBalance": None}
        }

def process_multiple_json_files(input_folder, output_file):
    all_processed_data = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_folder, file_name)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                    if isinstance(data, list):
                        for item in data:
                            processed_data = extract_important_features(item)
                            all_processed_data.append(processed_data)
   
                    elif isinstance(data, dict):
                        processed_data = extract_important_features(data)
                        all_processed_data.append(processed_data)
                    else:
    
                        all_processed_data.append(extract_important_features({}))

            except Exception as e:
                print(f"Error processing file {file_name}: {e}")
                all_processed_data.append(extract_important_features({}))


    with open(output_file, 'w') as outfile:
        json.dump(all_processed_data, outfile, indent=4)



input_folder = "/." 
output_file = "processed_data.json" 


process_multiple_json_files("", output_file)

print(f"Semua data telah diproses dan disimpan di {output_file}")