# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 
import geopandas as gpd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from streamlit_folium import folium_static
import geopandas as gpd
from plotly.subplots import make_subplots
from utils.data_loader import set_page_config, load_data, load_shp_data, load_excel_data
from utils.filters import select_data, select_dong
from utils.visualizations import visualize_bar_chart, visualize_housing_type_distribution_by_selected_dong, visualize_elderly_population_ratio_by_selected_year, visualize_elderly_population_by_year, visualize_population_by_selected_year, visualize_fire_counts_by_selected_year, visualize_pie_chart, visualize_bar_chart_updated, visualize_horizontal_bar_chart
from utils.map_visualization import create_and_show_map, create_fire_equip_map

# 페이지 설정

st.set_page_config(
    page_title="비상소화장치 위치 제안",
    initial_sidebar_state="expanded",
)

data = load_excel_data("data/(송파소방서)비상소화장치.xlsx")
df = load_data("data/2020-2022_송파구_동별_화재건수.csv", encoding='CP949')
df_P = load_data("data/2022-2023_송파구_인구.csv", encoding='CP949')
df_O = load_data("data/2021-2023_송파구_고령자현황.csv", encoding='CP949')
df_H = load_data("data/2020_송파구_주택.csv", encoding='CP949')

df = df.replace('-', 0)
df['화재건수'] = df['화재건수'].astype(int)

df_H = df_H.replace('X', 0)
df_H['단독주택'] = df_H['단독주택'].astype(int)
df_H['연립주택'] = df_H['연립주택'].astype(int)
df_H['다세대주택'] = df_H['다세대주택'].astype(int)
df_H['비거주용건물내주택'] = df_H['비거주용건물내주택'].astype(int)

def main():
    view_selection = st.sidebar.radio("선택", ("송파구 비상소화장치 제안 위치", "송파구 종합 정보 분석"), label_visibility="collapsed")
    if view_selection == "송파구 비상소화장치 제안 위치":
        # 스트림릿 대시보드
        st.header('비상소화장치 위치 제안', divider="gray")
        st.caption('현재 서비스는 송파구 내에서만 사용가능합니다.')
        with st.container(border=True, height=150):  
            st.subheader('송파구 비상소화장치 제안 위치')
    
    elif view_selection == "송파구 종합 정보 분석":

        st.header('비상소화장치 위치 제안', divider="gray")

        tab1, tab2, tab3, tab4, tab5, tab6= st.tabs(["송파구 소방 인프라", "화재 건수", "노년 인구", " 주택 현황", "재개발", "정리"])

        with tab1:

            col1, col2 = st.columns([7, 3])
            with col1:
                with st.container(border=True, height=600):
                    st.subheader('송파구 소방 인프라 분석')   
                    create_fire_equip_map(data)  # fire_equip_df는 당신의 데이터프레임 변수명입니다.

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

        # 송파구 화재 건수 분석
        with tab2:
            st.subheader('송파구 화재 건수 분석')
            select = st.radio("선택", ["동별 화재발생 건수", "연도별 화재발생 건수"],horizontal=True, label_visibility="collapsed")
            if select == '연도별 화재발생 건수':
                # 2020~2023 총 화재 건수 시각화
                new_data = pd.DataFrame({'시점': [2023],'화재건수': [382]})
                df_grouped = df.groupby(['시점'])['화재건수'].sum().reset_index()
                시점 = df_grouped['시점'].tolist()
                화재건수 = df_grouped['화재건수'].tolist()
                df_grouped_updated = pd.concat([df_grouped, new_data]).reset_index(drop=True)
                시점 = df_grouped_updated['시점'].tolist()
                화재건수 = df_grouped_updated['화재건수'].tolist()
                colors = ['#fc8d59', '#fdcc8a', '#e34a33', '#b30000']
                fig = go.Figure()
                fig.add_trace(go.Bar(x=시점, y=화재건수, width=0.4, marker_color=colors, text=df_grouped_updated['화재건수']))
                fig.update_layout(title_text='송파구 2020~2023 총 화재건수', xaxis_type='category',
                                yaxis_title='화재건수', xaxis_title='시점')
                st.plotly_chart(fig)

            else:
                # 연도 선택 위젯
                selected_year = st.selectbox('연도를 선택하세요.', options=sorted(df['시점'].unique(), reverse=True))

                # 선택된 연도에 대한 화재건수 시각화 함수 호출
                fig = visualize_fire_counts_by_selected_year(df, selected_year)
                st.plotly_chart(fig, use_container_width=True)
        
        # 송파구 노년 인구 분석
        with tab3:
            st.subheader('송파구 노년 인구 분석')
            select = st.radio("선택", ["거주인구", "노년인구", "동별 노년인구", "노년인구 비율"],horizontal=True, label_visibility="collapsed")

            if select == '거주인구':
                # 연도 선택 위젯
                selected_year = st.selectbox('연도를 선택하세요.', options=sorted(df_O['시점'].unique(), reverse=True))

                # 선택된 연도에 대한 거주인구 시각화 함수 호출
                fig = visualize_population_by_selected_year(df_O, selected_year)
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)

            elif select == '노년인구':
                시점 = df_P['시점'].tolist()
                노년인구 = df_P['노년 전체 인구'].tolist()
                시점.reverse()

                colors = ['tomato', 'crimson', 'darkred', 'lightsalmon']
                fig = go.Figure()
                fig.add_trace(go.Bar(x=시점, y=노년인구, marker_color=colors, width=0.4, text=df_P['노년 전체 인구']))
                fig.update_layout(title_text='송파구 2022~2023년도 노년인구 수', yaxis_title='노년인구', xaxis_title='시점')
                st.plotly_chart(fig)

            elif select == '동별 노년인구':
                
                # 선택된 연도에 대한 거주 인구 시각화
                visualize_elderly_population_by_year(df_O)
            
            else:
                # 연도 선택 위젯
                selected_year = st.selectbox('연도를 선택하세요.', options=sorted(df_O['시점'].unique(), reverse=True))

                # 선택된 연도에 대한 노년인구 비율 시각화 함수 호출
                fig = visualize_elderly_population_ratio_by_selected_year(df_O, selected_year)
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)

        # 송파구 주택현황 분석
        with tab4:
            st.subheader('송파구 주택현황 분석')
            select_1 = st.radio("선택", ["동별 주택유형 분포", "동별 주택수"], horizontal=True, label_visibility="collapsed")
            if select_1 == "동별 주택유형 분포":
                # 동 선택 위젯
                selected_dong = st.selectbox('동을 선택하세요.', options=sorted(df_H['동'].unique()))

                # 선택된 동에 대한 주택 유형별 분포 시각화 함수 호출
                fig = visualize_housing_type_distribution_by_selected_dong(df_H, selected_dong)
                st.plotly_chart(fig, use_container_width=True)

            # 주택 현황 - 동별 주택 수
            else: 
                df_total = df_H[['동', '소계']]
                df_total_sorted = df_total.sort_values('소계', ascending=True)

                # 가로 막대 그래프 그리기
                fig_total_sorted = px.bar(df_total_sorted, y='동', x='소계', text='소계',
                                        orientation='h',  # 가로 막대 그래프 설정
                                        color='소계', color_continuous_scale=px.colors.sequential.OrRd,
                                        title="송파구 동별 주택 수(2020년)")
                fig_total_sorted.update_layout(height=600)
                st.plotly_chart(fig_total_sorted, use_container_width=True)
if __name__ =="__main__":
    main()
