import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu

# Function to create CSV files with headers if they don't exist
def create_csv_if_not_exists(file_path, headers):
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        df = pd.DataFrame(columns=headers)
        df.to_csv(file_path, index=False)

# Function to edit data based on Bale/Roll Number
def edit_data(csv_file_path, bale_roll_number, updated_data):
    df = pd.read_csv(csv_file_path)

    # Convert the Bale/Roll Number column to string
    df['Bale/Roll Number'] = df['Bale/Roll Number'].astype(str)

    # Check if Bale/Roll Number exists in the CSV file
    if bale_roll_number in df['Bale/Roll Number'].values:
        # Update the data for the specified Bale/Roll Number
        df.loc[df['Bale/Roll Number'] == bale_roll_number, updated_data.keys()] = updated_data.values()

        # Save the updated DataFrame to the CSV file
        df.to_csv(csv_file_path, index=False)
        return True
    else:
        return False


# Function to get or create session state
def get_session_state():
    if 'session_state' not in st.session_state:
        st.session_state.session_state = {}
    return st.session_state.session_state

# CSV file paths
in_csv_file_path = "IN test.csv"
out_csv_file_path = "OUT.csv"
b1_csv_file_path = "Prdt List.csv"

# Headers for the CSV files
in_csv_headers = ['SNo', 'Date', 'Time', 'Bale/Roll Number', 'PRODUCT NAME', 'COLOUR', 'Stock Operation', 'Enter in metres', 'Enter in kilograms']
out_csv_headers = ['SNo', 'Date', 'Time', 'Bale/Roll Number']

# Create CSV files with headers if they don't exist
create_csv_if_not_exists(in_csv_file_path, in_csv_headers)
create_csv_if_not_exists(out_csv_file_path, out_csv_headers)

# Fetch unique values for PRODUCT NAME and COLOUR from B1.csv
b1_df = pd.read_csv(b1_csv_file_path)
product_names = b1_df['PRODUCT NAME'].unique().tolist()
colours = b1_df['COLOUR'].unique().tolist()

# Sidebar for stock operation
with st.sidebar:
    stock_operation = option_menu("VTM StockPilot Maintanance Portal", ['Input', 'Output', 'Edit Input Data','Edit Output Data','Display Input Data', 'Display Export Data'], 
     menu_icon="cast", default_index=0)



# Get or create session state
session_state = get_session_state() 

# If 'Output' is selected, display only the Bale/Roll Number input field
if stock_operation == 'Output':
    
    # Create Streamlit app
    st.title("Inventory Stock Withdrawal")
    bale_roll_number = st.text_input("Enter Bale/Roll Number for Output")

    # Button to save the entered data for 'Output' operation
    if st.button("Save"):
        # Validate that bale_roll_number is a numeric value for 'Output' operation
        if not bale_roll_number.isdigit():
            st.error("Bale/Roll Number should be a numeric value for Output operation.")
        else:
            # Check if Bale/Roll Number exists in IN.csv for 'Output' operation
            df_existing_in = pd.read_csv(in_csv_file_path)
            df_existing_out = pd.read_csv(out_csv_file_path)

            if bale_roll_number not in df_existing_in['Bale/Roll Number'].astype(str).values:
                st.error(f"Bale/Roll Number {bale_roll_number} does not exist in IN.csv. Cannot export.")
            elif bale_roll_number in df_existing_out['Bale/Roll Number'].astype(str).values:
                st.error(f"Bale/Roll Number {bale_roll_number} has already been exported. Cannot export duplicate entries.")
            else:
                # Create or load OUT.csv for 'Output' operation
                df_existing_out = pd.read_csv(out_csv_file_path)

                # Create a DataFrame with the new data for 'Output' operation
                new_data_out = pd.DataFrame({'SNo': [len(df_existing_out) + 1],
                                             'Date': [datetime.now().strftime("%Y-%m-%d")],
                                             'Time': [datetime.now().strftime("%H:%M:%S")],
                                             'Bale/Roll Number': [bale_roll_number],
                                             'Stock Operation': [stock_operation]})
                # Append the new data to the DataFrame
                df_existing_out = pd.concat([df_existing_out, new_data_out], ignore_index=True)

                # Save the DataFrame to the CSV file
                df_existing_out.to_csv(out_csv_file_path, index=False)

                # Display a success message
                st.success("Data saved successfully.")




