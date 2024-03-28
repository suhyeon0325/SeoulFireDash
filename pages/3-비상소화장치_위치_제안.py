# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
# utils 패키지 내 필요한 함수들을 import
from utils.ui_helpers import setup_sidebar_links, create_html_button, show_location_info
from utils.data_loader import load_data, get_locations_data
from utils.map_visualization import create_fire_equip_map, display_fire_extinguisher_map
from utils.visualizations import (
    visualize_housing_type_distribution_by_selected_dong,
    visualize_fire_incidents,
    visualize_elderly_population_ratio_by_selected_year,
    visualize_elderly_population_by_year,
    visualize_population_by_selected_year,
    visualize_fire_counts_by_selected_year
)

# 페이지 설정
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded", page_icon='🧯'
)

# 사이드바 설정
setup_sidebar_links()

# 데이터 로드
data = load_data("data/(송파소방서)비상소화장치.xlsx")
df = load_data("data/2020-2022_송파구_동별_화재건수.csv", encoding='CP949')
df_P = load_data("data/2022-2023_송파구_인구.csv", encoding='CP949')
df_O = load_data("data/2021-2023_송파구_고령자현황.csv", encoding='CP949')
df_H = load_data("data/2020_송파구_주택.csv", encoding='CP949')

# 데이터 전처리
df = df.replace('-', 0) # '-' 값을 0으로 대체
df['화재건수'] = df['화재건수'].astype(int) # '화재건수' 열의 데이터 타입을 정수형으로 변환

# 주택 데이터셋에서 'X'값을 0으로 대체하고 데이터 타입을 정수형으로 변환
df_H = df_H.replace('X', 0)
df_H = df_H.astype({'단독주택': int, '연립주택': int, '다세대주택': int, '비거주용건물내주택': int})

