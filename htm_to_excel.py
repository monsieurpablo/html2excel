# Install necessary libraries
# !pip install streamlit
# !pip install xlsxwriter
# !pip install lxml
# !pip install pandas 

# %%
import streamlit as st
import pandas as pd
import re
from io import BytesIO
from datetime import datetime

# Streamlit app
st.title('HTML to Excel Converter')
st.write("This app extracts tables from an HTML file")
st.write("Pablo Arango 2024")
# Upload the HTML file
uploaded_file = st.file_uploader("Choose an HTML file", type=["html", "htm"])

if uploaded_file is not None:
    # Read the uploaded HTML file as text
    html_data = uploaded_file.read().decode("latin-1")

    # Extract tables using pandas
    tables = pd.read_html(BytesIO(html_data.encode("utf-8")))
    
    # Combine all tables into a single DataFrame
    combined_data = pd.concat(tables, ignore_index=True)
    
    # Use regex to find all text inside square brackets []
    pattern = re.compile(r"\[(.*?)\]")
    headers = pattern.findall(html_data)
    
    # Duplicate headers for alignment with the table data
    headers = [header for header in headers for _ in (0, 1)]  # Double each header
    
    # Insert the headers as a new column called "Legend" in the combined DataFrame
    try:
        combined_data.insert(0, "Legend", headers, False)
    except:
        pass
    
    # Display the first few rows of the data
    st.write("Preview of Combined Data:")
    st.dataframe(combined_data.head())
    
    # Get the current date and time in the format YYYYMMDD-HH-MM
    current_time = datetime.now().strftime("%Y%m%d-%H-%M")
    
    # Export to Excel on button click
    if st.button('Export to Excel'):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            combined_data.to_excel(writer, sheet_name="Combined_Data", index=False)
        
        output.seek(0)
        
        # Set the filename with the current date and time
        excel_file_name = f"combined_data_{current_time}.xlsx"
        
        # Provide the download link
        st.download_button(
            label="Download Excel file",
            data=output,
            file_name=excel_file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# %%
