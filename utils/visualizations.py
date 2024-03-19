import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 
import geopandas as gpd
import matplotlib.pyplot as plt
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