Mailusion : An automated email sender 




IMPORTANT NOTE : 
1. This wont work without a .env file that contains your email (sender email) and password 
2. Password should be a 16 digit key generated after creating an app for python in gmail account 
3. Do install necessary frameworks. 
4. Follow the proper format of excel and csv file. Format is given at the last. 
5. The project is not hosted anywhere yet. 





Starting: 

1. Install Python, pandas, dotenv, csv, flask before using the app.
2. Run app.py and then go to the server link it will provide (ctrl + click)
3. Upload your data.xlsx and body_subject.csv and click Upload and send
4. Your emails would be sent. It might take some time depending on number of recipeints so please wait.
5. If it does not work, contact me and report the issue. 





Format for excel file:
1. It must contain email addresses of the receivers. 
   That particular column must be named "Email" {case sensitive}
2. Each column must have a name




Format for csv file:
```
SUBJECT = <Your subject here>

BODY = <YOUR BODY
        HERE>
``` 

1. this is also case sensitive, body and subject are treated as keys.
2. To add an empty line in the body or starting a new paragraph, use "\n" 
   and then start writing in next line.
