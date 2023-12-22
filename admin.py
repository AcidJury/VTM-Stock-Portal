import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime

csv_file_path = "Prdt List.csv"
df = pd.read_csv(csv_file_path)
product_names = df['PRODUCT NAME'].tolist()
colours = df['COLOUR'].tolist()

in_data = pd.read_csv("IN test.csv")
out_data = pd.read_csv("OUT.csv")

filter = in_data[~in_data['Bale/Roll Number'].isin(out_data['Bale/Roll Number'])]

df_copy = in_data.copy()
df_copy_2 = df_copy.copy()


st.set_page_config(page_title="Admin Page")
with st.sidebar:
    selected = option_menu("Main Menu", ["Dashboard", 'Add New Product', "Delete Product", "Stock Inventory"], 
        icons=['bar-chart', 'plus-circle', 'trash', 'table'], menu_icon="cast", default_index=0)
    
if selected == "Dashboard":

    st.markdown("<h1 style='text-align: center; color: white;'>DASHBOARD - IN STOCK</h1><br>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    # Total number of entries
    total_entries = len(filter)
    col1.metric("Total Entries", total_entries, None)

    # Total quantity entered in metres
    total_metres = filter['Enter in metres'].sum()
    total_metres = round(total_metres)
    total_metres_f = "{:,}".format(total_metres)
    col3.metric("Total Length(in mtrs)", total_metres_f, None)

    # Total quantity entered in kilograms
    total_kilograms = filter['Enter in kilograms'].sum()
    total_kilograms = round(total_kilograms)
    total_kilograms_f = "{:,}".format(total_kilograms)

    # Display the metric with custom CSS
    col5.metric("Total Weight(in kgs)", total_kilograms_f, None)

    Product_count = filter.groupby(['PRODUCT NAME', 'COLOUR']).size().reset_index(name='Product Count')
    product_table = filter.groupby(['PRODUCT NAME', 'COLOUR']).agg({
        'Enter in metres': 'sum',
        'Enter in kilograms': 'sum'
    }).reset_index()
    
    product_table = pd.merge(product_table, Product_count, how='left', on=['PRODUCT NAME', 'COLOUR'])
    product_table = product_table.sort_values(by='Product Count', ascending=False)

    # Display the initial data table
    original_table_to_display = product_table.rename(columns={'COLOUR': 'Colour', 'Enter in metres': 'Total Metres', 'Enter in kilograms': 'Total Kilograms'})
    
    # Add a color filter option in the sidebar
    selected_color = st.selectbox("Select Color", product_table['COLOUR'].unique().tolist())

    # Filter the data based on the selected count and color
    filtered_table = product_table[(product_table['COLOUR'] == selected_color)]

    # Determine whether to display the original table or the filtered table
    col5.markdown("#")
    display_original_table = st.checkbox("Display Original Table", False)

    # Display the appropriate table
    if display_original_table:
        st.table(original_table_to_display)
        low_product_count = product_table[product_table['Product Count'] < 12]

        if not low_product_count.empty:
            low_prdt_names = low_product_count['PRODUCT NAME'].tolist()
            low_colours = low_product_count['COLOUR'].tolist()
            low_counts = low_product_count['Product Count'].tolist()

            combined_list = [f"{name} - {colour} (Count: {count})" for name, colour, count in zip(low_prdt_names, low_colours, low_counts)]

            error_message = "\n- ".join(combined_list)
            st.success(f"Products with count less than 12:\n- {error_message}")
    else:
        st.markdown(f"Color: {selected_color if selected_color != 'All' else 'All'}")
        st.table(filtered_table.rename(columns={'COLOUR': 'Colour', 'Enter in metres': 'Total Metres', 'Enter in kilograms': 'Total Kilograms'}))

        low_product_count = filtered_table[filtered_table['Product Count'] < 12]

        if not low_product_count.empty:
            low_prdt_names = low_product_count['PRODUCT NAME'].tolist()
            low_colours = low_product_count['COLOUR'].tolist()
            low_counts = low_product_count['Product Count'].tolist()

            combined_list = [f"{name} - {colour} (Count: {count})" for name, colour, count in zip(low_prdt_names, low_colours, low_counts)]

            error_message = "\n- ".join(combined_list)
            st.success(f"Products with count less than 12:\n- {error_message}")

elif selected == "Add New Product":

    # Create Streamlit app
    st.markdown("<h1 style='text-align: center; color: white;'>ADD NEW PRODUCT</h1><br>", unsafe_allow_html=True)
    
    # Dropdown menu for PRODUCT NAME
    selected_product = st.text_input("Select PRODUCT NAME")
    selected_product = selected_product.upper().strip()

    # Dropdown menu for COLOUR
    selected_colour = st.text_input("Select COLOUR")
    selected_colour = selected_colour.upper().strip()

    m = st.markdown(""" <style> div.stButton > button:first-child { background-color: #2E3454; align: centre; font-size: 30px} </style>""", unsafe_allow_html=True) 
    col1, col2, col3 , col4, col5 = st.columns(5)

    with col1:
        pass
    with col2:
        pass
    with col4:
        pass
    with col5:
        pass
    with col3 :
        b = st.button("Add New Product")

    # Button to save the entered data
    if b:
        if ((df['PRODUCT NAME'] == selected_product) & (df['COLOUR'] == selected_colour)).any():
            st.error("Product and Colour combination already exists!")

        else:     
            df2 = {'PRODUCT NAME': selected_product, 'COLOUR': selected_colour}
            df = df.append(df2, ignore_index = True)
            df.to_csv("Prdt List.csv", index=False)

            # Display a success message
            st.success("Data Save Successfully!")

elif selected == "Delete Product":
    # Create Streamlit app
    st.markdown("<h1 style='text-align: center; color: white;'>DELETE PRODUCT</h1><br>", unsafe_allow_html=True)
 
    # Dropdown menu for PRODUCT NAME
    filter_product_names = df['PRODUCT NAME'].unique()
    selected_product = st.selectbox("Select PRODUCT NAME", filter_product_names)
    selected_product = selected_product.strip()
    filtered_df = df[df['PRODUCT NAME'] == selected_product]

    # Get unique colors for the selected product
    available_colors = filtered_df['COLOUR'].unique()

    # Dropdown menu for COLOUR
    selected_colour = st.selectbox("Select COLOUR", available_colors)
    selected_colour = selected_colour.strip()

    m = st.markdown(""" <style> div.stButton > button:first-child { background-color: #2E3454; align: centre; font-size: 30px} </style>""", unsafe_allow_html=True) 
    col1, col2, col3 , col4, col5 = st.columns(5)

    with col1:
        pass
    with col2:
        pass
    with col4:
        pass
    with col5:
        pass
    with col3 :
        b = st.button("DELETE")

    # Button to save the entered data
    if b:
        df = df[(df['PRODUCT NAME'] != selected_product) | (df['COLOUR'] != selected_colour)]

        # Save the DataFrame to the new CSV file
        df.to_csv("Prdt List.csv", index=False)

        # Display a success message
        st.success("Data Deleted!")
        
elif selected == 'Stock Inventory':
    #  # Create Streamlit app
    st.markdown("<h1 style='text-align: center; color: white;'>STOCK INVENTORY</h1>", unsafe_allow_html=True)

    input_data = in_data
    output_data = out_data

    c1, c2, c3, c4, c5 = st.columns(5)

    # Merge input and output data based on 'Bale/Roll Number'
    combined_data = pd.merge(input_data, output_data, on='Bale/Roll Number', how='outer', suffixes=('_input', '_output'))
 
    filter_product_names = df['PRODUCT NAME'].unique()
    selected_product = st.selectbox("Select PRODUCT NAME", filter_product_names)
    selected_product = selected_product.strip()
    filtered_df = df[df['PRODUCT NAME'] == selected_product]

    # Get unique colors for the selected product
    available_colors = filtered_df['COLOUR'].unique()

    # Dropdown menu for COLOUR
    selected_colour = st.selectbox("Select COLOUR", available_colors)
    selected_colour = selected_colour.strip()
    combined_data = combined_data[
        (combined_data['PRODUCT NAME'] == selected_product) &
        (combined_data['COLOUR'] == selected_colour)
    ]

    combined_data['Date_output'] = pd.to_datetime(combined_data['Date_output']).dt.strftime("%Y-%m-%d")

    # Convert 'Date' and 'Time' columns to datetime objects for both input and output data
    combined_data['Datetime_input'] = pd.to_datetime(combined_data['Date_input'] + ' ' + combined_data['Time_input'], format='%Y-%m-%d %H:%M:%S')
    combined_data['Datetime_output'] = pd.to_datetime(combined_data['Date_output'] + ' ' + combined_data['Time_output'], format='%Y-%m-%d %H:%M:%S')

    # Calculate the current date and time
    current_datetime = datetime.now()

    # Calculate the duration for each item that is still inside the warehouse
    combined_data['Duration_inside'] = current_datetime - combined_data['Datetime_input']
    combined_data['Duration_outside'] = combined_data.apply(lambda row: row['Datetime_output'] - row['Datetime_input'], axis=1)
    combined_data['Duration_in'] = current_datetime - combined_data['Datetime_output']
 
    def format_duration(duration):
        if duration.total_seconds() >= 24 * 3600:
            days = duration.days
            return f"{days} days"
        else:
            hours, remainder = divmod(duration.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            if hours == 0:
                return f"{minutes} minutes"
            else:
                return f"{hours} hours {minutes} minutes"

    # Apply the formatting function to the 'Duration' column
    combined_data['Formatted Duration_inside'] = combined_data['Duration_inside'].apply(format_duration)
    combined_data['Formatted Duration_outside'] = combined_data['Duration_outside'].apply(format_duration)
    combined_data['Formatted Duration_in'] = combined_data['Duration_in'].apply(format_duration)

    # Get the latest operation (Input or Output) for each Bale/Roll Number
    latest_operations = combined_data.sort_values(['Bale/Roll Number', 'SNo_input', 'SNo_output']).groupby('Bale/Roll Number').tail(1)

    # Filter data for items inside the warehouse
    inside_data = latest_operations[latest_operations['Stock Operation_output'].isnull()]
    # Filter data for items outside the warehouse
    outside_data = latest_operations[latest_operations['Stock Operation_output'].notnull()]

    operation_selections = st.selectbox("Select Operation", options=["Import", "Export"])
    # in_data = combined_data[combined_data['Date_input'].dt.date == selected_date]

    selected_date = st.date_input("Select a date")
    selected_date_str = selected_date.strftime("%Y-%m-%d")
    st.markdown("##")

    table_style = """
        <style>
            table {
                width: 50%; /* You can adjust the width as needed */
                margin-left: auto;
                margin-right: auto;
                text-align: center;
            }
            th, td {
                text-align: center;
            }
        </style>
    """

    if operation_selections == "Import":
        # inside_data['Date_input'] = pd.to_datetime(inside_data['Date_input'], format="%Y/%m/%d")
        inside_data_f = inside_data[inside_data['Date_input'] == selected_date_str]
        inside_data_sorted = inside_data_f.sort_values('Duration_inside', ascending=False)     
        table_to_display = inside_data_sorted.rename(columns={'Bale/Roll Number': 'Roll Number', 'Date_input': 'Import Date', 'Time_input': 'Import Time', 'Formatted Duration_inside': 'Duration - Inside Storage'})
        st.table(table_to_display[['Roll Number','Import Date','Import Time', 'Duration - Inside Storage']])
 
    if operation_selections == "Export":
        outside_data_f = outside_data[outside_data['Date_output'] == selected_date_str]
        outside_data_sorted = outside_data_f.sort_values('Duration_in', ascending=False)
        table_to_display = outside_data_sorted.rename(columns={'Bale/Roll Number': 'Roll Number', 'Date_output': 'Export Date', 'Time_output': 'Export Time', 'Formatted Duration_outside': 'Duration - Inside Storage', 'Formatted Duration_in': 'Duration - Outside Storage'})
        st.table(table_to_display[['Roll Number','Export Date','Export Time', 'Duration - Inside Storage', 'Duration - Outside Storage']])
  