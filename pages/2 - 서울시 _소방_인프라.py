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
from utils.map_visualization import create_and_show_map, create_folium_map, display_folium_map_with_clusters, visualize_fire_water

# 페이지 설정
set_page_config()

data = load_data("data/서울시_비상소화장치_좌표_구동.csv")
grid = load_data("data/seoul_500_grid_water.csv", encoding='euc-kr')
df = load_data("data/서울시_소방서_안전세터_구조대.csv")

# `geometry` 열을 Point 객체로 변환
data['geometry'] = data['geometry'].apply(wkt.loads)

# GeoDataFrame 생성
gdf = gpd.GeoDataFrame(data, geometry='geometry')


def main():

    # 스트림릿 대시보드
    st.header('서울시 소방 인프라', divider="gray")
    
    col1, col2 = st.columns([3, 9])
    with col1:
        with st.container(border=True, height=700):
            st.write('무언가 추가해 볼 예정..')

    with col2:        

        with st.container(border=True, height=700):   
            st.subheader('서울시 소방 인프라 시각화')
            tab1, tab2, tab3 = st.tabs(["소방서 및 안전센터", "비상 소화장치", "소방용수"])

            with tab1:
                m = create_folium_map(df)
                folium_static(m)


            with tab2:
                # 서울시 비상소화장치 클러스터링 시각화
                display_folium_map_with_clusters(data)

            with tab3:
                with st.expander("💡 **시각화 기준 설명**"):
                    st.markdown("""
                    - **소방용수의 분포**: 이 지도상의 색상은 소방용수의 분포를 나타냅니다. 색이 **더 진할수록 소방용수의 양이 많음**을 의미합니다.
                    - **소화용수 접근성**: 서울시 내 대부분의 지역에서는 500미터 이내에 최소 한 개 이상의 소화용수 점이 위치하고 있어, 접근성이 높습니다.
                    - **높은 소방용수 밀집 지역**: 일부 지역에서는 소방용수 점의 수가 100개를 넘는 경우도 있으며, 이는 해당 지역의 소방 안전 인프라가 잘 갖추어져 있음을 나타냅니다.
                    """)

                # 서울시 비상용수 시각화
                visualize_fire_water(grid, column_name='소방용수_수')
           

 

if __name__ == "__main__":
    main()    