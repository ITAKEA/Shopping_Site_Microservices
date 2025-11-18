import streamlit as st
import requests

# Account Service URL
ACCOUNT_SERVICE_URL = "http://acc:5000"
PRODUCT_SERVICE_URL = "http://products:5000/products"

# Initialize session state for authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

# Sidebar for login/registration
with st.sidebar:
    st.title("Account")

    if not st.session_state.logged_in:
        tab1, tab2 = st.tabs(["Login", "Register"])

        # Login Tab
        with tab1:
            st.subheader("Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login"):
                try:
                    response = requests.post(
                        f"{ACCOUNT_SERVICE_URL}/login",
                        json={"username": login_username, "password": login_password}
                    )

                    if response.status_code == 200:
                        # Extract Bearer token from Authorization header
                        auth_header = response.headers.get('Authorization')
                        if auth_header and auth_header.startswith('Bearer '):
                            st.session_state.logged_in = True
                            st.session_state.username = login_username
                            st.session_state.auth_token = auth_header
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid token received from server")
                    else:
                        st.error(response.json().get('message', 'Login failed'))
                except Exception as e:
                    st.error(f"Error connecting to account service: {str(e)}")

        # Register Tab
        with tab2:
            st.subheader("Create Account")
            reg_username = st.text_input("Username", key="reg_username")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm")

            if st.button("Register"):
                if reg_password != reg_password_confirm:
                    st.error("Passwords do not match!")
                elif not reg_username or not reg_password:
                    st.error("Username and password are required!")
                else:
                    try:
                        response = requests.post(
                            f"{ACCOUNT_SERVICE_URL}/profile",
                            json={"username": reg_username, "password": reg_password}
                        )

                        if response.status_code == 201:
                            st.success("Registration successful! Please login.")
                        else:
                            st.error(response.json().get('message', 'Registration failed'))
                    except Exception as e:
                        st.error(f"Error connecting to account service: {str(e)}")

    else:
        st.success(f"Logged in as: {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.auth_token = None
            st.rerun()

# Main content - Product Catalog
st.title("Product Catalog")

try:
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
except Exception as e:
    st.error(f"Error loading products: {str(e)}")
