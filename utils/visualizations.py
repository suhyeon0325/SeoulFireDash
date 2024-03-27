import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 
from plotly.subplots import make_subplots

# 1. 서울시 화재사고 현황 페이지 - 각 탭, 범위별 추세 시각화
def visualize_trend_by_district_with_tabs(df):
    """
    Visualizes the trend of various fire-related statistics across districts in Seoul
    with the option to view the entire city or compare specific districts. The trends
    are displayed through interactive tabs, each representing a different statistic.

    Args:
        df (pd.DataFrame): A DataFrame containing fire incident data, structured with
                           columns for each year and statistic, as well as a district column.

    Returns:
        None: This function primarily modifies the Streamlit UI by adding charts and
              interactive elements, and does not have a return value.

    Raises:
        ValueError: If no districts are selected when the option to compare specific
                    districts is chosen, a ValueError is raised to prompt the user for selection.
    """

    columns = ['화재건수', '사망', '부상', '인명피해 계', '부동산피해(천원)', '동산피해(천원)', '재산피해(천원)', '재산피해/건당(천원)']
    years = [f'{year}' for year in range(18, 24)]  # 연도 리스트 (2018-2023)

    selected_districts = []

    with st.container(border=True, height=650):
        option = st.radio("**화재 추세 분석**", ("서울시 전체", "각 구별로 비교하기"), horizontal=True)

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
                return
                
            df = df[df['자치구'].isin(selected_districts)]

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
                    if option == "서울시 전체" and column == "화재건수":
                        title = f'서울시 전체 {column} 추세 (2018-2023)'
                        fig = px.line(new_df, x='연도', y=column, color='자치구', title=title)
                        fig.update_layout(height=350)
                    
                        
                        # 화재건수를 선택했을 때만 열 2개로 나눠서 그래프와 이미지 표시
                        col1, col2 = st.columns([4,5])
                        with col1:
                            st.plotly_chart(fig, use_container_width=True)
                        with col2:
                            st.markdown('**2024년 서울시 월별 화재건수 예측**')
                            st.image('data/사진/2024_서울시_월별화재건수_예측.png')
                    else:
                        # 화재건수가 아닌 다른 탭이나 "각 구별로 비교하기" 선택 시 단독으로 그래프 표시
                        title = f'{("서울시 전체 " if option == "서울시 전체" else "")}{column} 추세 (2018-2023)'
                        fig = px.line(new_df, x='연도', y=column, color='자치구', title=title)
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)


# 1. 서울시 화재사고 현황 페이지 - 장소유형별 트리맵 시각화 함수
def display_treemap(df):
    """
    Displays a treemap visualization of fire incidents by location type within a specific
    district ('자치구') and neighborhood ('동') in Seoul. The visualization allows users
    to select a district and a neighborhood from dropdown menus, and it aggregates
    fire incident data by location type within the selected area.

    Args:
        df (pd.DataFrame): A DataFrame containing fire incident data, with columns
                           for district ('자치구'), neighborhood ('동'), and various
                           location types that represent the place of fire incidents.

    """

    col1, col2 = st.columns(2)

    with col1:
        # '자치구' 선택을 위한 스트림릿 셀렉트박스 구현
        selected_gu = st.selectbox('자치구 선택', options=df['자치구'].unique(), key='자치구_select')
        # 선택된 '자치구'에 해당하는 데이터만 필터링
        df_filtered_by_gu = df[df['자치구'] == selected_gu]

    with col2:
        # '동' 선택을 위한 스트림릿 셀렉트박스 구현, 선택된 '자치구'에 해당하는 '동'만을 옵션으로 제공
        selected_dong = st.selectbox('동 선택', options=df_filtered_by_gu['동'].unique(), key='동_select_dong')
        # 선택된 '동'에 해당하는 데이터만 최종 필터링
        df_filtered_by_dong = df_filtered_by_gu[df_filtered_by_gu['동'] == selected_dong]

    # 화재 발생 장소 유형별로 화재 발생 건수 집계
    df_agg = df_filtered_by_dong.melt(id_vars=['자치구', '동'], value_vars=df.columns[3:], var_name='장소 유형', value_name='건수')
    df_agg = df_agg.groupby(['자치구', '동', '장소 유형']).sum().reset_index()

    # 건수가 0 이상인 데이터만 필터링
    df_agg = df_agg[df_agg['건수'] > 0]

    # 사용자 지정 색상 리스트
    colors = ['#F25E6B', '#F2C744', '#A1BF34', '#EEDFE2', '#FCE77C', '#E2D0F8', '#DCE2F0', '#F2EFBB', '#D5D971', '#6779A1', '#9B7776','#1BBFBF', '#D94B2B', '#D98F89', '#FFDEDC', '#ACC7B4']

    # 트리맵 생성
    fig = px.treemap(df_agg, path=['자치구', '동', '장소 유형'], values='건수',
                     color='장소 유형',
                     hover_data=['건수'],
                     color_discrete_sequence=colors)

    # 차트 제목 및 스타일 설정
    fig.update_layout(title='동별 화재 장소유형 트리맵', font=dict(family="Arial, sans-serif", size=14, color="black"))

    # Streamlit에 트리맵 표시
    st.plotly_chart(fig, use_container_width=True)

