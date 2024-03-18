import streamlit as st
import pandas as pd
import geopandas as gpd

# 페이지 설정 함수
def set_page_config():
    st.set_page_config(
        page_title="메인",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded"
    )

# csv 데이터 로딩 함수
@st.cache_data
def load_data(csv_file, encoding=None):
    if encoding:
        return pd.read_csv(csv_file, encoding=encoding)
    else:
        return pd.read_csv(csv_file)

# SHP 데이터 로딩 함수
@st.cache_data
def load_shp_data(shp_file):
    return gpd.read_file(shp_file)

# GeoJson 데이터 로딩 함수
@st.cache_data
def load_json_data(geojson_file):
    return gpd.read_file(geojson_file)
