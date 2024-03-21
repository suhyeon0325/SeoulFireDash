# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
from streamlit_folium import folium_static
import geopandas as gpd
from plotly.subplots import make_subplots
from utils.data_loader import set_page_config, load_data, load_shp_data, load_excel_data
from utils.filters import select_data, select_dong
from utils.visualizations import visualize_bar_chart, visualize_pie_chart, visualize_bar_chart_updated, visualize_horizontal_bar_chart
from utils.map_visualization import create_and_show_map, create_fire_equip_map

# 페이지 설정
set_page_config()

df = load_excel_data("data/(송파소방서)비상소화장치.xlsx")



def main():

    # 스트림릿 대시보드
    st.header('비상소화장치 위치 제안', divider="gray")
    st.caption('현재 서비스는 송파구 내에서만 사용가능합니다.')
    with st.container(border=True, height=150):  
        st.subheader('송파구 비상소화장치 제안 위치')

    col1, col2 = st.columns([7, 3])
    with col1:
        with st.container(border=True, height=600):
            st.subheader('송파구 소방 인프라 분석')   
            create_fire_equip_map(df)  # fire_equip_df는 당신의 데이터프레임 변수명입니다.

    with col2:
        with st.container(border=False, height=600):
            with st.container(border=True, height=138):
                st.metric(label="송파구 비상소화장치", value='34개', delta= ' (평균대비)',
                        delta_color="normal", help="미접수 거래는 반영되지 않았습니다.")
            with st.container(border=True, height=138):
                st.metric(label="송파구 소방용수", value='ㅇ', delta='ㅇ',
                        delta_color="normal", help="강서구의 1월 거래량은 총 236건입니다.")
            with st.container(border=True, height=138):
                st.metric(label="송파구 화재출동 건수", value='ㅇ', delta='ㅇ',
                        delta_color="normal", help="강남구의 1월 평균 거래가는 158,170만원입니다.")
            with st.container(border=True, height=138):
                st.metric(label="송파구 소방서 및 안전센터", value='송파구', delta='송파구',
                        delta_color="normal", help="성동구의 1월 평균 건물면적은 84.75㎡입니다.")

            

             

if __name__ =="__main__":
    main()
