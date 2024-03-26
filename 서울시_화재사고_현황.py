# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
# utils 패키지 내 필요한 함수들을 import
from utils.data_loader import load_data
from utils.visualizations import display_treemap, visualize_trend_by_district_with_tabs, visualize_facilities
from utils.etc import setup_sidebar_links, select_data, select_dong

# 스트림릿 페이지 기본 설정
st.set_page_config(layout="wide",
   initial_sidebar_state="expanded", page_icon="🔥")

# 사이드바 내비게이션 링크
setup_sidebar_links()

# 데이터 불러오기
df = load_data("data/18_23_서울시_화재.csv")
dong = load_data("data/동별_화재발생_장소_2021_2022.csv")

# "서울시 전체" 데이터 처리
seoul_total = dong.drop(['자치구', '동'], axis=1).sum().rename('서울시 전체')
seoul_total['자치구'] = '서울시 전체'
seoul_total['동'] = '전체'

# dong 최종 데이터 프레임 조합
dong = pd.concat([dong, pd.DataFrame([seoul_total])], ignore_index=True)
dong = dong.drop(columns=["Unnamed: 0"])

def main():
    # 페이지 헤더 설정    
    st.header('서울시 화재사고 현황', help='이 페이지에서는 서울시 내의 최근 화재 사고 발생 통계, 화재 유형별 및 지역별 분석에 관한 정보를 제공합니다.', divider='gray')
    
    # 기간 정보 표시
    st.button("**기간: 2024-02-24~2024-03-25**", disabled=True)

    #메트릭 시각화
    col1, col2, col3, col4 = st.columns([1,1,1,1])
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

    # 지역별 화재 추이 시각화                        
    visualize_trend_by_district_with_tabs(df)

    # 동별 화재발생 장소 분석 시각화
    with st.container(border=True, height=700):
        st.markdown('<h4>화재 장소 유형 분석</h4>', unsafe_allow_html=True) 
        tab1, tab2 = st.tabs(["트리맵으로 보기", "막대 그래프로 보기"])
        with tab1:            
            display_treemap(dong, select_data, select_dong)

        with tab2:
            selected_gu = st.selectbox("자치구 선택", options=dong['자치구'].unique())
            df_selected = dong[dong['자치구'] == selected_gu]

            visualize_facilities(df_selected)

if __name__ == "__main__":
    main()