def main():
    # 대시보드 헤더 설정
    st.header('비상소화장치 위치 제안', divider="gray")
    st.caption('현재 서비스는 송파구 내에서만 사용가능합니다.')

    # 비상소화장치 제안 위치 섹션
    col1, col2 = st.columns([7,4])
    with col1: # 열 1 - 비상소화장치 위치 지도 시각화
        with st.container(border=True, height=650):  
            col3, col4 = st.columns([7,3])
            with col3: # 열 3 - 부제목 섹션
               st.markdown('<h4>송파구 비상소화장치 제안 위치</h4>', unsafe_allow_html=True)

            with col4: # 열 4 - 위치 선정 방법 설명
                with st.popover("💡 **위치 선정 방법**"):
                    st.markdown("""
                            <div style="font-family: sans-serif;">
                            <h4>선정 단계</h4>
                            <ol>
                                <li><strong>화재 주택 밀집 지역 파악:</strong> 우선적으로 화재가 자주 발생하는 주택이 밀집된 지역을 선별했습니다.</li>
                                <li><strong>지역 상세 분석:</strong> 선택된 지역 및 인접 지역을 상세히 조사하여 화재 위험 요인을 식별했습니다.</li>
                                <li><strong>설치 필요 지역 결정:</strong> 
                                    <ul>
                                        <li>비상소화장치가 없는 화재 건물 밀집 지역을 설치 대상으로 선정했습니다.</li>
                                        <li>화재 위험이 없는 지역이라도, 길이 좁고 노후한 건물이 많아 위험성이 높은 곳은 설치를 고려했습니다.</li>
                                    </ul>
                                <li><strong>우선순위 결정:</strong> 
                                    <ul>
                                        <li>인구 밀도와 소방 인프라 접근성, 도로 상황을 평가하였습니다.</li>
                                        <li>유사한 특성을 가진 지역을 군집화하고, 우선순위를 매깁니다.</li> 
                                    </ul>                                  
                                </ol>
                                <h4>우선순위 별 색상 코드</h4>
                                <ul>
                                    <li><font color="red"><strong>빨간색:</strong></font> 1순위</li>
                                    <li><font color="orange"><strong>노란색:</strong></font> 2순위</li>
                                    <li><font color="green"><strong>초록색:</strong></font> 3순위</li>
                                    <li><font color="blue"><strong>파란색:</strong></font> 4순위</li>
                                </ul>
                            </div>
                        """, unsafe_allow_html=True)


            # 송파구 중심 좌표 설정 및 지도 시각화
            center = [37.514543, 127.106597]
            locations = get_locations_data()
            display_fire_extinguisher_map(center, locations)

    with col2: # 열 2 - 각 위치에 대한 상세 정보 제공
        with st.container(border=True, height=650):  
            create_html_button('각 위치별 상세 정보')

            col3, col4 = st.columns([1,1])
            with col3:
                # 1번 위치 상세 정보
                show_location_info(st, "🔴 1번 위치", """
                    **잠실동 / 경위도좌표 X,Y (37.5085071,127.0825862)**
                    - **길이 좁아**서 소방차가 들어가기 힘듦
                    - **소화전이 위치**한 곳
                    - **노후 주택**이 많은 곳
                    """, [('data/사진/01_좌표.png', '좌표사진'), ('data/사진/01_주변_1.png', '주변사진'), ('data/사진/01_주변_2.png', '주변사진')])
                
                # 3번 위치 상세 정보
                show_location_info(st, "🔵 3번 위치", """
                    **삼전동 / 경위도좌표 X,Y (37.50231025,127.0901942)**
                    - **필로티 구조빌딩**이 밀집
                    """, [('data/사진/03_좌표.png', '좌표사진'), ('data/사진/03_주변_1.png', '주변사진'), ('data/사진/03_주변_2.png', '주변사진')])

                # 5번 위치 상세 정보
                show_location_info(st, "🔵 5번 위치", """
                    **삼전동 / 경위도좌표 X,Y (37.504103,127.090679)**                
                    - 길이 그리 좁지는 않으나, **주차 공간이 거주 지역에 배치되어** 소방차의 통행이 불가능함
                    - **주거지역 인근에 플라스틱 패널**로 된 구조물이 있어, 화재 위험성을 고려하여 선정
                    """, [('data/사진/05_좌표.png', '좌표사진'), ('data/사진/05_주변_1.png', '주변사진'), ('data/사진/05_주변_2.png', '주변사진')])

                # 7번 위치 상세 정보
                show_location_info(st, "🔵 7번 위치", """
                    **석촌동 / 경위도좌표 X,Y (37.50097974, 127.1000492)**
                    - **소방차 접근이 힘든 길**과, **노후화가 진행된 주택들**이 많이 밀집
                    - 비상소화장치 장소를 선정
                    """, [('data/사진/07_좌표.png', '좌표사진'), ('data/사진/07_주변_1.png', '주변사진'), ('data/사진/07_주변_2.png', '주변사진')])
                
                # 9번 위치 상세 정보
                show_location_info(st, "🔵 9번 위치", """
                    **방이동 / 경위도좌표 X,Y (37.51174,127.110053)**
                    - 주변에 **식당•술집 골목**이 있고, 주택가로 들어오면 길이 확 좁아짐
                    - 여기도 **소방차 진입**에 시간이 많이 걸릴 것 같음
                    - 지나다니는 **사람들이 많아** 차가 지나갈 때 움직이기 힘든 골목
                    """, [('data/사진/09_좌표.png', '좌표사진'), ('data/사진/09_주변_1.png', '주변사진'), ('data/사진/09_주변_2.png', '주변사진')])

                # 11번 위치 상세 정보
                show_location_info(st, "🟡 11번 위치", """
                    **가락본동 / 경위도좌표 X,Y (37.499000, 127.120611)**
                    - **넓은 도로와 좁은 도로가 반복**되는 곳
                    - **신축건물과 노후건물**이 공존하는 구역
                    - 마커가 찍힌 곳은 좁지만, **주변 길들이 관리가 잘 되어 있음**
                    - **임시로 주차**되어 있는 경우, 길이 좁아지는 곳이 많음
                    """, [('data/사진/11_좌표.png', '좌표사진'), ('data/사진/11_주변.png', '주변사진')])

                # 13번 위치 상세 정보
                show_location_info(st, "🟢 13번 위치", """
                    **송파2동 / 경위도좌표 X,Y (37.500694, 127.112639)**
                    - **식당이 많고 좁은 골목**이 많아 차량 통행이 많은 구역
                    - **소방차 진입 시간이 지체될 것**으로 예상
                    - 소화기가 설치된 주택이 많음을 관찰
                    - **사거리, 단독/노후주택이 밀집**되어 있고, **좁은 뒷골목들**이 많음
                    - 이 골목들은 대로와 연결되어 있지 않아, **소방차는 블록을 한 바퀴 돌아야 도달** 가능
                    - **학교 근처 상가건물 사거리**에 비상소화장치를 설치하는 것이 유리
                    """, [('data/사진/13_좌표.png', '좌표사진'), ('data/사진/13_주변.png', '주변사진'), ('data/사진/13_주변_도로_1.png', '주변 도로 사진: 진입하기 힘들다.'), ('data/사진/13_주변_도로_2.png', '주변 도로 사진: 차가 많이 다닌다.')])

                # 15번 위치 상세 정보
                show_location_info(st, "🔵 15번 위치", """
                    **마천2동 / 경위도좌표 X,Y (37.499138,127.149098)**
                    - **화재가 났던 구역보다 로드맵 상에서 안 보이는 지역**에 비상소화장치 설치 고려
                    - **주차된 차량**이 많음
                    """, [('data/사진/15_좌표.png', '좌표사진'), ('data/사진/15_주변_1.png', '주변사진'), ('data/사진/15_주변_2.png', '주변사진')])

                # 17번 위치 상세 정보
                show_location_info(st, "🟢 17번 위치", """
                    **거여1동 / 경위도좌표 X, Y(37.497698, 127.143332)**
                    - **낡은 주택**이 많고 **좁은 길**, **경사**가 많음
                    - 길에 **정차된 차량** 때문에 통행이 더 어려움
                    - 소방차 진입 시간을 고려하여 **비상소화장치 설치** 필요
                    """, [('data/사진/17_좌표.png', '좌표사진'), ('data/사진/17_주변_1.png', '주변사진'), ('data/사진/17_주변_2.png', '주변사진')])

                # 19번 위치 상세 정보
                show_location_info(st, "🔵 19번 위치", """
                    **오금동 / 경위도좌표X, Y (37.502313, 127.134786)**
                    - **오래된 주택**이 많고 길에 **주정차된 차량과 쓰레기** 등 장애물이 많음
                    - 근처 길이 모두 **좁아 비상소화장치 필요성**이 높음
                    - **송파소방서** 관할구역 내에서도 **눈에 띄게 좁은 길이 많은 곳**
                    - **비상소화장치 선정지역**으로 고려해도 좋을 것 같음
                    """, [('data/사진/19_좌표.png', '좌표사진'), ('data/사진/19_주변.png', '주변사진')])

            with col4:

                # 2번 위치 상세 정보
                show_location_info(st, "🔴 2번 위치", """
                    **잠실동 / 경위도좌표 X,Y (37.50511389,127.0817572)**
                    - **길이 좁아서 소방차가 들어가기 힘든 곳**
                    - **소화전이 위치한 곳**
                    - **노후 주택이 많은 곳**
                    """, [('data/사진/02_좌표.png', '좌표사진'), ('data/사진/02_주변_1.png', '주변사진'), ('data/사진/02_주변_2.png', '주변사진')])

                # 4번 위치 상세 정보
                show_location_info(st, "🔵4번 위치", """
                    **삼전동 / 경위도좌표 X,Y (37.50094046,127.0936817)**
                    - **길이 굉장히 좁음**
                    """, [('data/사진/04_좌표.png', '좌표사진'), ('data/사진/04_주변_1.png', '주변사진'), ('data/사진/04_주변_2.png', '주변사진')])

                # 6번 위치 상세 정보
                show_location_info(st, "🔵 6번 위치", """
                    **석촌동 / 경위도좌표 X,Y (37.49991962,127.0974103)**
                    - **좁은 길은 있지만 소방차가 못 들어갈 만한 지역은 없음**
                    - 불법 주차된 차가 있다면 소방차 진입이 어려울 수 있음                  
                    """, [('data/사진/06_좌표.png', '좌표사진'), ('data/사진/06_주변_1.png', '주변사진'), ('data/사진/06_주변_2.png', '주변사진')])

                # 8번 위치 상세 정보
                show_location_info(st, "🔵 8번 위치", """
                    **송파1동 / 경위도좌표 X,Y (37.50884075, 127.1087034)**
                    - 최근 **새로 지어진 건물이 많음**
                    - **놀이터 및 보행로, 좁은 길이 많고** 지나다니는 사람이 많아 일반 차량 진입에도 시간이 많이 걸림
                    """, [('data/사진/08_좌표.png', '좌표사진'), ('data/사진/08_주변_1.png', '주변사진'), ('data/사진/08_주변_2.png', '주변사진')])

                # 10번 위치 상세 정보
                show_location_info(st, "🔵 10번 위치", """
                    **방이동 / 경위도좌표 X,Y (37.51299316, 127.1161285)**
                    - 도로는 **나름 깔끔하고 잘 관리**되어 있지만, 차량 접근 시간이 오래 걸릴 것 같음
                    - **길에 주차구역이 종종 있어**, 여러 차량이 지나갈 경우 통과에 오래 걸림
                    - **오래된 건물과 신축빌라가 섞여 있는 지역**
                    """, [('data/사진/10_좌표.png', '좌표사진'), ('data/사진/10_주변_1.png', '주변사진'), ('data/사진/10_주변_2.png', '주변사진')])

                # 12번 위치 상세 정보
                show_location_info(st, "🟡 12번 위치", """
                    **가락본동 / 경위도좌표 X,Y (37.496917, 127.120417)**
                    - 주변에 **식당, 술집이 많음**
                    - 주택가에는 주차된 차가 있을 경우 **승용차가 겨우 지나가는 폭**
                    - 큰 도로가 옆에 있어 진입은 어렵지 않지만, **노후주택이 많아 화재 시 피해가 클 것**
                    - **골목길이 화재 발생지역과 가까워**, 차량이 한 대만 주정차되어 있어도 **소방차량의 진입이 어려움**
                    - **노후 건물에 교회와 노인복지센터가 위치**하여, 화재사고 시 대량의 인명피해가 예상되는 구간
                    - **비상소화장치의 설치가 필요한 구간**
                    """, [('data/사진/12_좌표.png', '좌표사진'), ('data/사진/12_주변.png', '주변사진')])

                # 14번 위치 상세 정보
                show_location_info(st, "🟢 14번 위치", """
                    **마천1동 / 경위도좌표 X,Y (37.492321,127.154682)**
                    - **좁은 골목에 주택이 촘촘히 위치한 지역**
                    - 불법주정차 차량이 많아 **사람도 겨우 지나갈 수 있는 길이 많음**
                    - **비상소화장치가 설치되면 좋을 것**
                    """, [('data/사진/14_좌표.png', '좌표사진'), ('data/사진/14_주변_1.png', '주변사진'), ('data/사진/14_주변_2.png', '주변사진')])

                # 16번 위치 상세 정보
                show_location_info(st, "🔵 16번 위치", """
                    **거여1동 / 경위도좌표 X, Y (37.493358, 127.142836)**
                    - **낡은 주택과 좁은 골목**으로 이루어진 지역
                    - 큰 도로가 바로 옆이긴 하지만, 차들이 얽히면 **사람이 지나가기 힘듦**
                    - **소방차 진입 시간을 고려**하여 비상소화장치를 설치하면 좋을 것
                    - 화재 발생건수가 많았던 만큼, **빠른 접근이 어려운 곳**에 비상소화장치 설치 필요
                    """, [('data/사진/16_좌표.png', '좌표사진'), ('data/사진/16_주변_1.png', '주변사진'), ('data/사진/16_주변_2.png', '주변사진')])

                # 18번 위치 상세 정보
                show_location_info(st, "🟢 18번 위치", """
                    **오금동 / 경위도좌표X, Y (37.503962, 127.140793)**
                    - 주변 길이 모두 **좁고 주차된 차들이 많음**
                    - **송파소방서가 가까움**에도 불구하고, 원활한 차량 통행이 어려움
                    - **노후/단독주택이 많은 지역**이지만, 최근 **신축 빌라가 지어지는 곳**도 있음
                    - 특히 **문정로25길 쪽**에 협소한 폭의 도로와 노후주택이 집중되어 있어, 이곳에 비상소화장치 설치 고려 필요
                    """, [('data/사진/18_좌표.png', '좌표사진'), ('data/사진/18_주변_1.png', '주변사진'), ('data/사진/18_주변_2.png', '주변사진')])
               
    # 송파구 소방 인프라 분석 섹션
    with st.container(border=True, height=900):
        # 부제목
        st.markdown('<h4>송파구 소방 인프라 분석</h4>', unsafe_allow_html=True)
        # 4개의 탭 생성
        tab1, tab2, tab3, tab4 = st.tabs(["비상소화장치", "화재 건수", "인구 및 노년 인구", " 주택 현황"])
         
        with tab1: # 탭 1 - 송파구 비상 소화장치 위치 시각화      
            st.markdown('**현재 송파구 비상소화장치 위치**')
            create_fire_equip_map(data)  # fire_equip_df는 당신의 데이터프레임 변수명입니다.

        with tab2: # 탭 2 - 송파구 화재 건수 분석
            st.markdown('**송파구 화재 건수 분석**')            
            # 선택 메뉴 생성
            select = st.radio("선택", ["동별 화재발생 건수", "연도별 화재발생 건수"],horizontal=True, label_visibility="collapsed")
            # 연도별 화재발생 건수를 선택한 경우 - 2020~2023 총 화재 건수 시각화
            if select == '연도별 화재발생 건수':
                new_data = pd.DataFrame({'시점': [2023],'화재건수': [382]})
                df_grouped = df.groupby(['시점'])['화재건수'].sum().reset_index()
                visualize_fire_incidents(df, new_data, '송파구 2020~2023 총 화재건수')

            # 연도별 화재발생 건수를 선택한 경우 - 선택된 연도에 대한 화재건수 시각화
            else:
                # 연도 선택 위젯
                selected_year = st.selectbox('연도 선택', options=sorted(df['시점'].unique(), reverse=True))

                # 선택된 연도에 대한 화재건수 시각화 함수 호출
                visualize_fire_counts_by_selected_year(df, selected_year)
            
        with tab3: # 탭 3 - 송파구 노년 인구 분석
            st.markdown('**송파구 노년 인구 분석**')   

            # 노년 인구 분석에 대한 선택 옵션 제공
            select = st.radio("선택", ["노년인구", "동별 노년인구", "노년인구 비율", "거주인구"],horizontal=True, label_visibility="collapsed")

            # 거주인구를 선택한 경우 - 선택한 연도에 따른 거주인구 시각화
            if select == '거주인구':

                # 연도 선택 위젯
                selected_year = st.selectbox('연도 선택', options=sorted(df_O['시점'].unique(), reverse=True))

                # 선택된 연도에 대한 거주인구 시각화 함수 호출
                visualize_population_by_selected_year(df_O, selected_year)
                

            # 노년인구를 선택한 경우 - 2020~2023 송파구 노년인구수 시각화
            elif select == '노년인구':

                시점 = df_P['시점'].tolist()
                노년인구 = df_P['노년 전체 인구'].tolist()
                시점.reverse()

                colors = ['tomato', 'crimson', 'darkred', 'lightsalmon']
                fig = go.Figure()
                fig.add_trace(go.Bar(x=시점, y=노년인구, marker_color=colors, width=0.4, text=df_P['노년 전체 인구']))
                fig.update_layout(title_text='송파구 2022~2023년도 노년인구 수', yaxis_title='노년인구', xaxis_title='시점')
                st.plotly_chart(fig, use_container_width=True)

            # 동별 노년인구를 선택한 경우 - 선택된 연도에 대한 거주 인구 시각화
            elif select == '동별 노년인구':                    
                visualize_elderly_population_by_year(df_O)
                
            # 노년인구 비율을 선택한 경우 - 선택한 연도에 따라 노년인구 비율 시각화
            else:
                # 연도 선택 위젯
                selected_year = st.selectbox('연도 선택', options=sorted(df_O['시점'].unique(), reverse=True))

                # 선택된 연도에 대한 노년인구 비율 시각화 함수 호출
                visualize_elderly_population_ratio_by_selected_year(df_O, selected_year)
                

        with tab4: # 탭 4 - 송파구 주택현황 분석
            st.markdown('**송파구 주택현황 분석**') 

            # 선택 옵션 제공
            select_1 = st.radio("선택", ["동별 주택유형 분포", "동별 주택수"], horizontal=True, label_visibility="collapsed")
            
            # 동별 주택유형 분포를 선택한 경우 - 선택한 동에 따라 주택유형 분포 시각화
            if select_1 == "동별 주택유형 분포":

                # 동 선택 위젯
                selected_dong = st.selectbox('동 선택', options=sorted(df_H['동'].unique()))

                # 선택된 동에 대한 주택 유형별 분포 시각화 함수 호출
                visualize_housing_type_distribution_by_selected_dong(df_H, selected_dong)
                
            # 동별 주택수를 선택한 경우 - 동별 주택수 가로 막대 그래프 시각화
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
