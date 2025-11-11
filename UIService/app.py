import streamlit as st
import requests

st.title("Product Catalog")

PRODUCT_SERVICE_URL = "http://products:5000/products"
response = requests.get(PRODUCT_SERVICE_URL)
products = response.json()

for product in products:
    with st.container():
        col1, col2 = st.columns([1, 4])

        with col1:
            if 'thumbnail' in product and product['thumbnail']:
                st.image(product['thumbnail'], width=100)

        with col2:
            st.subheader(product['title'])
            st.write(f"**Pris:** {product['dkk_price']} kr.")
            st.write(f"**Mærke:** {product['brand']}")
            st.write(f"**Kategori:** {product['category']}")
            st.write(product['description'])

        st.divider()
