# -*- coding:utf-8 -*-
import streamlit as st
import geopandas as gpd
from streamlit_folium import folium_static
from shapely import wkt
# utils 패키지 내 필요한 함수들을 import
from utils.data_loader import load_data
from utils.map_visualization import display_fire_incidents_map, create_folium_map, display_folium_map_with_clusters, visualize_fire_water
from utils.etc import setup_sidebar_links, display_season_colors, display_fire_safety_links, create_html_button

# 페이지 설정
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_icon='🚒')

# 사이드바 설정
setup_sidebar_links()

# 데이터 로드
data = load_data("data/서울시_비상소화장치_좌표_구동.csv")
grid = load_data("data/seoul_500_grid_water.csv", encoding='euc-kr')
df = load_data("data/서울시_소방서_안전세터_구조대.csv")
time = load_data("data/화재출동_골든타임.csv")

# GeoDataFrame 생성
data['geometry'] = data['geometry'].apply(wkt.loads)  # `geometry` 열을 Point 객체로 변환
gdf = gpd.GeoDataFrame(data, geometry='geometry')

def main():
    # 메인 헤더
    st.header('서울시 소방 인프라', divider="gray")
    
    # 메인 컨텐츠 컬럼 구성
    col1, col2 = st.columns([7, 3])
    
    with col1:  # 첫 번째 컬럼 시작
        with st.container(border=True, height=650):
            st.markdown('<h4>서울시 소방 시설 위치 시각화</h4>', unsafe_allow_html=True) 
            # 소방 인프라 시각화 탭
            tab1, tab2, tab3 = st.tabs(["소방서 및 안전센터", "비상 소화장치", "소방용수"])

            with tab1:
                # 소방서 및 안전센터 지도 시각화
                m = create_folium_map(df)
                folium_static(m)

            with tab2:
                # 비상 소화장치 위치 클러스터링 시각화
                display_folium_map_with_clusters(data)

            with tab3:
                # 소방용수 분포 시각화
                visualize_fire_water(grid, column_name='소방용수_수')
    
    with col2:  # 두 번째 컬럼 시작
        with st.container(border=True, height=650):
            # 소방 관련 정보 버튼 및 링크
            create_html_button("소방 복지 및 정책")
            display_fire_safety_links()

    # 골든타임 분석 섹션
    with st.container(border=True, height=650):
        st.markdown('<h4>소방 서비스 접근성 분석: 골든타임 초과 건물화재사고</h4>', unsafe_allow_html=True) 
        col1, col2 = st.columns([2, 8])
        
        with col1: 
     
            with st.popover("⏰ **골든타임**", use_container_width=True):
                st.markdown('소방차 골든타임은 7분입니다. 골든타임 내에 소방대원이 도착하여 화재를 진압할 수 있다면, 인명 및 재산 피해를 최소화할 수 있습니다. 따라서 소방서의 위치 선정과 응급 대응 시스템의 효율성이 매우 중요합니다.')

            # 골든타임 정보 표시
            display_season_colors()
            
        with col2:            
            # 화재 출동 골든타임 초과 지도 시각화
            display_fire_incidents_map(time)

if __name__ == "__main__":
    main()
