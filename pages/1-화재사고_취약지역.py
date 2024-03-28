# -*- coding:utf-8 -*-
import streamlit as st
# utils 패키지 내 필요한 함수들을 import
from utils.data_loader import load_data
from utils.visualizations import visualize_vertical_bar_chart, visualize_top_districts_with_seoul_average
from utils.map_visualization import create_and_show_map
from utils.ui_helpers import setup_sidebar_links

# 스트림릿 페이지 설정
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_icon='⚠️')

# 데이터 로드
df = load_data("data/total_rank.csv", encoding='cp949')
gdf = load_data("data/구경계_geo/구경계_geo.shp")

# 사이드바 링크 설정
setup_sidebar_links()

# 분석에서 보여주지 않을 열들 정의(점수 열들은 시각화 X)
columns_to_exclude = ["비상소화장치 설치개수 점수", "서울시 주거 시설 중 주택 비율 점수", "인구밀도(명/km^2) 점수", 
                          "노후 주택 수 점수", "소방관 1명당 담당인구 점수", "화재발생건수 점수", "안전센터 1개소당 담당인구 점수", 
                          "출동소요시간 점수", "순위", "전체 점수", "고령자 수 점수"]
    
# 점수 열들을 제외하고 데이터 프레임 재구성
df_09 = df[[col for col in df.columns if col not in columns_to_exclude]]
    
# 열이름 변경('서울시 주거 시설 중 주택 비율' -> '주택 중 아파트를 제외한 건물 비율')
df_09 = df_09.rename(columns={'서울시 주거 시설 중 주택 비율': '주택 중 아파트를 제외한 건물 비율'})
    
# '순위'와 '전체 점수' 열만 포함하고, '순위' 기준으로 오름차순 정렬한 새로운 데이터 프레임 생성
df_3 = df[['자치구', '순위', '전체 점수']].sort_values(by='순위', ascending=True)
    
# GeoDataFrame과 기존 DataFrame을 합치기 위해 '구'열과 '자치구' 열을 기준으로 병합
merged_data = gdf.merge(df, left_on='구', right_on='자치구')

def main():

    # 헤더 설정
    st.header('화재사고 취약지역 분석', divider="gray")

    # 주택화재 취약지역 분석
    with st.container(border=True, height=700):

        # 부제목
        st.markdown('<h4>서울시 주택화재 취약지역 분석</h4>', unsafe_allow_html=True)

        # 탭 생성
        tab1, tab2, tab3 = st.tabs(['전체 보기', '상/하위 5개구만 보기', '테이블로 보기'])

        with tab1: # 탭 1 - 전체 보기

            # 분석 카테고리 선택 메뉴 생성
            selected_column = st.selectbox('분석 카테고리 선택', options=df_09.columns[1:], index=0, key='_selected_data_1')
            
            # 선택한 카테고리에 따라 막대 차트 시각화
            visualize_vertical_bar_chart(df_09, selected_column, title=f"서울시 자치구별 {selected_column} 분석")

        with tab2: # 탭 2 - 상/하위 5개구만 보기
            visualize_top_districts_with_seoul_average(df_09)

        with tab3: # 탭 3 - 표로 보기

            # 안내 문구
            st.caption('테이블 상단의 열을 클릭하면, 해당 열을 기준으로 데이터를 오름차순 혹은 내림차순으로 정렬할 수 있습니다.')
            
            # 데이터 프레임 시각화
            st.dataframe(df, height=500, use_container_width=True)

    # 지도 시각화 대시보드 구성
    col1, col2 = st.columns([7, 3])
    with col1: # 열 1 - 구별 취약지역 점수지도 시각화 섹션
        
        with st.container(border=True, height=700): 
            st.markdown('<h4>서울시 구별 취약지역 점수 지도</h4>', unsafe_allow_html=True) 

            # 점수 기준에 대한 설명을 제공하는 팝오버 생성
            with st.popover("💡 **점수 기준**"):
                st.markdown("""
                    각 카테고리별로 지역의 취약성을 분석하여 순위를 매긴 뒤,
                    모든 카테고리의 순위를 합산하여 최종 점수를 산출했습니다.
                    :orange[**점수가 높을수록 소방 취약지역입니다.**]
                        
                    **카테고리**: 비상소화장치 설치개수, 주택 중 아파트를 제외한 건물 비율,	인구밀도(명/km^2),	노후 주택 수, 소방관 1명당 담당인구, 화재발생건수, 안전센터 1개소당 담당인구, 출동소요시간, 고령자 수
                """)

            # 취약지역 점수 지도 시각화
            html_string = create_and_show_map(_data=merged_data, columns=['자치구', '전체 점수'], key_on='feature.properties.자치구')
            st.components.v1.html(html_string, height=570)

    with col2: # 열 2 - 취약점수 순위와 점수를 보여주는 데이터 프레임 섹션
        
        with st.container(border=True, height=700): 
            st.markdown("**취약점수 순위**")
            st.dataframe(df_3, height=600, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
