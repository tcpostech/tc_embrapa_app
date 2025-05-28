"""App beta version"""
import os
from datetime import datetime
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

from utils import sub_options, main_options, columns

load_dotenv()

# Session management
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = None

BACKEND_API = os.getenv('API_URL')
API_URL = f'{BACKEND_API}v1/api'
bearer = {'Authorization': f'Bearer {st.session_state.access_token}'}

st.set_page_config(page_title='TC Embrapa APP - β Version')
st.title('TC Embrapa APP - β Version')
st.markdown("""<style>
    div.block-container{ padding: 2rem; }
    h1 {text-align: center;}
    </style>""", unsafe_allow_html=True)


def auth_login(email: str, password: str):
    """
    Method to login user
    :param email: email as str param
    :param password: password as str param
    :return:
    """
    payload = {'email': email, 'password': password}
    return requests.post(f'{API_URL}/auth/login', json=payload, timeout=60).json()


def auth_register(first_name: str, last_name: str, email: str, username: str, password: str):
    """
    Method to register user
    :param first_name: first_name as str param
    :param last_name: last_name as str param
    :param email: email as str param
    :param username: username as str param
    :param password: password as str param
    :return:
    """
    payload = {'first_name': first_name, 'last_name': last_name,
               'email': email, 'username': username, 'password': password}
    return requests.post(f'{API_URL}/auth/signup', json=payload, timeout=60).json()


def about_me():
    """Method to get all user data"""
    return requests.get(f'{API_URL}/auth/me', headers=bearer, timeout=60).json()


def save_viticulture(category: str, mode: str):
    """
    Method to save subcategory
    :param category: category as str param
    :param mode: mode as str param
    :return:
    """
    url = f'{API_URL}/viticulture/external_content/{category}?mode={mode}'
    return requests.post(url, headers=bearer, timeout=60).json()


def search_subcategories(subcategory: str, year: int):
    """
    Method to find subcategories by year
    :param subcategory: subcategory as str param
    :param year: year as int param
    :return:
    """
    url = f'{API_URL}/viticulture/subcategory/{subcategory}/{year}'
    return requests.get(url, headers=bearer, timeout=60).json()


def login_page():
    """Method responsible to render the login page"""
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab.form('login_form', clear_on_submit=True):
        st.subheader("Login")
        email = st.text_input("Email", key='mail')
        password = st.text_input("Password", key='pwd', type="password")
        if st.form_submit_button("Enter"):
            result = auth_login(email, password)

            if result.get('access_token') and result.get('refresh_token'):
                st.toast(result.get('message'), icon='😍')
                st.session_state.authenticated = True
                st.session_state.access_token = result.get('access_token')
                st.session_state.refresh_token = result.get('refresh_token')
                st.rerun()
            else:
                st.toast(result.get('detail'), icon='😡')

    with register_tab.form('registration_form', clear_on_submit=True):
        st.subheader("Register")
        first_name = st.text_input("First name")
        last_name = st.text_input("Last name")
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.form_submit_button("Register"):
            result = auth_register(first_name, last_name, email, username, password)
            if result.get('detail'):
                st.toast(result.get('detail'), icon='😡')
            else:
                st.toast(result.get('message'), icon='😍')


def page_content():
    """Method responsible to render the protected page"""
    with st.sidebar:
        response = about_me()
        st.markdown(f'Olá, **{response.get('first_name')} {response.get('last_name')}**')

        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.access_token = None
            st.session_state.refresh_token = None
            st.rerun()

        st.divider()

        st.text('Clique abaixo para verificar se os dados já existem no banco de dados')
        with st.expander(':red[Clique para expandir]'):
            category = st.selectbox('Categoria', options=list(sorted(main_options.keys())))
            mode = st.selectbox('Modo', options=['API', 'FILE'],
                                help='Modo de busca: (API) no site da Embrapa, (FILE) por arquivo CSV')
            if st.button('Verificar', use_container_width=True):
                response = save_viticulture(main_options[category], mode)
                if response.get('detail'):
                    st.toast(response.get('detail'), icon='❗')
                else:
                    st.toast(response.get('message'), icon='😍')

    with st.form('search_form', clear_on_submit=False, border=0):
        col1, col2 = st.columns(2)
        default_year = int(datetime.now().strftime('%Y'))
        subcategory = col1.selectbox('Subcategoria',
                                     options=list(sorted(sub_options.keys())),
                                     help='Informe uma subcategoria válida')
        year = col2.number_input('Ano', min_value=1970, value=default_year,
                                 help='Informe um ano de cadastro da subcategoria')

        submit = st.form_submit_button(label='Buscar', use_container_width=True)
        if submit:
            response = search_subcategories(sub_options[subcategory], year)
            if isinstance(response, list):
                with st.container():
                    df = pd.DataFrame(response).drop(columns=columns).dropna(axis=1, how='all')
                    st.dataframe(df)
            else:
                st.toast(response.get('detail'), icon='❗')


# Redirecting based by authentication
if st.session_state.authenticated:
    page_content()
else:
    login_page()
