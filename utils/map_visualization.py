import folium
import streamlit.components.v1 as components

def create_and_show_map(data, columns, key_on, fill_color='YlOrRd'):
    """
    GeoDataFrame의 지리 정보를 사용하여 서울시 자치구별 지도에 Choropleth 레이어를 추가하고 시각화하는 함수.

    매개변수:
    - data: 지도에 표시할 데이터와 지리 정보를 포함한 GeoDataFrame. 'geometry' 열에 지리 정보가 포함되어 있어야 함.
    - columns: GeoDataFrame에서 'key_on'에 해당하는 열과 시각화할 값의 열 이름을 담은 리스트.
    - key_on: GeoJSON 내의 특성과 매핑되는 GeoDataFrame의 열 이름. 예: 'feature.properties.자치구'
    - fill_color: Choropleth 레이어의 색상 팔레트. 기본값은 'YlGnBu'.

    반환값:
    - 생성된 Folium 지도의 HTML 표현 문자열.
    """

    # 서울시 중심부의 위도와 경도로 지도 초기화
    seoul_map = folium.Map(location=[37.5642135, 127.0016985], zoom_start=11)
    
    # Choropleth 레이어 추가
    choropleth = folium.Choropleth(
        geo_data=data,
        name='choropleth',
        data=data,
        columns=columns,
        key_on=key_on,
        fill_color=fill_color,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='서울시 취약 분야별 점수 합계(높은 값 일수록 취약)',
        bins=25,
        show_legend=False
    ).add_to(seoul_map)

    # 툴팁 추가
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['자치구', '전체 점수'],
                                        aliases=['자치구: ', '전체 점수:'],  # HTML 스타일 적용을 위해 aliases 사용 안 함
                                        labels=False,
                                        sticky=True,
                                        style="""
                                            background-color: #F0EFEF;
                                            color: #333333;
                                            font-family: Arial;
                                            font-size: 14px;
                                            font-weight: bold;
                                            border: 2px solid black;
                                            border-radius: 3px;
                                            box-shadow: 3px;
                                        """                                  
    ))

    # HTML로 변환 후 반환
    return seoul_map._repr_html_()
