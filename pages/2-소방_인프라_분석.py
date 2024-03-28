# -*- coding:utf-8 -*-
import streamlit as st
import geopandas as gpd
from streamlit_folium import folium_static
from shapely import wkt
# utils 패키지 내 필요한 함수들을 import
from utils.data_loader import load_data
from utils.map_visualization import display_fire_incidents_map, create_folium_map, display_folium_map_with_clusters, visualize_fire_water
from utils.ui_helpers import setup_sidebar_links, display_season_colors, create_html_button

# 페이지 설정
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_icon='🚒')

# 사이드바 설정
setup_sidebar_links()

# 데이터 로드
data = load_data("data/서울시_비상소화장치_좌표_구동.csv")
grid = load_data("data/seoul_500_grid_water.csv", encoding='euc-kr')
df = load_data("data/서울시_소방시설_좌표_구동.csv")
time = load_data("data/화재출동_골든타임.csv")

# `data['geometry']` 열에 저장된 WKT(Well-Known Text) 포맷의 지리적 데이터를 
# Shapely 라이브러리의 `loads` 함수를 사용하여 Point 객체로 변환
data['geometry'] = data['geometry'].apply(wkt.loads)  
_gdf = gpd.GeoDataFrame(data, geometry='geometry') # GeoDataFrame으로 변환

