import pandas as pd
from backend import read_csv as rcsv
from backend import send_email as se
import openpyxl

class SafeDict(dict):
    def __missing__(self, key):
        return "N/A"

df = pd.read_excel("data.xlsx", engine = "openpyxl")
def start(df):
        df["Status_email"] = "Pending" 
        subject_template = rcsv.getTxt().get('SUBJECT')
        body_template = rcsv.getTxt().get('BODY')

        for index, row in df.iterrows():

            dictonary = row.to_dict()
            receiver_mail = dictonary['Email']
            subject = subject_template.format_map(dictonary)
            body = body_template.format_map(SafeDict(dictonary))
            is_Sent = se.send_email(receiver_mail=receiver_mail, subject=subject,body=body)
            if is_Sent:
                print("Mail sent")
                df.loc[index,'Status_email'] = "Sent"
        
        df.to_excel("data.xlsx", index=False, engine="openpyxl")

start(df=df)