# 1. 서울시 화재사고 현황 페이지 - 자치구별 장소유형 막대그래프 시각화 함수
def visualize_facilities(df_selected):
    """
    Generates a bar chart showing the total counts for different facility types.
    The bar chart highlights the aggregate counts of facilities by type within a given area, 
    using a distinct color for each facility type.

    Args:
        df_selected (pd.DataFrame): DataFrame with counts of different facility types. 
                                    The first two columns should be '자치구' and '동', 
                                    followed by columns for each facility type.

    Returns:
        None: Displays a bar chart in the Streamlit application. 

    """

    fig = go.Figure()

    colors = ['#F25E6B', '#F2C744', '#A1BF34', '#EEDFE2', '#FCE77C', '#E2D0F8', '#DCE2F0', '#F2EFBB', '#D5D971', '#6779A1', '#9B7776','#1BBFBF', '#D94B2B', '#D98F89', '#FFDEDC', '#ACC7B4']
    facility_types = ['단독주택', '공동주택', '기타주택', '학교', '일반업무', '판매시설', '숙박시설', '종교시설', '의료시설', '공장 및 창고', '작업장', '위락오락시설', '음식점', '일상서비스시설', '기타']
    color_map = dict(zip(facility_types, colors))

    for column in df_selected.columns[2:]:  # '자치구'와 '동' 컬럼을 제외한 나머지 컬럼에 대해 반복
        total = df_selected[column].sum()  # 해당 시설 유형의 총합
        # 시설 유형별로 지정된 색상 사용, 레전드 표시하지 않음
        fig.add_trace(go.Bar(x=[column], y=[total], marker_color=color_map.get(column), showlegend=False))

    fig.update_layout(title="시설 유형별 총계", xaxis_title="시설 유형", yaxis_title="총계")
    st.plotly_chart(fig, use_container_width=True)

# 2. 화재사고 취약지역 페이지 - 전체보기탭: 가로 막대그래프 시각화 함수
@st.cache_data
def visualize_vertical_bar_chart(df, selected_column, title, color_scale='Reds'):
    """
    Visualizes a vertical bar chart in Streamlit, displaying data from a selected column across districts.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to visualize.
        selected_column (str): The name of the column to visualize.
        title (str): The title of the graph.
        color_scale (str): The color scale for the bars, default is 'Reds'.

    Returns:
        None: The function directly displays the vertical bar chart in the Streamlit app.

    Notes:
        The color scale can be customized by the user. Default orientation is vertical ('v').
        The function is decorated with @st.cache_data to cache the data and improve performance.
    """

    df_sorted = df.sort_values(by=selected_column, ascending=False)
    
    fig = px.bar(df_sorted, x='자치구', y=selected_column,
                 labels={'자치구': '자치구', selected_column: selected_column},
                 title=title, orientation='v',  # 세로 막대 그래프를 위해 orientation을 'v'로 설정
                 color=selected_column, color_continuous_scale=px.colors.sequential.__dict__[color_scale])
    
    # x축 레이블이 더 넓게 표시되도록 조정 및 글꼴 크기 조정, 레전드 위치 조정
    fig.update_layout(plot_bgcolor='rgba(240, 240, 240, 0)',
                      margin=dict(l=100, b=150),  # 좌측과 바텀 마진을 늘려 레전드 및 레이블에 공간을 만듭니다.
                      width=700, height=500
                      )
    fig.update_xaxes(tickmode='array', tickvals=df_sorted['자치구'], tickangle=-45, tickfont=dict(size=10))  # x축 레이블 각도 조정
    
    st.plotly_chart(fig, use_container_width=True)