def main():
    # 메인 헤더
    st.header('서울시 소방 인프라 분석', divider="gray")
    
    # 메인 컨텐츠 컬럼 구성
    col1, col2 = st.columns([7, 3])
    
    with col1:  # 열 1 - 서울시 소방 시설 위치 시각화 섹션
        with st.container(border=True, height=750):

            # 부제목
            st.markdown('<h4>서울시 소방 인프라 위치 시각화</h4>', unsafe_allow_html=True) 

            # 3개의 탭 생성
            tab1, tab2, tab3 = st.tabs(["소방서 및 안전센터", "비상 소화장치", "소방용수"])

            with tab1: # 탭 1 - 소방서 및 안전센터
                # 선택된 구에 따라 동 선택
                # '서울시'를 추가한 구 선택
                gu_options = ['서울시'] + sorted(df['구'].unique().tolist())

                # st.columns를 사용하여 레이아웃을 설정
                col_gu, col_dong = st.columns(2)

                with col_gu:
                    selected_gu = st.selectbox('자치구 선택', gu_options, index=0)

                # 선택된 구에 따라 동 선택 옵션을 업데이트
                if selected_gu == '서울시':
                    filtered_df = df
                else:
                    with col_dong:
                        # '구 전체' 옵션을 동 선택기에 추가
                        dong_options = [f'{selected_gu} 전체'] + sorted(df[df['구'] == selected_gu]['동'].unique().tolist())
                        selected_dong = st.selectbox('동 선택', dong_options, index=0)

                        if selected_dong == f'{selected_gu} 전체':
                            filtered_df = df[df['구'] == selected_gu]
                        else:
                            filtered_df = df[(df['구'] == selected_gu) & (df['동'] == selected_dong)]

                # 지도 시각화 함수에 필터링된 데이터프레임을 전달
                create_folium_map(filtered_df)

            with tab2: # 탭 2 - 비상 위치 소화장치 클러스터링 시각화
                # '서울시'를 추가한 구 선택 옵션 생성
                sig_options = ['서울시'] + sorted(_gdf['구'].unique().tolist())

                # st.columns를 사용하여 구와 동 선택기를 가로로 배치합니다.
                col1_sig, col2_emd = st.columns([1,1])

                with col1_sig:
                    selected_sig = st.selectbox('자치구 선택:', sig_options, index=0)

                # 선택된 구에 따라 동 선택 옵션을 업데이트합니다.
                if selected_sig == '서울시':
                    filtered_gdf = _gdf
                else:
                    with col2_emd:
                        emd_options = [f'{selected_sig} 전체'] + sorted(_gdf[_gdf['구'] == selected_sig]['동'].unique().tolist())
                        selected_emd = st.selectbox('동 선택:', emd_options, index=0)

                    if selected_emd == f'{selected_sig} 전체':
                        filtered_gdf = _gdf[_gdf['구'] == selected_sig]
                    else:
                        filtered_gdf = _gdf[(_gdf['구'] == selected_sig) & (_gdf['동'] == selected_emd)]

                display_folium_map_with_clusters(filtered_gdf)

            with tab3: # 탭 3 - 소방용수 분포

                # 시각화 기준 설명
                with st.popover("💡 **시각화 기준 설명**"):
                    st.markdown("""
                    - **소방용수의 분포**: 이 지도상의 색상은 소방용수의 분포를 나타냅니다. 색이 **더 진할수록 소방용수의 양이 많음**을 의미합니다.
                    - **소화용수 접근성**: 서울시 내 대부분의 지역에서는 500미터 이내에 최소 한 개 이상의 소화용수 점이 위치하고 있어, 접근성이 높습니다.
                    - **높은 
                    소방용수 밀집 지역**: 일부 지역에서는 소방용수 점의 수가 100개를 넘는 경우도 있으며, 이는 해당 지역의 소방 안전 인프라가 잘 갖추어져 있음을 나타냅니다.
                    """)

                # 소방용수 분포 시각화
                visualize_fire_water(grid, column_name='소방용수_수')
    
    with col2:  # 열 2 - 소방 복지 및 정책

        with st.container(border=True, height=750):
            # 소방 관련 정보를 제공하는 버튼과 링크 생성
            create_html_button("소방 복지 및 정책")
            st.divider()
            st.link_button("일일 화재 현황 📈", "https://www.nfds.go.kr/dashboard/quicklook.do", use_container_width=True, help="한눈에 화재 현황을 확인해보세요.")
            st.link_button("화재예방법 🛡️", "https://www.nfds.go.kr/bbs/selectBbsList.do?bbs=B04", use_container_width=True, help="화재를 예방하는 방법을 알아보세요.")
            st.link_button("소화기 사용요령 🔥", "https://www.nfds.go.kr/bbs/selectBbsDetail.do?bbs=B06&bbs_no=7753&pageNo=1", use_container_width=True, help="소화기 사용법을 올바르게 알고 화재에 대응하세요.")
            st.link_button("옥내소화전 사용방법 🚒", "https://www.nfds.go.kr/bbs/selectBbsDetail.do?bbs=B06&bbs_no=7756&pageNo=1", use_container_width=True, help="옥내소화전 사용 방법을 숙지하세요.")
            st.link_button("소화기 사용기한 확인 ⏳", "https://bigdata-119.kr/service/frxtInfr#tab04", use_container_width=True, help="소화기의 사용 기한을 확인해 안전을 유지하세요.")
            st.link_button("주택용 소방시설 설치 🏠", "https://fire.seoul.go.kr/pages/cnts.do?id=4808", use_container_width=True, help="취약계층을 위한 주택용 소방시설 설치 정보입니다.")
            st.link_button("소방시설 불법행위신고 🚫", "https://fire.seoul.go.kr/pages/cnts.do?id=4113", use_container_width=True, help="불법 소방시설 행위를 신고해 포상금을 받으세요.")
            st.link_button("안전신문고 📢", "https://www.safetyreport.go.kr/#safereport/safereport", use_container_width=True, help="소방 안전 관련 불법 행위를 신고할 수 있는 곳입니다.")
            st.link_button("소방기술민원센터 💡", "https://www.safeland.go.kr/safeland/index.do", use_container_width=True, help="소방시설 및 화재 예방 관련 자료를 제공합니다.")
            st.link_button("칭찬하기 👏", "https://fire.seoul.go.kr/pages/cnts.do?id=184", use_container_width=True, help="소방관님들에게 감사의 메시지를 전하세요.")

    # 골든타임 초과 건물화재사고를 분석하는 섹션
    with st.container(border=True, height=650):

        # 부제목
        st.markdown('<h4>소방 서비스 접근성 분석: 골든타임 초과 건물화재사고</h4>', unsafe_allow_html=True) 
        
        # 열생성
        col1, col2 = st.columns([2, 8])
        
        with col1: # 열 1 - 골든타임, 마커 색상 정보

            # 골든타임 관련 정보를 제공하는 팝오버 생성
            with st.popover("⏰ **골든타임**", use_container_width=True):
                st.markdown('소방차 골든타임은 **7분**입니다. 골든타임 내에 소방대원이 도착하여 화재를 진압할 수 있다면, 인명 및 재산 피해를 최소화할 수 있습니다.')

            # 계절에 따른 골든타임 마커 색상 정보
            display_season_colors()
            
        with col2: # 열 2 - 화재 출동 골든타임 초과한 사건 지도 시각화           
            display_fire_incidents_map(time)

if __name__ == "__main__":
    main()
