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

# 페이지 설정
set_page_config()

df = load_data("\data\total_rank.csv")
gdf = load_shp_data("data\구경계_geo\구경계_geo.shp")

df_09 = df.iloc[:, 0:9]
df_09.rename(columns={'서울시 주거 시설 중 주택 비율': '주택 중 아파트를 제외한 건물 비율'}, inplace=True)

merged_data = gdf.merge(df, left_on='구', right_on='자치구')

def main():
    
    # 스트림릿 대시보드
    st.header('자치구별 데이터 시각화', divider="gray")

    with st.container(border=True, height=650):

        tab1, tab2 = st.tabs(["전체 자치구 통계", "상/하위 자치구 분석"])
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
            st.plotly_chart(fig)

    with st.container(border=True, height=650):        

        st.subheader('서울시 소방 취약지역 시각화')
        with st.expander("💡 **점수 기준**"):
            st.markdown("""
                    각 카테고리별로 지역의 취약성을 분석하여 순위를 매긴 뒤,
                    모든 카테고리의 순위를 합산하여 최종 점수를 산출했습니다.
                    :orange[**점수가 높을수록 소방 취약지역입니다.**]
                        
                    **카테고리**: 비상소화장치 설치개수, 주택 중 아파트를 제외한 건물 비율,	인구밀도(명/km^2),	노후 주택 수, 소방관 1명당 담당인구, 화재발생건수, 안전센터 1개소당 담당인구, 출동소요시간
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