# 2. 화재사고 취약지역 페이지 - 상/하위 5개만 보기탭: 가로 막대그래프 시각화 함수
def visualize_top_districts_with_seoul_average(df, column_name='비상소화장치 설치개수'):
    """
    Visualizes the top 5 districts and the Seoul city average for a selected category.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be analyzed.
        column_name (str): The name of the column to analyze. Defaults to '비상소화장치 설치개수'. For this specific column,
                           the function displays the bottom 5 districts instead of the top 5.

    Returns:
        None: The function directly displays the bar chart in the Streamlit app, without returning any value.

    """

    # 분석 카테고리 선택
    selected_column = st.selectbox('분석 카테고리 선택', options=df.columns[1:], index=0, key='_selected_data_4')

    # 서울시 평균 계산
    seoul_average = df[selected_column].mean()
    # 서울시 평균 행 추가
    average_row = pd.DataFrame({'자치구': ['서울시 평균'], selected_column: [seoul_average]})
    
    if selected_column == column_name:
        # '비상소화장치 설치개수'의 경우 하위 5개 구 시각화
        districts = df.nsmallest(5, selected_column)
        title = f'{selected_column} 분석: 하위 5개구 및 서울시 평균'
    else:
        # 나머지 경우 상위 5개 구 시각화
        districts = df.nlargest(5, selected_column)
        title = f'{selected_column} 분석: 상위 5개구 및 서울시 평균'
    
    # 시각화할 데이터 프레임 생성
    visual_df = pd.concat([districts, average_row]).reset_index(drop=True)
    
    # 시각화
    fig = px.bar(visual_df, x='자치구', y=selected_column, 
                labels={'자치구': '자치구', selected_column: selected_column},
                title=title, orientation='v', 
                color=selected_column,
                color_continuous_scale=px.colors.sequential.Reds)  

    fig.update_layout(plot_bgcolor='rgba(240, 240, 240, 0)')
    fig.update_xaxes(tickmode='array', tickvals=visual_df['자치구'])

    # 스트림릿에 그래프 표시
    st.plotly_chart(fig, use_container_width=True)



# 4. 비상소화장치 위치 제안 페이지 - 화재건수탭: 동별 화재발생 건수
@st.cache_data
def visualize_fire_counts_by_selected_year(df, selected_year):
    """
    Visualizes fire incident counts by district for a selected year, using a horizontal bar chart.

    Args:
        df (pd.DataFrame): The DataFrame containing fire incident data, including a '시점' column for the year,
                           a '동' column for the district, and a '화재건수' column for the number of fire incidents.
        selected_year (int): The year for which the user wants to visualize fire incident counts.

    Returns:
        None: The function directly displays the horizontal bar chart in the Streamlit app, without returning any value.

    Notes:
        The function is decorated with @st.cache_data to improve performance by caching the data.
    """
    df_year = df[df['시점'] == selected_year].sort_values(by='화재건수', ascending=True)
    fig = px.bar(df_year, x='화재건수', y='동', text_auto=True,
                 title=f"{selected_year}년 송파구 화재건수",
                 color='화재건수',
                 color_continuous_scale=px.colors.sequential.OrRd)
    fig.update_traces(textfont_size=10, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_yaxes(tickmode='array', tickvals=df_year['동'].unique())
    fig.update_layout(height=600)

    st.plotly_chart(fig, use_container_width=True)

# 4. 비상소화장치 위치 제안 페이지 - 화재건수탭: 연도별 화재발생 건수
@st.cache_data
def visualize_fire_incidents(df, new_data, title, xaxis_title='시점', yaxis_title='화재건수', colors=['#fc8d59', '#fdcc8a', '#e34a33', '#b30000']):
    """
    Visualizes fire incident data with the option to include new data, displaying the total fire incidents over time. 

    Args:
        df (pd.DataFrame): The original dataset containing fire incidents. 
                           It must include columns for time period ('시점') and number of incidents ('화재건수').
        new_data (pd.DataFrame): A DataFrame containing new fire incident data to be added to the original dataset. 
                                 It must follow the same format as 'df'.
        title (str): The title of the visualization.
        xaxis_title (str, optional): The title of the x-axis. Defaults to '시점'.
        yaxis_title (str, optional): The title of the y-axis. Defaults to '화재건수'.
        colors (list of str, optional): A list of strings representing colors for the bar chart. 
                                        Defaults to ['#fc8d59', '#fdcc8a', '#e34a33', '#b30000'].

    """

    # 기존 데이터에서 '시점'에 따른 '화재건수' 집계
    df_grouped = df.groupby(['시점'])['화재건수'].sum().reset_index()
    # 새로운 데이터 추가
    df_grouped_updated = pd.concat([df_grouped, new_data]).reset_index(drop=True)
    # 시각화
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_grouped_updated['시점'], 
        y=df_grouped_updated['화재건수'], 
        width=0.4, 
        marker_color=colors, 
        text=df_grouped_updated['화재건수']
    ))
    fig.update_layout(
        title_text=title,
        xaxis_type='category',
        yaxis_title=yaxis_title,
        xaxis_title=xaxis_title
    )
    st.plotly_chart(fig, use_container_width=True)

