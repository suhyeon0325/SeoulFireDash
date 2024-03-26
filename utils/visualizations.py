import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from plotly.subplots import make_subplots

# 바차트 시각화
def visualize_bar_chart(df, x_axis, y_axes, names, title, xaxis_title='월', yaxis_title='건수', colors=['#032CA6', '#F25E6B']):
    """
    막대 차트 시각화 함수.
    :param df: 데이터프레임
    :param x_axis: X축 데이터
    :param y_axes: Y축 데이터 리스트 (각 Y축 데이터에 해당하는 컬럼명 리스트)
    :param names: 각 데이터의 이름 리스트
    :param title: 차트 제목
    :param xaxis_title: X축 제목
    :param yaxis_title: Y축 제목
    :param colors: 막대 색상 리스트
    """
    fig = go.Figure()
    for y_axis, name, color in zip(y_axes, names, colors):
        fig.add_trace(go.Bar(x=x_axis, y=df[y_axis].values.flatten(), name=name, marker_color=color))
    fig.update_layout(title=title, xaxis_title=xaxis_title, yaxis_title=yaxis_title, legend_title='년도', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

# 바차트 시각화 서브플롯
def visualize_bar_chart_updated(df, x_axes, y_axes_list, names_list, title, xaxis_titles, yaxis_title, colors_list):
    """
    각 카테고리별로 서브플롯에 막대 차트를 시각화하는 함수.
    
    :param df: 데이터프레임
    :param x_axes: x 축에 사용될 데이터의 리스트
    :param y_axes_list: y 축에 사용될 데이터의 리스트의 리스트 (각 카테고리별 y 축 데이터 목록)
    :param names_list: 각 막대의 이름 리스트의 리스트
    :param title: 차트 제목
    :param xaxis_titles: x 축 제목의 리스트
    :param yaxis_title: y 축 제목
    :param colors_list: 막대 색상의 리스트의 리스트
    """
    # 서브플롯 생성
    fig = make_subplots(rows=1, cols=len(x_axes), subplot_titles=xaxis_titles)
    
    # 각 카테고리별로 막대 차트 추가
    for i, (x_axis, y_axes, names, colors) in enumerate(zip(x_axes, y_axes_list, names_list, colors_list), start=1):
        for y_axis, name, color in zip(y_axes, names, colors):
            fig.add_trace(
                go.Bar(x=df[x_axis], y=df[y_axis], name=name, marker_color=color),
                row=1, col=i
            )
    
    # 레이아웃 업데이트
    fig.update_layout(title=title, yaxis_title=yaxis_title, barmode='group')
    
    # Streamlit에 차트 표시
    st.plotly_chart(fig, use_container_width=True)

def visualize_pie_chart(labels, values_list, names, title, colors=['#F25E6B', '#032CA6', '#FCE77C']):
    """
    파이 차트 시각화 함수.
    :param labels: 파이 차트 레이블 리스트
    :param values_list: 각 파이 차트의 값들의 리스트 (각 리스트는 파이 차트 한 개의 값을 담고 있음)
    :param names: 각 파이 차트의 이름 리스트
    :param title: 차트 제목
    :param colors: 파이 차트 색상 리스트
    """
    fig = make_subplots(rows=1, cols=len(values_list), specs=[[{'type':'domain'}] * len(values_list)])
    for i, (values, name) in enumerate(zip(values_list, names), start=1):
        fig.add_trace(go.Pie(labels=labels, values=values, name=name, marker_colors=colors), 1, i)
    fig.update_layout(title_text=title)
    st.plotly_chart(fig)

# 소방취약지역 가로그래프
def visualize_horizontal_bar_chart(df, selected_column, title, color_scale='Reds'):
    """
    스트림릿에서 선택한 열에 따른 자치구별 가로 막대 그래프를 시각화하는 함수.
    
    :param df: 데이터프레임
    :param selected_column: 사용자가 선택한 열 이름
    :param title: 그래프 제목 (기본값: '가로 막대 그래프')
    :param color_scale: 막대 색상 스케일 (사용자가 선택 가능)
    """
    df_sorted = df.sort_values(by=selected_column)
    
    fig = px.bar(df_sorted, y='자치구', x=selected_column,
                 labels={'자치구': '자치구', selected_column: selected_column},
                 title=title, orientation='h',
                 color=selected_column, color_continuous_scale=px.colors.sequential.__dict__[color_scale])
    
    # y축 레이블이 더 넓게 표시되도록 조정 및 글꼴 크기 조정, 레전드 위치 조정
    fig.update_layout(plot_bgcolor='rgba(240, 240, 240, 0.6)',
                      margin=dict(l=50, b=100),  # 바텀 마진을 늘려 레전드에 공간을 만듭니다.
                      width=700,height=500
                      )
    fig.update_yaxes(tickmode='array', tickvals=df_sorted['자치구'], tickfont=dict(size=10))
    
    st.plotly_chart(fig, use_container_width=True)


# 시설 함수
def visualize_facilities(df_selected):
    fig = go.Figure()

    # 제공된 색상 목록
    colors = ['#F25E6B', '#F2C744', '#A1BF34', '#EEDFE2', '#FCE77C', '#E2D0F8', '#DCE2F0', '#F2EFBB', '#D5D971', '#6779A1', '#9B7776','#1BBFBF', '#D94B2B', '#D98F89', '#FFDEDC', '#ACC7B4']
    
    # 시설 유형 목록
    facility_types = ['단독주택', '공동주택', '기타주택', '학교', '일반업무', '판매시설', '숙박시설', '종교시설', '의료시설', '공장 및 창고', '작업장', '위락오락시설', '음식점', '일상서비스시설', '기타']
    
    # 시설 유형과 색상 매핑
    color_map = dict(zip(facility_types, colors))

    for column in df_selected.columns[2:]:  # '자치구'와 '동' 컬럼을 제외한 나머지 컬럼에 대해 반복
        total = df_selected[column].sum()  # 해당 시설 유형의 총합
        # 시설 유형별로 지정된 색상 사용, 레전드 표시하지 않음
        fig.add_trace(go.Bar(x=[column], y=[total], marker_color=color_map.get(column), showlegend=False))

    fig.update_layout(title="시설 유형별 총계", xaxis_title="시설 유형", yaxis_title="총계")
    st.plotly_chart(fig, use_container_width=True)

# 송파구 연도별 화재발생현황(동)
def visualize_fire_counts_by_selected_year(df, selected_year):
    df_year = df[df['시점'] == selected_year].sort_values(by='화재건수', ascending=True)
    fig = px.bar(df_year, x='화재건수', y='동', text_auto=True,
                 title=f"{selected_year}년 송파구 화재건수",
                 color='화재건수',
                 color_continuous_scale=px.colors.sequential.OrRd)
    fig.update_traces(textfont_size=10, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_yaxes(tickmode='array', tickvals=df_year['동'].unique())
    fig.update_layout(height=600)
    return fig

# 송파구 연도별 거주 인구
def visualize_population_by_selected_year(df, selected_year):
    df_year = df[df['시점'] == selected_year].sort_values(by='전체인구', ascending=True)
    fig = px.bar(df_year, x='전체인구', y='동', text_auto=True,
                 title=f"{selected_year}년 송파구 거주인구",
                 color='전체인구',
                 color_continuous_scale=px.colors.sequential.OrRd)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_yaxes(tickmode='array', tickvals=df_year['동'].unique())
    return fig

def visualize_elderly_population_by_year(df, time_column='시점'):
    """
    각 연도별로 '65세이상 인구'를 시각화하는 함수입니다.
    
    :param df: 데이터프레임, '시점'과 '65세이상 인구', '동' 컬럼을 포함해야 합니다.
    :param time_column: 시간을 나타내는 컬럼의 이름, 기본값은 '시점'입니다.
    """
    unique_years = df[time_column].unique() # '시점' 컬럼의 고유값을 가져옵니다.
    
    selected_year = st.selectbox("연도 선택", options=sorted(unique_years, reverse=True), key='year_select') # 연도를 선택할 수 있는 selectbox를 생성합니다.
    
    df_year = df[df[time_column] == selected_year].sort_values(by='65세이상 인구', ascending=True) # 선택된 연도에 해당하는 데이터를 추출하고, '65세이상 인구' 기준으로 정렬합니다.
    
    # Plotly Express를 사용하여 막대 그래프를 생성합니다.
    fig = px.bar(df_year, x='65세이상 인구', y='동', text_auto=True,
                 title=f"{selected_year}년 송파구 노년인구",
                 color='65세이상 인구',
                 color_continuous_scale=px.colors.sequential.OrRd)
    
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) # 텍스트 스타일 조정
    fig.update_yaxes(tickmode='array', tickvals=df_year['동']) # y축 조정
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

def visualize_elderly_population_ratio_by_selected_year(df, selected_year):
    df_year = df[df['시점'] == selected_year].copy()
    df_year.loc[:, '65세이상 인구 비율'] = (df_year['65세이상 인구'] / df_year['전체인구']) * 100
    df_year.sort_values(by='65세이상 인구 비율', ascending=True, inplace=True)

    fig = px.bar(df_year, x='65세이상 인구 비율', y='동', text_auto=True,
                 title=f"{selected_year}년 송파구 노년인구 비율",
                 color='65세이상 인구 비율',
                 color_continuous_scale=px.colors.sequential.OrRd)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_yaxes(tickmode='array', tickvals=df_year['동'].unique())
    return fig

import plotly.express as px

def visualize_housing_type_distribution_by_selected_dong(df, selected_dong):
    df_dong = df[df['동'] == selected_dong]
    df_melted = df_dong.melt(id_vars=['시점', '동'], var_name='주택 유형', value_name='수량')
    fig = px.bar(df_melted, x='주택 유형', y='수량', text_auto=True, color='수량',
                 color_continuous_scale=px.colors.sequential.OrRd, title=f"{selected_dong} 주택 유형별 분포")
    return fig

# 18~23 시각화 함수
def visualize_trend_by_district_with_tabs(df):
    columns = ['화재건수', '사망', '부상', '인명피해 계', '부동산피해(천원)', '동산피해(천원)', '재산피해(천원)', '재산피해/건당(천원)']
    years = [f'{year}' for year in range(18, 24)]  # 연도 리스트 (2018-2023)

    # 미리 selected_districts 변수를 정의해둡니다.
    selected_districts = []

    left_column, right_column = st.columns([1, 3])

    with left_column:
        with st.container(border=True, height=600):
            option = st.radio("**데이터 범위 선택**", ("서울시 전체", "각 구별로 비교하기"), horizontal=True)

            if option == "서울시 전체":
                df = df[df['자치구'] == '서울시']
            else:
                districts_options = df['자치구'].unique().tolist()
                if '서울시' in districts_options:
                    districts_options.remove('서울시')
                default_districts = [district for district in ['강북구', '송파구', '영등포구'] if district in districts_options]
                selected_districts = st.multiselect('**자치구 선택**', options=districts_options, default=default_districts)
                
                if not selected_districts:
                    st.error('적어도 하나 이상의 자치구를 선택해야 합니다.', icon="🚨")
                    return  # 추가 처리를 중지하고 함수 종료
                
                df = df[df['자치구'].isin(selected_districts)]

    with right_column:
        with st.container(border=True, height=600):
            # 선택된 자치구가 있거나, "서울시 전체" 옵션이 선택된 경우에 그래프를 표시합니다.
            if selected_districts or option == "서울시 전체":
                tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(columns)
                tabs = [tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8]

                for tab, column in zip(tabs, columns):
                    with tab:
                        data_list = []
                        for year in years:
                            for index, row in df.iterrows():
                                data_list.append({'자치구': row['자치구'], '연도': f'20{year}', column: row[f'{year}_{column}']})

                        new_df = pd.DataFrame(data_list)
                        # 그래프 제목 설정을 위한 조건문 추가
                        if option == "서울시 전체":
                            title = f'서울시 전체 {column} 추세 (2018-2023)'
                            fig = px.line(new_df, x='연도', y=column, color='자치구', title=title)
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)

                            if column == "화재건수":
                                st.image('data/사진/2024_서울시_월별화재건수_예측.png')
 
                        else:
                            title = f'자치구별 {column} 추세 (2018-2023)'
                            fig = px.line(new_df, x='연도', y=column, color='자치구', title=title)
                            st.plotly_chart(fig, use_container_width=True)
            
