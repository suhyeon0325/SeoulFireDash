# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 
import geopandas as gpd
import matplotlib.pyplot as plt
import geopandas as gpd
from plotly.subplots import make_subplots
from utils.data_loader import load_data
from utils.filters import select_data, select_dong, select_chart_type
from utils.visualizations import visualize_bar_chart, visualize_pie_chart, visualize_trend_by_district_with_tabs, visualize_facilities, visualize_bar_chart_updated
from streamlit_option_menu import option_menu


# 페이지 설정
st.set_page_config(layout="wide",
   initial_sidebar_state="expanded", page_icon="🔥")

st.sidebar.page_link("서울시_화재사고_현황.py", label="서울시 화재사고 현황", icon="🔥")
st.sidebar.page_link("pages/1-화재사고_취약지역.py", label="화재사고 취약지역", icon="⚠️")
st.sidebar.page_link("pages/2-소방_인프라_분석.py", label="소방 인프라 분석", icon="🚒")
st.sidebar.page_link("pages/3-비상소화장치_위치_제안.py", label="비상소화장치 위치 제안", icon="🧯")
st.sidebar.page_link("pages/4-건의사항.py", label="건의사항", icon="💬")



# 데이터 불러오기
df = load_data("data/18_23_서울시_화재.csv")



def main():
    
    st.header('서울시 화재사고 현황', help='이 페이지에서는 서울시 내의 최근 화재 사고 발생 통계, 화재 유형별 및 지역별 분석에 관한 정보를 제공합니다.', divider='gray')
    # 메트릭 열 생성
    st.button("**기간: 2024-02-24~2024-03-25**", disabled=True)
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    # 2021, 2022 화재 사고 총합 컨테이너 생성
    with col1:
        with st.container(height=130, border=True):
            st.metric(label="**화재 건수 🔥**", value='465건', delta='- 64건', delta_color="inverse",
                      help = '전년동기: 529건')

    with col2:
        with st.container(height=130, border=True):
            st.metric(label="**인명피해 🚑**", value='21명', delta='+ 9명', delta_color="inverse",
                      help='사망자 수 2명, 부상자 수 19명 | 전년동기: 인명피해 12명, 사망자 수 2명, 부상자 수 10명')

    with col3:
        with st.container(height=130, border=True):
            st.metric(label="**총 재산피해 💸**", value='36.79억', delta='+ 17.79억', delta_color="inverse",
                      help = '부동산피해 567,425 천원, 동산피해 3,111,368 천원 | 전년동기: 총 재산피해 1,899,163 천원, 부동산피해 511,694 천원, 동산피해 1,387,469 천원')

    with col4:
        with st.container(height=130, border=True):
            st.metric(label="**재산 피해/건당 💰**", value='7,911 천원', delta='+ 4,321 천원', delta_color="inverse",
                      help = '전년동기: 3,590 천원')
    visualize_trend_by_district_with_tabs(df)




if __name__ == "__main__":
    main()