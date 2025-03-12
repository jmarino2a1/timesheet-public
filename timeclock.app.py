import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title("Employee Time Clock")

# Initialize session state if not already done
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Employee Name', 'Date', 'Check-In Time', 'Check-Out Time', 'Hours Worked'])

employee_name = st.text_input("Enter your name:")

if employee_name:
    col1, col2 = st.columns(2)
    
    if col1.button("Check In"):
        check_in_time = datetime.now()
        new_entry = pd.DataFrame({
            'Employee Name': [employee_name],
            'Date': [check_in_time.date()],
            'Check-In Time': [check_in_time.strftime('%H:%M:%S')],
            'Check-Out Time': [None],
            'Hours Worked': [0]
        })
        st.session_state['data'] = pd.concat([st.session_state['data'], new_entry], ignore_index=True)
        st.success(f"Checked in at {check_in_time.strftime('%H:%M:%S')}")
    
    if col2.button("Check Out"):
        check_out_time = datetime.now()
        for index, row in st.session_state['data'].iterrows():
            if row['Employee Name'] == employee_name and pd.isnull(row['Check-Out Time']):
                st.session_state['data'].at[index, 'Check-Out Time'] = check_out_time.strftime('%H:%M:%S')
                hours_worked = (check_out_time - datetime.strptime(row['Check-In Time'], '%H:%M:%S')).seconds / 3600
                st.session_state['data'].at[index, 'Hours Worked'] = round(hours_worked, 2)
                st.success(f"Checked out at {check_out_time.strftime('%H:%M:%S')}. Hours worked: {round(hours_worked, 2)}")
                break

st.subheader("Time Log")
st.dataframe(st.session_state['data'])

# Weekly Summary
if st.button("Show Weekly Summary"):
    if not st.session_state['data'].empty:
        last_week = datetime.now() - timedelta(days=7)
        weekly_data = st.session_state['data'][pd.to_datetime(st.session_state['data']['Date']) >= last_week.date()]
        weekly_summary = weekly_data.groupby('Employee Name')['Hours Worked'].sum().reset_index()
        st.subheader("Weekly Summary (Last 7 Days)")
        st.dataframe(weekly_summary)
    else:
        st.warning("No data available for the weekly summary.")

# CSV Export
if st.button("Export to CSV"):
    csv = st.session_state['data'].to_csv(index=False)
    st.download_button(label="Download CSV", data=csv, file_name="employee_time_log.csv", mime="text/csv")

# To run this app, save the code to a .py file and run with:
# streamlit run filename.py

# Let me know if you’d like me to refine or add more features! 🚀
