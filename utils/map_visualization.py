import folium
import streamlit.components.v1 as components
import geopandas as gpd
from shapely import wkt
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import streamlit as st
from folium import plugins
import branca
from folium import IFrame


# 화재사고 취약 페이지 - 지도 시각화
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
        folium.features.GeoJsonTooltip(fields = [
                                                    '자치구', '전체 점수', '순위','비상소화장치 설치개수 점수', '서울시 주거 시설 중 주택 비율 점수', '인구밀도(명/km^2) 점수', 
                                                    '노후 주택 수 점수', '소방관 1명당 담당인구 점수', '화재발생건수 점수', '안전센터 1개소당 담당인구 점수', 
                                                    '출동소요시간 점수',  '고령자 수 점수'
                                                ],
                                        aliases = [
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
                                        """                                  
    ))

    # HTML로 변환 후 반환
    return seoul_map._repr_html_()


# 서울시 비상소화장치 시각화
def display_folium_map_with_clusters(gdf):
    """
    GeoDataFrame의 포인트들을 클러스터링하여 Folium 지도에 표시하고, 이를 스트림릿에서 보여주는 개선된 함수.
    
    :param gdf: GeoDataFrame, 포인트들의 좌표를 포함하는 `geometry` 열을 가져야 하며, '구'와 '동' 정보를 포함해야 함.
    """
    # 서울시 중심에 지도를 생성하고, CartoDB Positron 타일을 사용
    m = folium.Map(location=[37.5665, 126.9780], tiles='OpenStreetMap', zoom_start=11)
    
    # 클러스터 객체 생성
    marker_cluster = MarkerCluster().add_to(m)
    
    # GeoDataFrame 내의 각 지점에 대해 마커 추가
    for idx, row in gdf.iterrows():
        # 마커에 표시될 팝업 및 툴팁 생성
        tooltip = f"{row['구']}, {row['동']}"
        
        # 마커에 팝업과 툴팁 추가, 빨간색 아이콘 사용
        folium.Marker(
            location=[row['geometry'].y, row['geometry'].x],
            tooltip=tooltip,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(marker_cluster)
    
    # 스트림릿에서 지도 표시
    folium_static(m)


# 소방용수 함수 정의
def visualize_fire_water(grid, column_name='소방용수_수'):
    """
    소방용수 분포를 지도에 시각화하는 함수입니다.
    GeoPandas와 Folium 라이브러리를 사용하여 소방용수가 있는 위치를 지도 위에 표시합니다.
    이 때, 소방용수의 양에 따라 지도 상의 색상이 달라집니다.
    
    :param grid: 소방용수 분포 데이터가 담긴 DataFrame. 'geometry' 컬럼에는 WKT 포맷의 지리 정보가, 
                 column_name에 지정된 컬럼에는 소방용수의 양 정보가 있어야 합니다.
    :param column_name: 소방용수의 양을 나타내는 컬럼 이름. 기본값은 '소방용수_수'.
    """
    # geometry 열을 GeoPandas의 geometry로 변환
    grid['geometry'] = gpd.GeoSeries.from_wkt(grid['geometry'])
    gdf = gpd.GeoDataFrame(grid, geometry='geometry')
    gdf.crs = "EPSG:4326"

    # 지도 객체 생성 (서울시 중심 좌표로 설정)
    map_fw = folium.Map(location=[37.564, 126.997], zoom_start=11, tiles='OpenStreetMap')

    # 색상을 결정하는 함수. 여기서는 단순화를 위해 소방용수의 양에 따라 색상을 분류합니다.
    def color_scale(amount):
        """
        소방용수의 양에 따라 색상을 매핑하는 함수입니다. 소방용수의 양이 1부터 10까지는 각각 다른 색상을,
        10 이상, 20 이상, 30 이상에서도 각각 특정 색상을 할당합니다.
        """
        if amount == 30:
            return '#01579B' 
        elif amount == 20:
            return '#0277BD' 
        elif amount == 10:
            return '#0288D1' 
        elif amount in[8, 9]:
            return '#039BE5'
        elif amount in[6, 7]:
            return '#03A9F4'  
        elif amount == 5:
            return '#29B6F6'  
        elif amount == 4:
            return '#4FC3F7'  
        elif amount == 3:
            return '#81D4FA'  
        elif amount == 2:
            return '#B3E5FC'  
        elif amount == 1:
            return '#E1F5FE' 
        else:
            return '#808080' # 회색 (양이 0 또는 정의되지 않은 경우)


    # GeoPandas DataFrame을 이용하여 지도에 추가
    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': color_scale(feature['properties'][column_name]),
            'color': 'black',
            'weight': 0.1,
            'fillOpacity': 0.7,
        }
    ).add_to(map_fw)
    # 지도 표시 (스트림릿으로 변환시 st.write(m) 사용)
    folium_static(map_fw)

# 서울시 소방서 및 안전센터 시각화 함수
# 지도 생성 및 마커 추가 함수
def create_folium_map(df):
    m = folium.Map(location=[37.5642135, 127.0016985], zoom_start=11)
    colors = {
        '소방서': 'red',
        '안전센터': 'blue',
        '구조대': 'orange',
        '소방항공대': 'lightblue',
        '특수대응단': 'purple'
    }

    for index, row in df.iterrows():
        popup_content = f"<b>서센터명:</b> {row['서ㆍ센터명']}<br><b>유형구분명:</b> {row['유형구분명']}"
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color=colors[row['유형구분명']])
        ).add_to(m)

    return m

# 송파구 비상소화장치 시각화 함수
def create_fire_equip_map(fire_equip):
    map_songpa = folium.Map(location=[37.514543, 127.106597], zoom_start=13)

    colors = {
        '소방차진입곤란': 'red',
        '주거지역': 'blue',
        '시장지역': 'green',
        '영세민밀집': 'purple',
        '소방차진입불가': 'orange'
    }

    for index, row in fire_equip.iterrows():
        icon_color = colors.get(row['설치지역'], 'gray')
        popup_html = f"""
        <h4>소방 장비 정보</h4>
        <ul style="margin: 0; padding: 0;">
            <li>설치지역: {row['설치지역']}</li>
            <li>설치유형구분: {row['설치유형구분']}</li>
            <li>상세위치: {row['상세위치']}</li>
            <li>주소: {row['주소']}</li>
        </ul>
        """
        popup = folium.Popup(popup_html, max_width=250)
        folium.Marker(
            location=[row['경위도좌표Y'], row['경위도좌표X']],
            popup=popup,
            tooltip=row['주소'],
            icon=folium.Icon(color=icon_color)
        ).add_to(map_songpa)

    legend_html = '''
    <div style="position: fixed; 
         top: 10px; right: 10px; width: 180px; height: 120px; 
         background-color: white; border:2px solid rgba(0,0,0,0.2); 
         z-index:9999; font-size:11px; border-radius: 8px; 
         box-shadow: 3px 3px 5px rgba(0,0,0,0.3); padding: 8px;">
         <h4 style="text-align:center; font-size:14px; font-weight: bold; margin-top: 0;">설치지역별 마커 색상</h4>
         &nbsp; 소방차진입곤란: <i style="background:#D33D2A; border-radius: 50%; width: 12px; height: 12px; display: inline-block;"></i> 빨강<br>
         &nbsp; 소방차진입불가: <i style="background:#F0932F; border-radius: 50%; width: 12px; height: 12px; display: inline-block;"></i> 주황<br>
         &nbsp; 시장지역: <i style="background:#73A626; border-radius: 50%; width: 12px; height: 12px; display: inline-block;"></i> 초록<br>
         &nbsp; 주거지역: <i style="background:#3BACD9; border-radius: 50%; width: 12px; height: 12px; display: inline-block;"></i> 파랑<br>
         &nbsp; 영세민밀집: <i style="background:#BF4EAC; border-radius: 50%; width: 12px; height: 12px; display: inline-block;"></i> 보라<br>
    </div>
    '''

    map_songpa.get_root().html.add_child(folium.Element(legend_html))

    # 기존의 create_fire_equip_map 함수 끝부분에 다음 코드 추가
    map_songpa.save('map_with_legend.html')  # 지도를 HTML 파일로 저장

    # 스트림릿에서 지도를 표시하는 부분을 아래와 같이 변경
    with open('map_with_legend.html', 'r', encoding='utf-8') as f:
        map_html = f.read()

    components.html(map_html, height=600)  # 조절이 필요할 수 있음
    
    map_songpa.get_root().html.add_child(folium.Element(legend_html))
    map_songpa.save('map_with_legend.html') 

# 비상소화장치 위치 제안
def display_fire_extinguisher_map(center, locations, zoom_start=13):
    """
    비상 소화장치 위치와 관련 정보를 포함한 지도를 생성하고 표시하는 함수.
    
    :param center: 지도의 중심이 될 위치의 (위도, 경도)
    :param locations: 비상 소화장치의 위치, 각 위치는 (위도, 경도, 설명, 사진 URL)의 튜플로 구성됨
    :param zoom_start: 초기 지도 줌 레벨
    """

    m = folium.Map(location=center, zoom_start=13)

    for idx, (lat, lon, label, image_path) in enumerate(locations):
        # 마커에 표시할 번호를 포함한 HTML 문자열 생성
        icon_html = f"""<div style="font-family: Arial; font-size: 12px; color: blue;"><b>{idx+1}</b></div>"""
        
        # DivIcon을 사용하여 번호를 포함한 아이콘 생성
        icon = folium.DivIcon(html=icon_html)
        
        # DivIcon 아이콘을 사용하는 마커 추가
        folium.Marker([lat, lon], icon=icon).add_to(m)
        
        # 선택적으로, 팝업도 추가할 수 있습니다.
        folium.Marker(
            location=[lat, lon],
            popup=f'<b>{idx+1}. {label}</b></b><br>{lat},{lon}</b><br><img src="{image_path}" width="150" height="100">',
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(m)

    # Streamlit을 사용하여 지도 표시
    folium_static(m)

# 골든타임 초과 시각화 함수(팝업텍스트 생성, 색 생성, 시각화)
# 팝업 텍스트를 생성하는 함수 (HTML 스타일 적용)
def create_popup_html(row):
    return f'''
    <html>
        <head><style>
            .popup {{
                font-family: Arial, sans-serif;
                font-size: 12px;
                color: #333333;
            }}
            .title {{
                font-weight: bold;
                color: #0078A8;
                margin-bottom: 5px;
            }}
            .info {{
                margin-bottom: 2px;
            }}
        </style></head>
        <body>
            <div class="popup">
                <div class="title">화재 정보</div>
                <div class="info">사망수: {row['사망수']}, 부상자수: {row['부상자수']}</div>
                <div class="info">재산피해금액: {row['재산피해금액']}만원</div>
                <div class="info">출동소요시간: {row['출동소요시간']}초</div>
                <div class="info">화재진압시간: {row['화재진압시간']}초</div>
                <div class="info">위치: {row['시군구명']}, {row['읍면동명']}</div>
                <div class="info">계절: {row['계절']}, 시간대: {row['시간대']}</div>
                <div class="info">화재발생일시: {row['화재발생일시']}</div>
            </div>
        </body>
    </html>
    '''

# 계절별 색상을 결정하는 함수
def get_color(season):
    if season == '봄':
        return 'green'
    elif season == '여름':
        return 'red'
    elif season == '가을':
        return 'orange'
    elif season == '겨울':
        return 'blue'
    else:
        return 'gray'  # 계절 정보가 없는 경우
                            
# 지도를 생성하고 Streamlit에 표시하는 함수
def display_fire_incidents_map(df):
    # NaN 값을 가진 행 제거
    df_filtered = df.dropna(subset=['위도', '경도'])
    
    # 서울의 중심 좌표로 지도 생성
    map_seoul = folium.Map(location=[37.5665, 126.9780], zoom_start=11)
    
    # 데이터프레임을 순회하며 CircleMarker 추가
    for idx, row in df_filtered.iterrows():
        color = get_color(row['계절'])  # 계절별 색상
        tooltip_text = f'출동소요시간: {row["출동소요시간"]}초'  # 툴팁 텍스트
        popup_html = create_popup_html(row)  # 팝업 HTML 텍스트 생성
        popup = folium.Popup(popup_html, max_width=300)  # 여기서 Popup 객체 생성

        folium.CircleMarker(
            [row['위도'], row['경도']],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            tooltip=tooltip_text,
            popup=popup  # 생성된 Popup 객체를 사용
        ).add_to(map_seoul)
    
    # Streamlit에 지도 표시
    folium_static(map_seoul, width=800)                        
