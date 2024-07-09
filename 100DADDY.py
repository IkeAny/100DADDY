
import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(r'fresh-gravity-419704-25735f1d7172.json', scope)
client = gspread.authorize(creds)
sheet = client.open('submissions').sheet1

st.title('Application Form')

# Terms and Conditions text
terms_and_conditions_text = """
**Terms and Conditions for Application Form**

1. Introduction
Welcome to our Application Form. By submitting your application, you are agreeing to comply with and be bound by the following terms and conditions of use, which together with our privacy policy govern [Your Company Name]'s relationship with you in relation to this service. If you disagree with any part of these terms and conditions, please do not use our application service.

2. Privacy
Please review our Privacy Policy, which also governs your visit to our application, to understand our practices.

3. Eligibility
You must be at least 18 years of age to submit this application. By submitting this application, you represent and warrant that you are of legal age to form a binding contract.

4. Application Submission
Your application does not guarantee acceptance into our program. We reserve the right to accept or reject applications at our discretion.

5. Accuracy of Information
You agree that all information you provide will be accurate, complete, and up to date.

6. Intellectual Property Rights
The content, organization, graphics, design, compilation, and other matters related to our application are protected under applicable copyrights, trademarks, and other proprietary rights.

7. Disclaimer of Warranties and Limitation of Liability
This application and the information, services, or products available to you through this application are provided on an 'as is' and 'as available' basis without any warranties of any kind, either express or implied.

8. Amendments to Terms and Conditions
We reserve the right to amend these terms and conditions at any time.

9. Governing Law
These terms and conditions are governed by the laws of [Your Jurisdiction] without regard to its conflict of law provisions.

10. Contact Information
For any questions or concerns regarding these terms and conditions, please contact us at [Your Contact Information].
"""

# Streamlit form
with st.form(key='application_form'):
    full_name = st.text_input('Full Name')
    email = st.text_input('Email')
    
    with st.expander("Terms and Conditions"):
        st.write(terms_and_conditions_text)
        
    terms_and_conditions = st.checkbox('I agree to the terms and conditions')
    submit_button = st.form_submit_button(label='Submit')

if submit_button and terms_and_conditions:
    # Preparing the data to insert into Google Sheets
    row = [full_name, email, str(datetime.now())]
    # Inserting the data into the sheet
    sheet.append_row(row)
    st.success('Thank you for your application. It has been recorded.')
elif submit_button:
    st.error('You must agree to the terms and conditions to submit the form.')
