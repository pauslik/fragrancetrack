import streamlit as st
import polars as pl

# --- 1. Setup & Mock Data ---
# In a real app, you would load this from a CSV/Parquet file
data = {
    "category": ["Electronics", "Electronics", "Furniture", "Furniture", "Clothing"],
    "item_name": ["Laptop", "Smartphone", "Chair", "Desk", "T-Shirt"],
    "price": [999, 699, 150, 300, 20],
    # Using placeholder images for demo
    "image_url": [
        "https://via.placeholder.com/150?text=Laptop",
        "https://via.placeholder.com/150?text=Phone",
        "https://via.placeholder.com/150?text=Chair",
        "https://via.placeholder.com/150?text=Desk",
        "https://via.placeholder.com/150?text=Shirt"
    ]
}
df = pl.DataFrame(data)

st.set_page_config(layout="wide", page_title="FragranceTrack")

# --- 2. Navigation (Separate Pages) ---
# Using sidebar radio to simulate pages in a single script for easy deployment
page = st.sidebar.radio("Navigation", ["Browse Database", "Internal Search", "External Search"])

# --- 3. Page Logic ---

if page == "Browse Database":
    st.header("📂 Full Database Browsing")
    st.dataframe(df.to_pandas(), use_container_width=True) # Convert to pandas for native Streamlit rendering if needed

elif page == "Internal Search":
    st.header("🔍 2-Step Internal Search")
    
    # Step 1: Search/Select Category
    categories = df["category"].unique().to_list()
    selected_cat = st.selectbox("Step 1: Select Category", options=[""] + categories)
    
    # Step 2: Dynamic Options based on Step 1
    if selected_cat:
        # Filter data for the second step
        filtered_df = df.filter(pl.col("category") == selected_cat)
        items = filtered_df["item_name"].to_list()[:10] # Limit to 10 options
        
        selected_item_name = st.selectbox("Step 2: Select Item", options=items)
        
        # Single Item View
        if selected_item_name:
            st.divider()
            st.subheader(f"Item Details: {selected_item_name}")
            
            # Get the exact row
            item_row = filtered_df.filter(pl.col("item_name") == selected_item_name)
            
            # Display Image and Info
            col1, col2 = st.columns([1, 2])
            with col1:
                # Use markdown for images on GitHub Pages to avoid filesystem path issues
                img_url = item_row["image_url"][0]
                st.markdown(f"![Image]({img_url})")
            with col2:
                st.write(f"**Category:** {item_row['category'][0]}")
                st.write(f"**Price:** ${item_row['price'][0]}")
                st.success("Item found in internal database.")

elif page == "External Search":
    st.header("globe 2-Step External Search")
    st.info("This simulates searching an external API or dataset.")
    
    # Example of independent search logic
    query = st.text_input("Step 1: Enter external query (e.g., 'python')")
    
    if query:
        # Mocking dynamic results based on input
        mock_results = [f"{query} result {i+1}" for i in range(5)]
        selected_ext = st.selectbox("Step 2: Select Result", options=mock_results)
        
        if selected_ext:
            st.write(f"You selected: **{selected_ext}**")