# 서울시 화재사고 현황페이지_장소유형_트리맵 시각화 함수
def display_treemap(dong, select_data, select_dong):
    col1, col2 = st.columns(2)

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

    # 차트 제목 및 스타일 설정
    fig.update_layout(title='동별 화재 장소유형 트리맵', font=dict(family="Arial, sans-serif", size=14, color="black"))

    # 툴팁 커스터마이징
    fig.update_traces(
        hovertemplate='장소 유형: %{label}<br>건수: %{value}<br>전체 대비 비율: %{percentRoot:.2%}',
        textfont=dict(family="Arial, sans-serif", size=12, color="black")
    )

    # Streamlit에 트리맵 표시
    st.plotly_chart(fig, use_container_width=True)                            

def visualize_top_bottom_districts(df, column_name='비상소화장치 설치개수'):
    """
    선택된 카테고리에 따라 상위 5개구 혹은 하위 5개구를 시각화하는 함수입니다.
    
    :param df: 데이터프레임
    :param column_name: 분석할 카테고리의 열 이름. 기본값은 '비상소화장치 설치개수'
    """
    # 분석 카테고리 선택
    selected_column = st.selectbox('분석 카테고리 선택', options=df.columns[1:], index=0, key='_selected_data_2')

    if selected_column == column_name:
        # 하위 5개 구 시각화
        df_sorted = df.nsmallest(5, selected_column)
        title = f'{selected_column} - 하위 5개구 분석'
    else:
        # 상위 5개 구 시각화
        df_sorted = df.nlargest(5, selected_column).iloc[::-1]  # 역순 정렬
        title = f'{selected_column} - 상위 5개구 분석'

    # 시각화
    fig = px.bar(df_sorted, y='자치구', x=selected_column, labels={'자치구': '자치구', selected_column: selected_column},
                 title=title, orientation='h', color=selected_column, color_continuous_scale=px.colors.sequential.Reds)

    fig.update_layout(plot_bgcolor='rgba(240, 240, 240, 0.6)')
    fig.update_yaxes(tickmode='array', tickvals=df_sorted['자치구'])

    # 스트림릿에 그래프 표시
    st.plotly_chart(fig, use_container_width=True)