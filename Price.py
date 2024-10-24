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
        "Price (NZD)": [
            5379.19, 9706.88, 5443.26, 
            5167.67, 9178.69, 5167.67, 
            9261.27, 4892.07, 4892.07, 
            5057.79, 9003.36, 4485.40, 
            7857.58
        ],
        "Price per m3 (NZD)": [
            192.11, 142.75, 194.40, 
            184.56, 134.98, 184.56, 
            136.20, 174.72, 174.72, 180.64, 
            132.40, 160.19, 115.55
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
    container_price_nzd = filtered_data.iloc[0]['Price (NZD)']  # Get the container price in NZD
    container_volume = filtered_data.iloc[0]['Volume (m3)']  # Get the volume (m3) for the container size

    # Step 7: Calculate the Estimated Landed NZD
    st.subheader("Estimated Landed NZD")

    # Get the product volume (m3)
    product_volume = product_size_mapping.get(selected_product_type, 0)

    if product_price_usd > 0 and container_volume > 0 and container_price_nzd > 0 and product_volume > 0:
        # Calculate the freight cost for the item (already in NZD)
        shipping_cost_per_m3_nzd = container_price_nzd / container_volume
        freight_cost_for_product_nzd = shipping_cost_per_m3_nzd * product_volume

        # Convert product price from USD to NZD
        product_price_nzd = product_price_usd * USD_TO_NZD

        # Total landed cost in NZD (price + freight cost)
        total_landed_cost_nzd = product_price_nzd + freight_cost_for_product_nzd

        st.success(f"The estimated landed cost for {selected_product_type} in NZD is: ${total_landed_cost_nzd:.2f}")
    else:
        st.error("Please provide valid inputs for product price, container size, and container price.")

if __name__ == '__main__':
    main()
