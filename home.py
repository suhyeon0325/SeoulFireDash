# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 
import geopandas as gpd
import matplotlib.pyplot as plt
import geopandas as gpd
from plotly.subplots import make_subplots
from utils.data_loader import set_page_config, load_data
from utils.filters import select_data
from utils.visualizations import visualize_bar_chart, visualize_pie_chart

# 페이지 설정
set_page_config()

# 데이터 불러오기
data = load_data("C:/Users/1qlqj/Desktop/multicamp_semi/SeoulFireDash/data/구별_화재발생_현황_2021_2022.csv")
df = load_data("data\화재발생_자치구별_현황(월별).csv", encoding='cp949')

st.title('서울시 화재사고 현황', help='이 페이지에서는 서울시 내의 최근 화재 사고 발생 통계, 화재 유형별 및 지역별 분석, 화재 예방 및 대응에 관한 정보를 제공합니다. 사용자는 화재 발생 빈도, 피해 규모, 대응 시간 등 다양한 데이터를 통해 서울시의 화재 안전 상태를 파악할 수 있으며, 화재 예방과 대응에 유용한 인사이트를 얻을 수 있습니다.')
st.divider()

# 서브헤더 생성
st.subheader('2022 서울시 화재 정보')

# 메트릭 열 생성
col1, col2, col3, col4 = st.columns([1,1,1,1])
# 2021, 2022 화재 사고 총합 컨테이너 생성
with col1:
    with st.container(height=130, border=True):
        st.metric(label="총 화재 건수", value='5396건', delta='+ 445건', delta_color="inverse")

with col2:
    with st.container(height=130, border=True):
        st.metric(label="총 피해인원", value='362명', delta='+ 45명', delta_color="inverse")

with col3:
    with st.container(height=130, border=True):
        st.metric(label="총 피해금액", value='16.59억', delta='- 0.17억', delta_color="inverse")

with col4:
    with st.container(height=130, border=True):
        st.metric(label="총 소실면적", value='34,065㎡', delta='+ 12,342㎡', delta_color="inverse")

# 그래프 시각화
with st.container(border=True, height=650):
    tab1, tab2, tab3, tab4 = st.tabs(["월별 화재발생 건수", "화재 발생 유형", "화재 피해 금액", "인평 피해 분석"])

    # 월별 화재발생 건수 탭 시각화
    with tab1:
        # 자치구 선택 및 데이터 필터링
        selected_df = select_data(df, '자치구', '_gu_select')

        # 월별로 표시할 x축 데이터
        months = [f"{i}월" for i in range(1, 13)]
        
        # y축 데이터에 해당하는 컬럼명 리스트
        y_axes = [[f"2021. {i:02d}" for i in range(1, 13)], [f"2022. {i:02d}" for i in range(1, 13)]]
        
        # 시각화
        visualize_bar_chart(selected_df, months, y_axes, names=['2021', '2022'], 
                            title=f'{selected_df["자치구"].iloc[0]}의 2021 vs 2022 월별 화재발생 건수',
                            xaxis_title='월', yaxis_title='건수', colors=['#032CA6', '#F25E6B'])


    # 화재발생 유형 파이차트로 시각화
    with tab2:
        # 자치구 선택 및 데이터 필터링
        selected_sig_data = select_data(data, '자치구', '_sig_select')

        # 화재 발생 유형별 데이터 집계
        labels = ['실화 발생', '방화 발생', '기타 발생']
        values_2021 = [
            selected_sig_data['2021_실화_발생'].sum(),
            selected_sig_data['2021_방화_발생'].sum(),
            selected_sig_data['2021_기타_발생'].sum()
        ]
        values_2022 = [
            selected_sig_data['2022_실화_발생'].sum(),
            selected_sig_data['2022_방화_발생'].sum(),
            selected_sig_data['2022_기타_발생'].sum()
        ]

        # 사용자 정의 색상
        custom_colors = ['#F25E6B', '#032CA6', '#FCE77C']

        # 시각화
        visualize_pie_chart(labels, [values_2021, values_2022], names=["2021", "2022"], 
                            title=f"{selected_sig_data['자치구'].iloc[0]} - 2021년 대비 2022년 화재 발생 유형 비교", 
                            colors=custom_colors)