# If 'Input' is selected, display the input fields for 'Input' operation
elif stock_operation == 'Input':
    st.title("Inventory Stock Data Entry")
    # Input field for Bale/Roll Number
    bale_roll_number = st.text_input("Enter Bale/Roll Number")

    selected_product = st.selectbox("Select PRODUCT NAME", product_names)
    b2_df = pd.read_csv("Prdt List.csv")
    colours = b2_df[b2_df['PRODUCT NAME'] == selected_product]['COLOUR'].unique().tolist()
    selected_colour = st.selectbox("Select COLOUR", colours)

    # Input field for entering in meters with validation
    meters = st.number_input("Enter Metres (numeric value with up to four decimal places)", format="%f", step=0.0001)

    # Input field for entering in kilograms with validation
    kilograms = st.number_input("Enter in Kilograms (numeric value with up to four decimal places)", format="%f", step=0.0001)

    # Button to save the entered data for 'Input' operation
    if st.button("Save"):
        # Validate if Bale/Roll Number is a positive whole number
        if not (bale_roll_number.isdigit() and int(bale_roll_number) > 0):
            st.error("Bale/Roll Number should be a positive whole number greater than zero.")
        else:
            # Check if Bale/Roll Number already exists in IN.csv
            df_existing_in = pd.read_csv(in_csv_file_path)
            if bale_roll_number in df_existing_in['Bale/Roll Number'].astype(str).values:
                st.error(f"Bale/Roll Number {bale_roll_number} already exists in IN.csv. Cannot save duplicate entries.")
            else:
                # Round meters and kilograms to 2 decimal places
                meters = round(meters, 2)
                kilograms = round(kilograms, 2)

                # Determine the CSV file to save to based on the stock operation
                csv_file = in_csv_file_path

                # Check if the CSV file exists and is not empty for 'Input' operation
                df_existing_in = pd.read_csv(csv_file)

                # Create a DataFrame with the new data for 'Input' operation
                new_data_in = pd.DataFrame({'SNo': [len(df_existing_in) + 1], 'Date': [datetime.now().strftime("%Y-%m-%d")],
                                            'Time': [datetime.now().strftime("%H:%M:%S")],
                                            'Bale/Roll Number': [bale_roll_number],
                                            'PRODUCT NAME': [selected_product], 'COLOUR': [selected_colour],
                                            'Stock Operation': [stock_operation], 'Enter in metres': [meters],
                                            'Enter in kilograms': [kilograms]})

                # Append the new data to the DataFrame
                df_existing_in = pd.concat([df_existing_in, new_data_in], ignore_index=True)

                # Save the DataFrame to the CSV file
                df_existing_in.to_csv(csv_file, index=False)

                # Display a success message
                st.success("Data saved successfully.")


            
            
# If 'Edit' is selected, display the input fields for 'Edit' operation
elif stock_operation == 'Edit Input Data':
    st.title("Modifying Inventory Inputs")
    # Input field for Bale/Roll Number
    bale_roll_number = st.text_input("Enter Bale/Roll Number to Edit")

    # Validate if Bale/Roll Number exists in IN.csv and not in OUT.csv
    df_existing_in = pd.read_csv(in_csv_file_path)
    df_existing_out = pd.read_csv(out_csv_file_path)

    if bale_roll_number not in df_existing_in['Bale/Roll Number'].astype(str).values:
        st.error(f"Bale/Roll Number {bale_roll_number} does not exist in IN.csv.")
    elif bale_roll_number in df_existing_out['Bale/Roll Number'].astype(str).values:
        st.error(f"Bale/Roll Number {bale_roll_number} exists in OUT.csv. Cannot edit.")
    else:
        # Display the existing data for the Bale/Roll Number
        existing_data = df_existing_in.loc[df_existing_in['Bale/Roll Number'].astype(str).values == bale_roll_number]
        st.write("Existing Data:")
        st.write(existing_data)

        # Input fields for editing the data
        new_bale_roll_number = st.text_input("Enter New Bale/Roll Number")

        # Check if the new Bale/Roll Number already exists in IN.csv
        if new_bale_roll_number in df_existing_in['Bale/Roll Number'].astype(str).values:
            st.error(f"New Bale/Roll Number {new_bale_roll_number} already exists in IN.csv. Cannot edit.")
        else:
            # Fetch unique product names from B1.csv
            product_names = b1_df['PRODUCT NAME'].unique().tolist()
            selected_product = st.selectbox("Select PRODUCT NAME", product_names)

            # Fetch unique colours for the selected product from B2.csv
            b2_df = pd.read_csv("Prdt List.csv")
            colours = b2_df[b2_df['PRODUCT NAME'] == selected_product]['COLOUR'].unique().tolist()
            selected_colour = st.selectbox("Select COLOUR", colours)

            meters = st.number_input("Edit Metres (numeric value with up to four decimal points)", format="%f", step=0.0001)
            kilograms = st.number_input("Edit Kilograms (numeric value with up to four decimal points)", format="%f", step=0.0001)

            # Button to save the edited data
            if st.button("Save"):
                # Create a dictionary with the updated data
                updated_data = {'Bale/Roll Number': new_bale_roll_number, 'PRODUCT NAME': selected_product,
                                'COLOUR': selected_colour, 'Enter in metres': meters, 'Enter in kilograms': kilograms}

                # Call the function to edit the data in the CSV file
                if edit_data(in_csv_file_path, bale_roll_number, updated_data):
                    st.success("Data updated successfully.")
                else:
                    st.error("Failed to update data.")
                
