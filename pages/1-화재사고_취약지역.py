# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium
from folium.features import DivIcon
from utils.data_loader import load_data
from utils.ui_helpers import setup_sidebar_links

st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_icon='⚠️')

df = load_data("data/total_rank.csv", encoding='cp949')
gdf = gpd.read_file("data/boundary/boundary.geojson", encoding="utf-8")
setup_sidebar_links()

columns_to_exclude = ["비상소화장치 설치개수 점수", "서울시 주거 시설 중 주택 비율 점수", "인구밀도(명/km^2) 점수", 
                      "노후 주택 수 점수", "소방관 1명당 담당인구 점수", "화재발생건수 점수", "안전센터 1개소당 담당인구 점수", 
                      "출동소요시간 점수", "순위", "전체 점수", "고령자 수 점수"]

df_09 = df[[col for col in df.columns if col not in columns_to_exclude]]
df_09 = df_09.rename(columns={'서울시 주거 시설 중 주택 비율': '주택 중 아파트를 제외한 건물 비율'})
df_3 = df[['자치구', '순위', '전체 점수']].sort_values(by='순위', ascending=True)
merged_data = gdf.merge(df, left_on='구', right_on='자치구')

@st.cache_data
def visualize_vertical_bar_chart(df, selected_column, title, color_scale='Reds'):
    df_sorted = df.sort_values(by=selected_column, ascending=False)
    fig = px.bar(df_sorted, x='자치구', y=selected_column,
                 labels={'자치구': '자치구', selected_column: selected_column},
                 title=title, orientation='v',
                 color=selected_column, color_continuous_scale=px.colors.sequential.__dict__[color_scale])
    fig.update_layout(plot_bgcolor='rgba(240, 240, 240, 0)', margin=dict(l=100, b=150), width=700, height=500)
    fig.update_xaxes(tickmode='array', tickvals=df_sorted['자치구'], tickangle=-45, tickfont=dict(size=10))
    st.plotly_chart(fig, use_container_width=True)

def visualize_top_districts_with_seoul_average(df, column_name='비상소화장치 설치개수'):
    selected_column = st.selectbox('분석 카테고리 선택', options=df.columns[1:], index=0, key='_selected_data_4')
    seoul_average = df[selected_column].mean()
    average_row = pd.DataFrame({'자치구': ['서울시 평균'], selected_column: [seoul_average]})
    
    if selected_column == column_name:
        districts = df.nsmallest(5, selected_column)
        title = f'{selected_column} 분석: 하위 5개구 및 서울시 평균'
    else:
        districts = df.nlargest(5, selected_column)
        title = f'{selected_column} 분석: 상위 5개구 및 서울시 평균'
    
    visual_df = pd.concat([districts, average_row]).reset_index(drop=True)
    fig = px.bar(visual_df, x='자치구', y=selected_column,
                 labels={'자치구': '자치구', selected_column: selected_column},
                 title=title, orientation='v',
                 color=selected_column,
                 color_continuous_scale=px.colors.sequential.Reds)
    fig.update_layout(plot_bgcolor='rgba(240, 240, 240, 0)')
    fig.update_xaxes(tickmode='array', tickvals=visual_df['자치구'])
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data
def create_and_show_map(_data, columns, key_on, fill_color='YlOrRd'):
    seoul_map = folium.Map(location=[37.5642135, 127.0016985], zoom_start=11)
    choropleth = folium.Choropleth(
        geo_data=_data,
        name='choropleth',
        data=_data,
        columns=columns,
        key_on=key_on,
        fill_color=fill_color,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='서울시 취약 분야별 점수 합계(높은 값 일수록 취약)',
        bins=25,
        show_legend=False
    ).add_to(seoul_map)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=[
            '자치구', '전체 점수', '순위', '비상소화장치 설치개수 점수', '서울시 주거 시설 중 주택 비율 점수', '인구밀도(명/km^2) 점수',
            '노후 주택 수 점수', '소방관 1명당 담당인구 점수', '화재발생건수 점수', '안전센터 1개소당 담당인구 점수',
            '출동소요시간 점수', '고령자 수 점수'
        ],
        aliases=[
            '자치구', '전체 점수', '비상소화장치 설치개수 점수', '순위', '서울시 주거 시설 중 주택 비율 점수', '인구밀도(명/km^2) 점수',
            '노후 주택 수 점수', '소방관 1명당 담당인구 점수', '화재발생건수 점수', '안전센터 1개소당 담당인구 점수',
            '출동소요시간 점수', '고령자 수 점수'
        ],
        labels=True,
        sticky=True,
        style="""
            background-color: #F0EFEF;
            color: #333333;
            font-family: Arial;
            font-size: 13px;
            font-weight: bold;
            border: 2px solid black;
            border-radius: 5px;
            box-shadow: 3px;
        """))

    for _, row in _data.iterrows():
        centroid = row['geometry'].centroid
        text = row['자치구']
        folium.Marker(
            [centroid.y, centroid.x],
            icon=DivIcon(
                icon_anchor=(0,0),
                html=f'<div style="font-size: 8pt; font-weight: bold; background: rgba(245, 245, 245, 0.6); padding: 4px 6px; border-radius: 5px; text-align: center; color: #1C1C1C; white-space: nowrap; min-width: 50px;">{text}</div>',
            )
        ).add_to(seoul_map)

    return seoul_map._repr_html_()

def main():
    st.header('화재사고 취약지역 분석', help ='이 페이지에서는 서울시 내 주택화재 취약지를 다양한 분석 지표를 통해 탐색해보고, 지역별로 취약점수를 비교해 볼 수 있습니다.', divider="gray")

    with st.container(border=True, height=700):
        st.markdown('<h4>서울시 주택화재 취약지역 분석</h4>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(['전체 보기', '상/하위 5개구만 보기', '테이블로 보기'])

        with tab1:
            selected_column = st.selectbox('분석 카테고리 선택', options=df_09.columns[1:], index=0, key='_selected_data_1')
            visualize_vertical_bar_chart(df_09, selected_column, title=f"서울시 자치구별 {selected_column} 분석")

        with tab2:
            visualize_top_districts_with_seoul_average(df_09)

        with tab3:
            st.caption('테이블 상단의 열을 클릭하면, 해당 열을 기준으로 데이터를 오름차순 혹은 내림차순으로 정렬할 수 있습니다.')
            st.dataframe(df, height=500, use_container_width=True)

    col1, col2 = st.columns([7, 3])
    with col1:
        with st.container(border=True, height=700): 
            st.markdown('<h4>서울시 구별 취약지역 점수 지도</h4>', unsafe_allow_html=True) 
            with st.popover("💡 **점수 기준**"):
                st.markdown("""
                    각 카테고리별로 지역의 취약성을 분석하여 순위를 매긴 뒤,
                    모든 카테고리의 순위를 합산하여 최종 점수를 산출했습니다.
                    :orange[**점수가 높을수록 소방 취약지역입니다.**]
                        
                    **카테고리**: 비상소화장치 설치개수, 주택 중 아파트를 제외한 건물 비율,	인구밀도(명/km^2),	노후 주택 수, 소방관 1명당 담당인구, 화재발생건수, 안전센터 1개소당 담당인구, 출동소요시간, 고령자 수
                """)
            html_string = create_and_show_map(_data=merged_data, columns=['자치구', '전체 점수'], key_on='feature.properties.자치구')
            st.components.v1.html(html_string, height=570)

    with col2:
        with st.container(border=True, height=700): 
            st.markdown("**취약점수 순위**")
            st.dataframe(df_3, height=600, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
