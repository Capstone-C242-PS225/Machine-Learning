import os
import json
import pandas as pd


def extract_gambling_features(data):
    try:
        return {
            "user_email": data.get("createdByUser", {}).get("email", None),
            "transaction_amount": data.get("amount", 0),
            "transaction_status": data.get("status", None),
            "transaction_type": data.get("entryType", None),
            "user_total_cashout": data.get("userBank", {}).get("totalCashout", 0),
            "user_total_balance": data.get("userBank", {}).get("totalBalance", 0),
            "company_total_cashout": data.get("companyBank", {}).get("totalCashout", 0),
            "company_total_balance": data.get("companyBank", {}).get("totalBalance", 0)
        }
    except Exception:

        return {
            "user_email": None,
            "transaction_amount": 0,
            "transaction_status": None,
            "transaction_type": None,
            "user_total_cashout": 0,
            "user_total_balance": 0,
            "company_total_cashout": 0,
            "company_total_balance": 0
        }
def process_json_to_tabular(input_folder, output_file):
    all_processed_data = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_folder, file_name)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

      
                    if isinstance(data, list):
                        for item in data:
                            processed_data = extract_gambling_features(item)
                            all_processed_data.append(processed_data)
         
                    elif isinstance(data, dict):
                        processed_data = extract_gambling_features(data)
                        all_processed_data.append(processed_data)

            except Exception as e:
                print(f"Error processing file {file_name}: {e}")
                all_processed_data.append(extract_gambling_features({}))


    df = pd.DataFrame(all_processed_data)
    df.to_csv(output_file, index=False)


input_folder = "."  
output_csv = "tabulated_gambling_data.csv" 

process_json_to_tabular(input_folder, output_csv)