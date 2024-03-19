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
from utils.filters import select_data, select_dong
from utils.visualizations import visualize_bar_chart, visualize_pie_chart, visualize_bar_chart_updated

# 페이지 설정
set_page_config()

# 데이터 불러오기
data = load_data("data/구별_화재발생_현황_2021_2022.csv")
df = load_data("data/화재발생_자치구별_현황(월별).csv", encoding='cp949')
dong = load_data("data/동별_화재발생_장소_2021_2022.csv")

def main():

    st.header('서울시 화재사고 현황', help='이 페이지에서는 서울시 내의 최근 화재 사고 발생 통계, 화재 유형별 및 지역별 분석에 관한 정보를 제공합니다. 2021, 2022년도의 데이터를 사용하였습니다.', divider='gray')

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
        tab1, tab2, tab3, tab4 = st.tabs(["월별 화재발생 건수", "화재 발생 유형", "화재 피해 금액", "인명 피해 분석"])

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
            col1, col2 = st.columns(2)

            # 첫 번째 컬럼에서 차트 유형 선택
            with col1:
                # 자치구 선택 및 데이터 필터링
                selected_sig_data = select_data(data, '자치구', '_sig_select')


            with col2:
                chart_type = st.selectbox(
                '차트 유형 선택',
                ('막대 그래프', '원형 차트'),  # 더 친숙하고 이해하기 쉬운 단어 사용
                key='chart_type'
                )


            if chart_type == '원형 차트':

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
                                    title=f"{selected_sig_data['자치구'].iloc[0]} - 2021년과 2022년 화재 발생 유형 분석", 
                                    colors=custom_colors)
                        
            elif chart_type == '막대 그래프':
                # 바차트 시각화 함수 호출
                visualize_bar_chart_updated(
                    df=selected_sig_data,
                    x_axes=['자치구', '자치구', '자치구'],  # x 축으로 사용될 열 이름
                    y_axes_list=[['2021_실화_발생', '2022_실화_발생'], ['2021_방화_발생', '2022_방화_발생'], ['2021_기타_발생', '2022_기타_발생']],
                    names_list=[['2021 실화', '2022 실화'], ['2021 방화', '2022 방화'], ['2021 기타', '2022 기타']],
                    title=f"{selected_sig_data['자치구'].iloc[0]} - 화재 발생 유형별 비교",
                    xaxis_titles=['실화 발생', '방화 발생', '기타 발생'],
                    yaxis_title='발생 건수',
                    colors_list=[['#F25E6B', '#032CA6'], ['#FAD04A', '#2B2726'], ['#9FC031', '#EEDFE2']]
                )
            
        # 화재 피해금액 시각화
        with tab3:
            col1, col2 = st.columns(2)

            with col1:
                # 자치구 선택 및 데이터 필터링
                selected_sig_data = select_data(data, '자치구', '_sig_select_tab3')

            with col2:
                # 차트 유형 선택
                chart_type = st.selectbox(
                    '차트 유형 선택',
                    ('막대 그래프', '원형 차트'),
                    key='chart_type_tab3'
                )

            if chart_type =='막대 그래프':
                # 시각화
                visualize_bar_chart_updated(
                    df=selected_sig_data,
                    x_axes=['자치구', '자치구', '자치구'],  # x 축으로 사용될 열 이름
                    y_axes_list=[['2021_소계_피해액', '2022_소계_피해액'], ['2021_부동산_피해액', '2022_부동산_피해액'], ['2021_동산_피해액', '2022_동산_피해액']],
                    names_list=[['2021 총 피해액', '2022 총 피해액'], ['2021 부동산 피해액', '2022 부동산 피해액'], ['2021 동산 피해액', '2022 동산 피해액']],
                    title='자치구별 화재 피해 금액 비교',
                    xaxis_titles=['총 피해액', '부동산 피해액', '동산 피해액'],
                    yaxis_title='피해액 (단위: 원)',
                    colors_list=[['#EE6A66', '#1E1A77'], ['#FAD04A', '#2B2726'], ['#9FC031', '#EEDFE2']]
                )

            elif chart_type == '원형 차트':
                # 화재 피해금액 데이터 집계
                labels = ['부동산 피해액', '동산 피해액']
                values_2021 = [
                    selected_sig_data['2021_부동산_피해액'].sum(),
                    selected_sig_data['2021_동산_피해액'].sum()
                ]
                values_2022 = [
                    selected_sig_data['2022_부동산_피해액'].sum(),
                    selected_sig_data['2022_동산_피해액'].sum()
                ]

                # 사용자 정의 색상
                custom_colors = ['#F25E6B', '#032CA6']

                # 화재 피해금액 비교를 위한 파이 차트 시각화
                # 2021년과 2022년 데이터를 각각 다른 파이 차트로 표시
                visualize_pie_chart(labels, [values_2021, values_2022], names=["2021", "2022"], 
                                    title=f"{selected_sig_data['자치구'].iloc[0]} - 2021년과 2022년 화재 피해 금액 비교", 
                                    colors=custom_colors)

        with tab4:
            col1, col2 = st.columns(2)
            
            with col1:
                # 자치구 선택 및 데이터 필터링
                selected_sig_4 = select_data(data, '자치구', '_sig_select_4')

            with col2:
                # 차트 유형 선택
                chart_type = st.selectbox(
                '차트 유형 선택',
                ('막대 그래프', '원형 차트'),  # 사용자에게 친숙한 용어 사용
                key='chart_type_tab4'
                )

            if chart_type == '막대 그래프':
                # 막대 그래프 시각화 코드 추가 (예시: 인명피해 비교)
                visualize_bar_chart_updated(
                    df=selected_sig_4,
                    x_axes=['자치구', '자치구', '자치구'], 
                    y_axes_list=[
                        ['2021_소계_인명피해', '2022_소계_인명피해'],
                        ['2021_사망_인명피해', '2022_사망_인명피해'],
                        ['2021_부상_인명피해', '2022_부상_인명피해']
                    ],
                    names_list=[
                        ['2021 소계 인명피해', '2022 소계 인명피해'],
                        ['2021 사망 인명피해', '2022 사망 인명피해'],
                        ['2021 부상 인명피해', '2022 부상 인명피해']
                    ],
                    title='자치구별 인명피해 비교',
                    xaxis_titles=['소계 인명피해', '사망 인명피해', '부상 인명피해'],
                    yaxis_title='인원 수',
                    colors_list=[
                        ['#EE6A66', '#1E1A77'], 
                        ['#FAD04A', '#2B2726'], 
                        ['#9FC031', '#EEDFE2']
                    ]
                )

            elif chart_type == '원형 차트':
                # 2021년 인명피해 데이터 집계 및 파이차트 시각화
                labels_p = ['사망 인명피해', '부상 인명피해']
                values_2021_p = [
                    selected_sig_4['2021_사망_인명피해'].sum(),
                    selected_sig_4['2021_부상_인명피해'].sum()
                ]

                # 2022년 인명피해 데이터 집계 및 파이차트 시각화
                values_2022_p = [
                    selected_sig_4['2022_사망_인명피해'].sum(),
                    selected_sig_4['2022_부상_인명피해'].sum()
                ]

                # 사용자 정의 색상
                custom_colors = ['#F25E6B', '#032CA6']

                # 시각화
                visualize_pie_chart(labels_p, [values_2021_p, values_2022_p], names=["2021", "2022"], 
                                    title=f"{selected_sig_data['자치구'].iloc[0]} - 2021년과 2022년 화재 사고 인명 피해 분석", 
                                    colors=custom_colors)

    # 동별 화재발생 현황 그래프
    with st.container(border=True, height=650):
        col1, col2 = st.columns(2)

        # 첫 번째 컬럼에서 차트 유형 선택
        with col1:
            # 구 선택
            df_filtered_by_gu = select_data(dong, '자치구', '_gu')

        with col2:
            # 동 선택
            df_filtered_by_dong = select_dong(df_filtered_by_gu, '동', '_dong_1')

        # 화재 발생 장소 유형
        place_types = ['단독주택', '공동주택', '기타주택', '학교', '일반업무', '판매시설', '숙박시설', '종교시설', '의료시설', '공장 및 창고', '작업장', '위락오락시설', '음식점', '일상서비스시설', '기타']

        # 장소 유형별 화재 발생 건수 데이터를 '장소 유형'과 '건수' 컬럼을 가진 새로운 데이터프레임으로 변환
        df_treemap = df_filtered_by_dong.melt(id_vars=['자치구', '동'], value_vars=place_types, var_name='장소 유형', value_name='건수')

        # 건수가 0 이상인 데이터만 필터링
        df_treemap = df_treemap[df_treemap['건수'] > 0]

        # 사용자 지정 색상 리스트
        colors = ['#F25E6B', '#F2C744', '#A1BF34', '#EEDFE2', '#FCE77C', '#E2D0F8', '#DCE2F0', '#F2EFBB', '#D5D971', '#6779A1', '#9B7776','#1BBFBF', '#D94B2B', '#D98F89', '#FFDEDC', '#ACC7B4']

        # 트리맵 생성
        fig = px.treemap(df_treemap, path=['자치구', '동', '장소 유형'], values='건수',
                        color='장소 유형',
                        hover_data=['건수'],
                        color_discrete_sequence=colors)

        # 차트 제목 설정
        fig.update_layout(title='동별 화재 장소유형 트리맵')

        # 전반적인 텍스트 스타일 조정
        fig.update_layout(font=dict(family="Arial, sans-serif", size=14, color="black"))

        # 툴팁 커스터마이징
        fig.update_traces(
            hovertemplate='장소 유형: %{label}<br>건수: %{value}<br>전체 대비 비율: %{percentRoot:.2%}',
            textfont=dict(family="Arial, sans-serif", size=12, color="black")
        )

        # Streamlit에 트리맵 표시
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()