import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Define the path to the CSV file where submissions will be stored
SUBMISSIONS_FILE = r'C:\Users\chine\Desktop\PythonScripts\100DADDY\submissions.csv'

# Ensure that all strings that could contain special characters are quoted
# and that the CSV file is read with the correct delimiter
def safe_read_csv(file_path):
    return pd.read_csv(
        file_path, 
        encoding='utf-8', 
        sep=',', 
        quotechar='"', 
        skipinitialspace=True
    )

# Ensure that DataFrame is saved with quotes for all string fields
def safe_to_csv(df, file_path):
    df.to_csv(
        file_path, 
        index=False, 
        encoding='utf-8', 
        sep=',', 
        quotechar='"'
    )

# Initialize the submissions file if it doesn't exist
if not os.path.isfile(SUBMISSIONS_FILE):
    columns = ['Full Name', 'Date of Birth', 'Email', 'Phone Number', 'Address', 
               'Occupation', 'Annual Income', 'Previous Experience', 'Description', 'Timestamp']
    pd.DataFrame([], columns=columns).to_csv(SUBMISSIONS_FILE, index=False, encoding='utf-8', sep=',', quotechar='"')

with st.form(key='application_form'):
    full_name = st.text_input('Full Name')
    date_of_birth = st.date_input('Date of Birth')
    email = st.text_input('Email')
    phone_number = st.text_input('Phone Number')
    address = st.text_input('Address')
    occupation = st.text_input('Occupation')
    annual_income = st.number_input('Annual Income', min_value=0.0, format='%f')
    previous_experience = st.radio('Do you have any previous experience?', ['Yes', 'No'])
    description = st.text_area('Please provide a brief description of yourself.')
    terms_and_conditions = st.checkbox('I agree to the terms and conditions')
    submit_button = st.form_submit_button(label='Submit')

if submit_button and terms_and_conditions:
    form_data = pd.DataFrame([{
        'Full Name': full_name,
        'Date of Birth': date_of_birth.isoformat(),
        'Email': email,
        'Phone Number': phone_number,
        'Address': address,
        'Occupation': occupation,
        'Annual Income': annual_income,
        'Previous Experience': previous_experience,
        'Description': description,
        'Timestamp': datetime.now().isoformat()
    }])

    try:
        if os.path.isfile(SUBMISSIONS_FILE):
            submissions_df = safe_read_csv(SUBMISSIONS_FILE)
            submissions_df = pd.concat([submissions_df, form_data], ignore_index=True)
        else:
            submissions_df = form_data
        safe_to_csv(submissions_df, SUBMISSIONS_FILE)
        st.success('Thank you for your application. It has been recorded.')
    except Exception as e:
        st.error(f'An error occurred when saving your application: {e}')
elif submit_button:
    st.error('You must agree to the terms and conditions to submit the form.')

