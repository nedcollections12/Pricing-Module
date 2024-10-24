import streamlit as st
import pandas as pd

# Directly input the cleaned data as a DataFrame
def load_data():
    # Define the data as a dictionary
    data_dict = {
        "Port": [
            "Fuzhou FZG", "Fuzhou FZG", "Jiujiang JIU", "Ningbo NBG", 
            "Ningbo NBG", "Qingdao QDG", "Qingdao QDG", "Tianjin Xingang TXG", 
            "Xiamen XMG", "Yantian YTN / Shenzhen", "Yantian YTN / Shenzhen", 
            "Haiphong HPH", "Haiphong HPH"
        ],
        "Container Size": [
            "20GP", "40HC", "20GP", "20GP", "40HC", 
            "20GP", "40HC", "20GP", "20GP", "20GP", 
            "40HC", "20GP", "40HC"
        ],
        "Volume (m3)": [
            28, 68, 28, 28, 68, 
            28, 68, 28, 28, 28, 
            68, 28, 68
        ],
        "Price": [
            5379.186622625929, 9706.878612716762, 5443.257638315441, 
            5167.665152766309, 9178.693228736582, 5167.665152766309, 
            9261.269611890999, 4892.072667217176, 4892.072667217176, 
            5057.793146160198, 9003.358794384807, 4485.402559867878, 
            7857.584640792733
        ],
        "Price per m3": [
            192.11380795092603, 142.74821489289357, 194.40205851126575, 
            184.55946974165388, 134.98078277553796, 184.55946974165388, 
            136.1951413513382, 174.716881, 174.716881, 180.63546950572137, 
            132.40233521154127, 160.19294856670993, 115.55271530577548
        ],
        "Product Type": [
            "Dawn Sofa", "Dining Table", "Dining Chair", "Occasional Chair", 
            "Coffee Table", "Dali Bowl", "Hudson Mug", "Dyne Sofa", 
            None, None, None, None, None
        ]
    }
    
    # Create a DataFrame
    data = pd.DataFrame(data_dict)
    return data

# Conversion rate (USD to NZD)
USD_TO_NZD = 1.66  # Example rate, adjust as needed

# Product type to size mapping (in m³)
product_size_mapping = {
    'Dyne Sofa': 2.15,
    'Dining Chair': 0.1363,
    'Dining Table': 0.228866,
    'Coffee Table': 1.212848,
    'Occasional Chair': 0.5179,
    'Dawn Sofa': 2.5,
    'Dali Bowl': 0.07,
    'Hudson Mug': 0.00145935
}

def main():
    st.title("Product Pricing Module")  # Main title of the page

    # Step 1: Load the data
    data = load_data()

    if data is None:
        return  # Stop if there's no data

    # Step 2: Select Port
    st.subheader("Select Port")
    port_options = data['Port'].unique()
    selected_port = st.selectbox("Select Port", port_options)

    # Step 3: Select Container Size
    st.subheader("Select Container Size")
    container_size_options = data['Container Size'].unique()
    selected_container_size = st.selectbox("Select Container Size", container_size_options)

    # Step 4: Select Product Type
    st.subheader("Select Product Type")
    product_type_options = list(product_size_mapping.keys())
    selected_product_type = st.selectbox("Select Product Type", product_type_options)

    product_type_options = [
    'Dyne Sofa', 'Dawn Sofa', 'Dining Chair', 'Dining Table', 
    'Coffee Table', 'Occasional Chair', 'Dali Bowl', 'Hudson Mug'
]

    # Step 5: Input Price in USD
    st.subheader("Enter Price in USD")
    product_price_usd = st.number_input(f"Enter the price of {selected_product_type} in USD", min_value=0.0, step=0.01)

    # Step 6: Filter the data to get container price and volume based on selected port and container size
    filtered_data = data[(data['Port'] == selected_port) & 
                         (data['Container Size'] == selected_container_size)]

    if filtered_data.empty:
        st.error(f"No data found for {selected_port} with {selected_container_size} container size.")
        return

    # Automatically fetch the container price and volume from the filtered data
    container_price = filtered_data.iloc[0]['Price']  # Get the container price
    container_volume = filtered_data.iloc[0]['Volume (m3)']  # Get the volume (m3) for the container size

    # Step 7: Calculate the Estimated Landed NZD
    st.subheader("Estimated Landed NZD")

    # Get the product volume (m3)
    product_volume = product_size_mapping.get(selected_product_type, 0)

    if product_price_usd > 0 and container_volume > 0 and container_price > 0 and product_volume > 0:
        # Calculate the freight cost for the item
        shipping_cost_per_m3 = container_price / container_volume
        freight_cost_for_product = shipping_cost_per_m3 * product_volume

         # Convert product price from USD to NZD
        product_price_nzd = product_price_usd * USD_TO_NZD

        # Total landed cost in NZD (price + freight cost)
        total_landed_cost_nzd = product_price_nzd + freight_cost_for_product_nzd

        st.success(f"The estimated landed cost for a product the same size as {selected_product_type} in NZD is: ${total_landed_cost_nzd:.2f}")
    else:
        st.error("Please provide valid inputs for product price, container size, and container price.")

if __name__ == '__main__':
    main()