# If 'Display' is selected, display the data based on the selected date
elif stock_operation == 'Display Input Data':
    st.title("Inventory Input Records")
    selected_date = st.date_input("Select a date")

    # Convert selected date to string
    selected_date_str = selected_date.strftime("%Y-%m-%d")

    # Read IN.csv and OUT.csv
    df_in = pd.read_csv(in_csv_file_path)
    df_out = pd.read_csv(out_csv_file_path)

    # Convert 'Date' column to string
    df_in['Date'] = df_in['Date'].astype(str)
    df_out['Date'] = df_out['Date'].astype(str)

    # Filter IN.csv based on the selected date
    df_in_filtered = df_in[df_in['Date'] == selected_date_str]

    # Filter OUT.csv based on the selected date
    df_out_filtered = df_out[df_out['Date'] == selected_date_str]

    # Find Bale/Roll Numbers that are in both IN.csv and OUT.csv
    common_bale_roll_numbers = pd.Series(list(set(df_in_filtered['Bale/Roll Number']).intersection(set(df_out_filtered['Bale/Roll Number']))))

    # Remove rows with Bale/Roll Numbers that are in both IN.csv and OUT.csv
    df_in_filtered = df_in_filtered[~df_in_filtered['Bale/Roll Number'].isin(common_bale_roll_numbers)]

    # Remove the 'SNo' column
    df_in_filtered = df_in_filtered.drop(columns=['SNo','Date','Time','Stock Operation'])

    # Sort the DataFrame in descending order (Last In First Out)
    df_in_filtered = df_in_filtered.sort_index(ascending=False)

    # Display the filtered data with a professional look
    st.table(df_in_filtered)
    
    
# If 'Display Export Data' is selected, display the data based on the selected date for OUT.csv
elif stock_operation == 'Display Export Data':
    
    st.title("Stock Withdrawal Records")
    selected_date_export = st.date_input("Select a date to view stock output entries")

    # Convert selected date to string
    selected_date_export_str = selected_date_export.strftime("%Y-%m-%d")

    # Read OUT.csv
    df_out = pd.read_csv(out_csv_file_path)

    # Convert 'Date' column to string
    df_out['Date'] = df_out['Date'].astype(str)

    # Filter OUT.csv based on the selected date
    df_out_filtered_export = df_out[df_out['Date'] == selected_date_export_str]

    # Remove the 'SNo' column
    df_out_filtered_export = df_out_filtered_export.drop(columns=['SNo'])

    # Sort the DataFrame in descending order (Last In First Out)
    df_out_filtered_export = df_out_filtered_export.sort_index(ascending=False)

    # Display the filtered data with a professional look for OUT.csv export data
    st.write("Export Data from OUT.csv:")
    st.table(df_out_filtered_export)
    
    
# If 'Edit Output Data' is selected, allow the user to search and edit the roll number in OUT.csv
elif stock_operation == 'Edit Output Data':
    st.title(" Editing Exported Stock Record")
    # Input field for searching the wrongly entered roll number
    search_roll_number = st.text_input("Enter the wrongly entered Roll Number to search")

    # Read OUT.csv
    df_out = pd.read_csv(out_csv_file_path)

    # Check if the search_roll_number exists in OUT.csv
    if search_roll_number not in df_out['Bale/Roll Number'].astype(str).values:
        st.error(f"Roll Number {search_roll_number} does not exist in OUT.csv.")
    else:
        # Display the existing data for the wrongly entered Roll Number
        existing_data = df_out.loc[df_out['Bale/Roll Number'].astype(str) == search_roll_number]
        st.write("Existing Data:")
        st.write(existing_data)

        # Input field for entering the correct Roll Number
        new_roll_number = st.text_input("Enter the correct Roll Number")

        # Button to save the edited data
        if st.button("Save"):
            # Check if the new_roll_number already exists in OUT.csv
            if new_roll_number in df_out['Bale/Roll Number'].astype(str).values:
                st.error(f"New Roll Number {new_roll_number} already exists in OUT.csv. Cannot update.")
            else:
                # Update the data in the same row with the correct Roll Number
                df_out.loc[df_out['Bale/Roll Number'].astype(str) == search_roll_number, 'Bale/Roll Number'] = new_roll_number

                # Save the updated DataFrame to OUT.csv
                df_out.to_csv(out_csv_file_path, index=False)

                # Display a success message
                st.success("Data updated successfully.")

