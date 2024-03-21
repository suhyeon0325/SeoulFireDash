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

def main():

    # 스트림릿 대시보드
    st.header('비상소화장치 위치 제안', divider="gray")
    st.caption('현재 서비스는 송파구 내에서만 사용가능합니다.')

if __name__ =="__main__":
    main()
