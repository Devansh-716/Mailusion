"""
Necessary changes made to this file after the report submission. 
Original work(file) can be found in Original Contributions/Devansh's Work
"""
import csv
from pathlib import Path

def load_csv_as_dict(filepath):
    """
    Loads key-value pairs from a CSV file into a dictionary.
    """
    data = {}
    current_value = []
    current_key = None
    is_line_blank = True
    with open(filepath, 'r', encoding="utf-8") as csvfile:
        for line in csvfile:
            line = line.strip()
            if not line:
                if current_key:
                    current_value.append("")
                    is_line_blank = True
                continue

            if "=" in line and is_line_blank:
                if current_key:
                    value = "\n".join(current_value).strip().strip('"')
                    value = value.encode().decode("unicode_escape")
                    data[current_key] = value

                key, value = line.split("=", 1)
                current_key = key.strip()
                current_value = [value.strip()]
                is_line_blank = False
            else:
                if current_key:
                    current_value.append(line.strip())
                is_line_blank = False

        if current_key:
            value = "\n".join(current_value).strip().strip('"')
            value = value.encode().decode("unicode_escape")
            data[current_key] = value
        #print(data)
    return data

def getTxt():
    project_root = Path(__file__).resolve().parent.parent
    config_vars = load_csv_as_dict(project_root/'body_subject.csv')
    return config_vars

if __name__ == "__main__":
    print(f"Subject: {getTxt().get('SUBJECT')}")
    print(f"Body: {getTxt().get('BODY')}")
