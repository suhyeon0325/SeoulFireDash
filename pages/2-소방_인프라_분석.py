# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 
import geopandas as gpd
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
from shapely import wkt
from streamlit_option_menu import option_menu
from plotly.subplots import make_subplots
from utils.data_loader import load_data, load_shp_data
from utils.filters import select_data, select_dong
from utils.visualizations import visualize_bar_chart, visualize_pie_chart, visualize_bar_chart_updated, visualize_horizontal_bar_chart
from utils.map_visualization import create_and_show_map, create_folium_map, display_folium_map_with_clusters, visualize_fire_water

# 페이지 설정
st.set_page_config(
   layout="wide",
   initial_sidebar_state="expanded", page_icon='🚒')
st.sidebar.page_link("서울시_화재사고_현황.py", label="서울시 화재사고 현황", icon="🔥")
st.sidebar.page_link("pages/1-화재사고_취약지역.py", label="화재사고 취약지역", icon="⚠️")
st.sidebar.page_link("pages/2-소방_인프라_분석.py", label="소방 인프라 분석", icon="🚒")
st.sidebar.page_link("pages/3-비상소화장치_위치_제안.py", label="비상소화장치 위치 제안", icon="🧯")
st.sidebar.page_link("pages/4-건의사항.py", label="건의사항", icon="💬")
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
    
    col1, col2 = st.columns([7, 3])
    with col1:        

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
                with st.popover("💡 **시각화 기준 설명**"):
                    st.markdown("""
                    - **소방용수의 분포**: 이 지도상의 색상은 소방용수의 분포를 나타냅니다. 색이 **더 진할수록 소방용수의 양이 많음**을 의미합니다.
                    - **소화용수 접근성**: 서울시 내 대부분의 지역에서는 500미터 이내에 최소 한 개 이상의 소화용수 점이 위치하고 있어, 접근성이 높습니다.
                    - **높은 소방용수 밀집 지역**: 일부 지역에서는 소방용수 점의 수가 100개를 넘는 경우도 있으며, 이는 해당 지역의 소방 안전 인프라가 잘 갖추어져 있음을 나타냅니다.
                    """)

                # 서울시 비상용수 시각화
                visualize_fire_water(grid, column_name='소방용수_수')
    with col2:
        
        with st.container(border=True, height=700):
            st.markdown("""
                <div style='text-align: center; margin-bottom: 20px;'>
                    <button style='
                        border: none;
                        pointer-events: none;
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        font-weight: bold;
                        margin: 4px 2px;
                        cursor: pointer;
                        background-color: #F24C3D;
                        border-radius: 8px;'>
                    소방 복지 및 정책
                    </button>
                </div>
                """, unsafe_allow_html=True)
            
            st.link_button("일일 화재 현황 📈", "https://www.nfds.go.kr/dashboard/quicklook.do", use_container_width=True, help="한눈에 화재 현황을 확인해보세요.")
            st.link_button("화재예방법 🛡️", "https://www.nfds.go.kr/bbs/selectBbsList.do?bbs=B04", use_container_width=True, help="화재를 예방하는 방법을 알아보세요.")
            st.link_button("소화기 사용요령 🔥", "https://www.nfds.go.kr/bbs/selectBbsDetail.do?bbs=B06&bbs_no=7753&pageNo=1", use_container_width=True, help="소화기 사용법을 올바르게 알고 화재에 대응하세요.")
            st.link_button("옥내소화전 사용방법 🚒", "https://www.nfds.go.kr/bbs/selectBbsDetail.do?bbs=B06&bbs_no=7756&pageNo=1", use_container_width=True, help="옥내소화전 사용 방법을 숙지하세요.")
            st.link_button("소화기 사용기한 확인 ⏳", "https://bigdata-119.kr/service/frxtInfr#tab04", use_container_width=True, help="소화기의 사용 기한을 확인해 안전을 유지하세요.")
            st.link_button("주택용 소방시설 설치 🏠", "https://fire.seoul.go.kr/pages/cnts.do?id=4808", use_container_width=True, help="취약계층을 위한 주택용 소방시설 설치 정보입니다.")
            st.link_button("소방시설 불법행위신고 🚫", "https://fire.seoul.go.kr/pages/cnts.do?id=4113", use_container_width=True, help="불법 소방시설 행위를 신고해 포상금을 받으세요.")
            st.link_button("안전신문고 📢", "https://www.safetyreport.go.kr/#safereport/safereport", use_container_width=True, help="소방 안전 관련 불법 행위를 신고할 수 있는 곳입니다.")
            st.link_button("소방민원센터 📜", "https://www.safeland.go.kr/somin/index.do", use_container_width=True, help="소방 관련 민원을 신청할 수 있는 곳입니다.")
            st.link_button("소방기술민원센터 💡", "https://www.safeland.go.kr/safeland/index.do", use_container_width=True, help="소방시설 및 화재 예방 관련 자료를 제공합니다.")
            st.link_button("칭찬하기 👏", "https://fire.seoul.go.kr/pages/cnts.do?id=184", use_container_width=True, help="소방관님들에게 감사의 메시지를 전하세요.")


           

 

if __name__ == "__main__":
    main()    