# 4. 비상소화장치 위치 제안 페이지 - 노년인구탭: 1 거주인구 그래프
@st.cache_data
# 송파구 연도별 거주 인구
def visualize_population_by_selected_year(df, selected_year):
    df_year = df[df['시점'] == selected_year].sort_values(by='전체인구', ascending=True)
    fig = px.bar(df_year, x='전체인구', y='동', text_auto=True,
                 title=f"{selected_year}년 송파구 거주인구",
                 color='전체인구',
                 color_continuous_scale=px.colors.sequential.OrRd)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_yaxes(tickmode='array', tickvals=df_year['동'].unique())
    fig.update_layout(height=600)
    
    st.plotly_chart(fig, use_container_width=True)

# 4. 비상소화장치 위치 제안 페이지 - 노년인구탭: 3 동별 노년인구
def visualize_elderly_population_by_year(df, time_column='시점'):
    """
    Visualizes the population of individuals aged 65 and above for each year.

    Args:
        df (pandas.DataFrame): A DataFrame containing at least the columns specified by `time_column`, 
            '65세이상 인구' (population aged 65 and above), and '동' (districts).
        time_column (str, optional): The name of the column in `df` that represents the time aspect. 
            Defaults to '시점'.

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

# 4. 비상소화장치 위치 제안 페이지 - 노년인구탭: 4 노년인구 비율
@st.cache_data
def visualize_elderly_population_ratio_by_selected_year(df, selected_year):
    """
    Visualizes the ratio of the population aged 65 and above in the selected year across different districts.

    This function computes the ratio of the elderly population to the total population for each district in 
    the specified year. It then generates and displays a bar chart visualizing these ratios.

    Args:
        df (pandas.DataFrame): A DataFrame containing the columns '시점' (year), '65세이상 인구' (population aged 65 and above),
            '전체인구' (total population), and '동' (districts).
        selected_year (int): The year for which the elderly population ratio should be visualized.

    """
    df_year = df[df['시점'] == selected_year].copy()
    df_year.loc[:, '65세이상 인구 비율'] = (df_year['65세이상 인구'] / df_year['전체인구']) * 100
    df_year.sort_values(by='65세이상 인구 비율', ascending=True, inplace=True)

    fig = px.bar(df_year, x='65세이상 인구 비율', y='동', text_auto=True,
                 title=f"{selected_year}년 송파구 노년인구 비율",
                 color='65세이상 인구 비율',
                 color_continuous_scale=px.colors.sequential.OrRd)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_yaxes(tickmode='array', tickvals=df_year['동'].unique())
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

# 4. 비상소화장치 위치 제안 페이지 - 주택현황탭: 1 동별 주택유형 분포
def visualize_housing_type_distribution_by_selected_dong(df, selected_dong):
    """
    Visualizes the distribution of different housing types in a selected district using both bar and pie charts.

    This function filters the dataset for the specified district, removes the 'Total' column, and then melts the DataFrame 
    to have a long format suitable for visualization. It generates a subplot containing a bar chart and a pie chart to 
    show the distribution of housing types within the selected district.

    Args:
        df (pandas.DataFrame): A DataFrame that includes '동' (district), housing types as columns, and their corresponding 
            counts. It should also contain a '시점' column indicating the time point of data collection.
        selected_dong (str): The name of the district for which the housing type distribution is to be visualized.

    """

    # 선택된 동에 해당하는 데이터 필터링
    df_dong = df[df['동'] == selected_dong]
    
    # '소계' 항목 제거
    df_dong = df_dong.drop(columns=['소계'])
    
    # 데이터를 '시점', '동'을 기준으로 melt 실행
    df_melted = df_dong.melt(id_vars=['시점', '동'], var_name='주택 유형', value_name='수량')
    
    # 막대 그래프와 파이 차트를 포함한 서브플롯 생성
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}]], subplot_titles=("막대 그래프", "파이 차트"))

    # 왼쪽 열에 막대 그래프 추가
    fig.add_trace(go.Bar(x=df_melted['주택 유형'], y=df_melted['수량'], text=df_melted['수량'], textposition='auto',
                        marker=dict(color=df_melted['수량'], colorscale='Reds'), name="주택 유형별 분포"), row=1, col=1)

    # 오른쪽 열에 파이 차트 추가, 색상 및 레전드 명시적 지정
    fig.add_trace(go.Pie(labels=df_melted['주택 유형'], values=df_melted['수량'],
                        pull=[0.1 if i == df_melted['수량'].idxmax() else 0 for i in range(len(df_melted))],
                        marker=dict(colors=px.colors.qualitative.Plotly), name=""),
                row=1, col=2)

    # 레전드 항목을 제거하고 싶은 경우, 다음과 같이 설정
    fig.update_traces(showlegend=False)

    # 서브플롯 레이아웃 업데이트
    fig.update_layout(title_text=f"{selected_dong} 주택 유형별 분포")

    st.plotly_chart(fig, use_container_width=True)