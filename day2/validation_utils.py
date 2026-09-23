# -------- Validation Utils --------
import json
import csv
from datetime import datetime

class DataValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"ERROR: {self.message}"

def validate_file_structure(file_path, req_fields):
    if not file_path.exists():
        raise DataValidationError(f"{file_path} does not exist")

    if not file_path.stat().st_size > 0:
        raise DataValidationError(f"{file_path} is empty")

    if file_path.suffix == ".csv":
        with open(file_path) as f:
            reader = csv.DictReader(f)
            file_fields = reader.fieldnames

    elif file_path.suffix == ".json":
        with open(file_path) as f:
            data = json.load(f)
            file_fields = list(data[0].keys())

    else:
        print(f"ERROR: {file_path} has an unsupported file type")
        return False

    missing_fields = [field for field in req_fields if field not in file_fields]
    if missing_fields:
        raise DataValidationError(f"{file_path} is missing required fields: {missing_fields}")

    return True

def validate_records(records, id_field, num_fields=None, date_fields=None):
    if num_fields is None:
        num_fields = []
    if date_fields is None:
        date_fields = []
 
    valid_records = []
    rejected_records = []
    seen_ids = set()
 
    for record in records:
        reasons = []
        # --- Checking if ID Valid ---
        try:
            record_id = int(record[id_field])

        except KeyError:
            reasons.append(f"{id_field} is missing")
            record_id = None

        except (ValueError, TypeError):
            reasons.append(f"{id_field} is not a valid integer")
            record_id = None

        else:
            if record_id in seen_ids:
                reasons.append(f"{id_field} {record_id} is a duplicate")

            else:
                seen_ids.add(record_id)
 
        # --- Checking if Amount is Valid ---
        for field in num_fields:
            try:
                value = float(record[field])

            except KeyError:
                reasons.append(f"{field} is missing")

            except (ValueError, TypeError):
                reasons.append(f"{field} is not a valid number")

            else:
                if value < 0:
                    reasons.append(f"{field} is negative")
 
        # --- Checking if Date is Valid ---
        for field in date_fields:
            try:
                datetime.strptime(record[field], "%Y-%m-%d")

            except KeyError:
                reasons.append(f"{field} is missing")

            except (ValueError, TypeError):
                reasons.append(f"{field} is not in YYYY-MM-DD format")
 
        # --- Put Record in Correct List ---
        if reasons:
            rejected_record = dict(record)
            rejected_record["rejection_reason"] = ", ".join(reasons)
            rejected_records.append(rejected_record)

        else:
            valid_record = dict(record)
            valid_record[id_field] = record_id 
            for field in num_fields:
                valid_record[field] = float(valid_record[field])

            valid_records.append(valid_record)
 
    return valid_records, rejected_records
 