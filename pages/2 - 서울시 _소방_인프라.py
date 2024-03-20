# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 
import geopandas as gpd
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
from shapely import wkt
from plotly.subplots import make_subplots
from utils.data_loader import set_page_config, load_data, load_shp_data
from utils.filters import select_data, select_dong
from utils.visualizations import visualize_bar_chart, visualize_pie_chart, visualize_bar_chart_updated, visualize_horizontal_bar_chart
from utils.map_visualization import create_and_show_map, display_folium_map_with_clusters, visualize_fire_water

# 페이지 설정
set_page_config()

data = load_data("data/서울시_비상소화장치_좌표_구동.csv")
grid = load_data("data/seoul_500_grid_water.csv", encoding='euc-kr')

# `geometry` 열을 Point 객체로 변환
data['geometry'] = data['geometry'].apply(wkt.loads)

# GeoDataFrame 생성
gdf = gpd.GeoDataFrame(data, geometry='geometry')


def main():

    # 스트림릿 대시보드
    st.header('서울시 소방 인프라', divider="gray")

    with st.container(border=True, height=650):   
        st.subheader('서울시 소방 인프라 시각화')
        tab1, tab2 = st.tabs(["비상 소화장치", "소방용수"])
        with tab1:
            # 서울시 비상소화장치 클러스터링 시각화
            display_folium_map_with_clusters(data)

        with tab2:
            # 서울시 비상용수 시각화
            visualize_fire_water(grid, column_name='소방용수_수')
           

 

if __name__ == "__main__":
    main()    