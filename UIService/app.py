import streamlit as st
import requests

# Configure page
st.set_page_config(page_title="Product Catalog", layout="centered")

# Title
st.title("Product Catalog")

# Product Catalog Service URL
PRODUCT_SERVICE_URL = "http://pro:5000/products"

# Fetch products from the ProductCatalogService
response = requests.get(PRODUCT_SERVICE_URL, timeout=5)
products = response.json()

# Display products in a list
for product in products:
    with st.container():
        col1, col2 = st.columns([1, 4])

        with col1:
            # Display product thumbnail
            if 'thumbnail' in product and product['thumbnail']:
                st.image(product['thumbnail'], width=100)

        with col2:
            # Display product details
            st.subheader(product['title'])
            st.write(f"**Pris:** {product['dkk_price']} kr.")
            st.write(f"**Mærke:** {product['brand']}")
            st.write(f"**Kategori:** {product['category']}")

            if 'description' in product:
                st.write(product['description'])

        st.divider()
