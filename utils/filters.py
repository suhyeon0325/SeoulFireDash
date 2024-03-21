import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 
import geopandas as gpd
import matplotlib.pyplot as plt
import geopandas as gpd

# 구 선택 필터링 함수
def select_data(df, column_name='자치구', key_suffix=''):
    """
    자치구 선택을 통해 데이터를 필터링하는 함수.
    :param df: 데이터프레임
    :param column_name: 필터링할 컬럼명
    :param key_suffix: Streamlit 위젯의 고유 key 식별자에 추가될 접미사
    :return: 선택된 자치구에 해당하는 데이터프레임
    """
    selected = st.selectbox(f'{column_name} 선택', options=df[column_name].unique(), key=f'{column_name}_select{key_suffix}')
    return df[df[column_name] == selected]

# 동 선택 필터링 함수
def select_dong(df, column_name='동', key_suffix='_dong'):
    return select_data(df, column_name, key_suffix)

