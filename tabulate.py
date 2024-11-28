import os
import json
import pandas as pd

# Fungsi untuk mengekstrak data relevan untuk klasifikasi tingkat kecanduan pejudi
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
        # Kembalikan data kosong jika terjadi error
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

# Fungsi untuk memproses banyak file JSON dan menyimpannya dalam file tabular
def process_json_to_tabular(input_folder, output_file):
    all_processed_data = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_folder, file_name)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                    # Jika data adalah list, iterasi setiap elemen list
                    if isinstance(data, list):
                        for item in data:
                            processed_data = extract_gambling_features(item)
                            all_processed_data.append(processed_data)
                    # Jika data adalah dictionary, langsung proses
                    elif isinstance(data, dict):
                        processed_data = extract_gambling_features(data)
                        all_processed_data.append(processed_data)

            except Exception as e:
                print(f"Error processing file {file_name}: {e}")
                all_processed_data.append(extract_gambling_features({}))

    # Simpan hasil ke dalam file tabular CSV menggunakan pandas
    df = pd.DataFrame(all_processed_data)
    df.to_csv(output_file, index=False)

# Lokasi folder input JSON dan output CSV
input_folder = "."  # Ganti dengan path folder JSON kamu
output_csv = "tabulated_gambling_data.csv"  # Nama file CSV hasil output

# Proses semua file JSON dan simpan ke CSV
process_json_to_tabular(input_folder, output_csv)