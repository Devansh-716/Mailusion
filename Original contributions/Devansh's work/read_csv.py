import csv
from pathlib import Path

def load_csv_as_dict(filepath):
    """
    Loads key-value pairs from a CSV file into a dictionary.
    Assumes the first column is the key and the second is the value.
    """
    data = {}
    with open(filepath, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter="=", quotechar='"')
        for row in reader:
            if len(row) >= 2:  # Ensure there are at least two columns
                key = row[0].strip()
                value = row[1].strip()
                value = value.encode().decode("unicode_escape")
                data[key] = value
        #print(data)
    return data

def getTxt():
    project_root = Path(__file__).resolve().parent.parent
    config_vars = load_csv_as_dict(project_root/'body_subject.csv')
    return config_vars

if __name__ == "__main__":
    print(f"Subject: {getTxt().get('SUBJECT')}")
    print(f"Body: {getTxt().get('BODY')}")