# streamlit_app.py

import time  # to simulate a real time data, time loop
import numpy as np  # np mean, np random
import streamlit as st
import pandas as pd
from io import StringIO


st.set_page_config(
    page_title="Med4Pro Анализатор протоколов",
    page_icon="✅",
    layout="wide",
)
def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Имя пользователя", on_change=password_entered, key="username")
        st.text_input(
            "Пароль", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Имя пользователя", on_change=password_entered, key="username")
        st.text_input(
            "Пароль", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Пользователь не существует или пароль не верен")
        return False
    else:
        # Password correct.
        return True

if check_password():
    st.title("Med4Pro - Анализатор протоколов")

    # read  from a github repo
    base_standarts_url = "https://github.com/lxxr/mz_2023_h/raw/main/base_standarts.xlsx"


    uploaded_file = st.file_uploader("Выберите протоколы из ЕМИАС для анализа")
    columns = ['Пол пациента','Дата рождения пациента','ID пациента','Код МКБ-10','Диагноз','Дата оказания услуги','Должность','Назначения','Замечания']

    data=[]
    if uploaded_file is not None:
        data=pd.read_excel(uploaded_file, sheet_name='Sheet1')

    @st.cache_data
    def get_data() -> pd.DataFrame:
       return pd.DataFrame(data)#pd.read_csv(dataset_url)

    if uploaded_file is not None:
#        print(data)
        df = get_data()
        df["Отклонения в назначениях"] = "Отклонений не обнаружено"

        st.checkbox("По ширине окна", value=False, key="use_container_width")
        st.dataframe(df.style.highlight_max(axis=0),use_container_width=st.session_state.use_container_width)
