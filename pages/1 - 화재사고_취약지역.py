# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 
import geopandas as gpd
import matplotlib.pyplot as plt
import geopandas as gpd
from plotly.subplots import make_subplots
from utils.data_loader import set_page_config, load_data, load_shp_data
from utils.filters import select_data, select_dong
from utils.visualizations import visualize_bar_chart, visualize_pie_chart, visualize_bar_chart_updated, visualize_horizontal_bar_chart
from utils.map_visualization import create_and_show_map
from streamlit_option_menu import option_menu
st.set_page_config(
    page_title="화재사고 취약지역",
    initial_sidebar_state="expanded",
)
df = load_data("data/total_rank.csv", encoding='cp949')
gdf = load_shp_data("data/구경계_geo/구경계_geo.shp")
def menu():
    with st.sidebar:
        # 옵션 메뉴를 사용하여 메인 메뉴 생성
        selected = option_menu("메인 메뉴", ["화재사고 현황", '화재사고 취약지역', "소방 인프라 분석", "비상소화장치 위치 제안", "건의사항"], 
                                icons=['bi-fire', 'bi-exclamation-triangle-fill', 'bi-truck', 'bi-lightbulb', 'bi-chat-dots'], 
                                menu_icon="house", default_index=0)

    # 선택된 메뉴에 따라 페이지 전환
    if selected == '화재사고 현황':
        st.switch_page("서울시_화재사고_현황.py")
    elif selected == '화재사고 취약지역':
        st.switch_page("pages/1 - 화재사고_취약지역.py")
    elif selected == '소방 인프라 분석':
        st.switch_page('pages/2 - 서울시_소방_인프라.py')
    elif selected == '비상소화장치 위치 제안':
        st.switch_page('pages/3 - 비상소화장치_위치_제안.py')
    elif selected == '건의사항':
        st.switch_page('pages/4 - 건의사항.py')

# 메뉴 함수 호출
menu()
def main():

    


    columns_to_exclude = ["비상소화장치 설치개수 점수", "서울시 주거 시설 중 주택 비율 점수", "인구밀도(명/km^2) 점수", 
                        "노후 주택 수 점수", "소방관 1명당 담당인구 점수", "화재발생건수 점수", "안전센터 1개소당 담당인구 점수", 
                        "출동소요시간 점수", "순위", "전체 점수", "고령자 수 점수"]
    columns_for_df_09 = [col for col in df.columns if col not in columns_to_exclude]
    df_09 = df[columns_for_df_09]
    df_09.rename(columns={'서울시 주거 시설 중 주택 비율': '주택 중 아파트를 제외한 건물 비율'}, inplace=True)

    merged_data = gdf.merge(df, left_on='구', right_on='자치구')
    
    # 사이드바 설정
    view_selection = st.sidebar.radio("보고 싶은 분석 선택", ("분석 결과", "지도 시각화"), label_visibility="collapsed")

    if view_selection == "분석 결과":
        # 분석 결과 대시보드 구성
        st.header('화재사고 취약지역 분석', divider="gray")

        with st.container(border=True, height=670):
            st.subheader('서울시 주택화재 취약지역 분석')

            tab1, tab2, tab3 = st.tabs(['전체 보기', '상위 5개구만 보기', '표로 보기'])
            with tab1:
            
                selected_column = st.selectbox('분석 카테고리 선택', options=df_09.columns[1:], index=0, key='_selected_data_1')

                # 선택한 열에 대한 가로 막대 그래프 시각화
                visualize_horizontal_bar_chart(df, selected_column, title=f"서울시 자치구 {selected_column} 분석")

            with tab2:
                selected_column = st.selectbox('분석 카테고리 선택', options=df_09.columns[1:], index=0, key='_selected_data_2')

                # 선택된 열에 따라 하위 5개구 혹은 상위 5개구 시각화
                if selected_column == '비상소화장치 설치개수':
                    # 비상소화장치 설치 개수에 대해 하위 5개 구 시각화
                    df_sorted = df_09.nsmallest(5, selected_column)
                    title = f'{selected_column} - 하위 5개구 분석'
                else:
                    # 나머지 지표에 대해 상위 5개 구 시각화
                    df_sorted = df_09.nlargest(5, selected_column)
                    df_sorted = df_sorted.iloc[::-1]  # 상위 5개를 역순으로 정렬하여 그래프에 나타냄
                    title = f'{selected_column} - 상위 5개구 분석'

                # Plotly로 시각화
                fig = px.bar(df_sorted, y='자치구', x=selected_column,
                            labels={'자치구': '자치구', selected_column: selected_column},
                            title=title, orientation='h',
                            color=selected_column, color_continuous_scale=px.colors.sequential.Reds)

                fig.update_layout(plot_bgcolor='rgba(240, 240, 240, 0.6)')
                fig.update_yaxes(tickmode='array', tickvals=df_sorted['자치구'])

                # 스트림릿으로 그래프 표시
                
                st.plotly_chart(fig, use_container_width=True)

            with tab3:
                st.caption('표 상단의 열을 클릭하면, 해당 열을 기준으로 데이터를 오름차순 혹은 내림차순으로 정렬할 수 있습니다.')
                st.dataframe(df, height=450, use_container_width=True)


    elif view_selection == "지도 시각화":
        st.header('화재사고 취약지역 분석', divider="gray")
        # 지도 시각화 대시보드 구성
        with st.container(border=True, height=1000):
            st.subheader('취약 지역 지도 시각화')
            with st.expander("💡 **점수 기준**"):
                st.markdown("""
                    각 카테고리별로 지역의 취약성을 분석하여 순위를 매긴 뒤,
                    모든 카테고리의 순위를 합산하여 최종 점수를 산출했습니다.
                    :orange[**점수가 높을수록 소방 취약지역입니다.**]
                        
                    **카테고리**: 비상소화장치 설치개수, 주택 중 아파트를 제외한 건물 비율,	인구밀도(명/km^2),	노후 주택 수, 소방관 1명당 담당인구, 화재발생건수, 안전센터 1개소당 담당인구, 출동소요시간, 고령자 수
                """)

            # 지도 시각화
            html_string = create_and_show_map(
            data=merged_data,  # 'geometry' 열 포함 GeoDataFrame
            columns=['자치구', '전체 점수'], 
            key_on='feature.properties.자치구'
            )

            # 스트림릿에서 지도 표시
            st.components.v1.html(html_string, height=700)

if __name__ == "__main__":
    main()
