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
    st.plotly_chart(fig)

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
    st.plotly_chart(fig)

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
                      width=700
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
    st.plotly_chart(fig)

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
