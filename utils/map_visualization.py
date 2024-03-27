import folium
import streamlit.components.v1 as components
import geopandas as gpd
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import streamlit as st
from folium.features import DivIcon

# 2. 화재사고 취약 페이지 - 서울시 구별 취약지역 점수 지도
@st.cache_data
def create_and_show_map(_data, columns, key_on, fill_color='YlOrRd'):
    """
    Creates and displays a Choropleth map layer using geographical information from a GeoDataFrame
    to visualize Seoul's districts data. The map highlights areas based on the specified data column values,
    allowing for a visual representation of various metrics across the city.

    Args:
        _data (GeoDataFrame): The GeoDataFrame containing the data and geographical information to be visualized.
                              It must include a 'geometry' column with geographic data.
        columns (list): A list containing the name of the column in GeoDataFrame that matches the 'key_on' parameter,
                        and the name of the column containing the values to visualize.
        key_on (str): The name of the feature property in the GeoDataFrame to bind the data to. For example,
                      'feature.properties.district'.
        fill_color (str, optional): The color palette for the Choropleth layer. Defaults to 'YlOrRd'.

    Returns:
        str: An HTML representation string of the generated Folium map.
    """

    # 서울시 중심부의 위도와 경도로 지도 초기화
    seoul_map = folium.Map(location=[37.5642135, 127.0016985], zoom_start=11)
    
    # Choropleth 레이어 추가
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

    # 각 자치구의 중심 좌표에 텍스트 레이블 추가
    for _, row in _data.iterrows():
        # 자치구의 중심 좌표 계산
        centroid = row['geometry'].centroid
        text = row['자치구']
        
        # 중심 좌표에 텍스트 레이블을 표시하는 마커 추가
        folium.Marker(
            [centroid.y, centroid.x],
            icon=DivIcon(
                icon_anchor=(0,0),
                html=f'<div style="font-size: 8pt; font-weight: bold; background: rgba(245, 245, 245, 0.6); padding: 4px 6px; border-radius: 5px; text-align: center; color: #1C1C1C; white-space: nowrap; min-width: 50px;">{text}</div>',
            )
        ).add_to(seoul_map)

    # HTML로 변환 후 반환
    return seoul_map._repr_html_()

# 3. 서울시 소방 인프라 페이지 - tab1: 서울시 소방서 및 안전센터 시각화
@st.cache_data
def create_folium_map(df):
    """
    Generates a Folium map with marked locations based on the input DataFrame. Each location is represented as a 
    CircleMarker on the map, with different colors indicating the type of fire service facility (e.g., fire stations, 
    safety centers, rescue squads). A popup attached to each marker provides detailed information about the facility.

    Args:
        df (pandas.DataFrame): A DataFrame containing columns for the name and type of each facility, as well as 
                               their latitude ('위도') and longitude ('경도'). Expected columns include '서ㆍ센터명' 
                               for the facility name and '유형구분명' for the facility type.
    
    Returns:
        None: The function directly renders a Folium map in the Streamlit app using folium_static.
    """
    m = folium.Map(location=[37.5642135, 127.0016985], zoom_start=11)
    colors = {
        '소방서': 'red',
        '안전센터': 'blue',
        '구조대': 'orange',
        '소방항공대': 'black',
        '특수대응단': 'yellow'
    }
    for index, row in df.iterrows():
        popup_content = f"<b>서ㆍ센터명:</b> {row['서ㆍ센터명']}<br><b>유형구분명:</b> {row['유형구분명']}"
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=8,
            color=colors[row['유형구분명']],
            fill=True,
            fill_color=colors[row['유형구분명']],
            fill_opacity=0.5,
            popup=folium.Popup(popup_content, max_width=300)
        ).add_to(m)

    folium_static(m)

# 3. 서울시 소방 인프라 페이지 - tab2: 비상 소화장치 클러스터링 시각화
def display_folium_map_with_clusters(gdf):
    """
    Displays a Folium map with clustered points from a GeoDataFrame in Streamlit. This function
    creates a map centered on Seoul and uses clustering to group points based on proximity, 
    improving the visualization of densely populated areas.

    Args:
        gdf (GeoDataFrame): A GeoDataFrame containing points to be displayed on the map. It must include
                            a 'geometry' column with point coordinates and should contain '구' (district)
                            and '동' (neighborhood) information for tooltips.

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


# 3. 서울시 소방 인프라 페이지 - tab3: 서울시 소방용수 그리드 시각화
@st.cache_data
def visualize_fire_water(grid, column_name='소방용수_수'):
    """
    Visualizes the distribution of firefighting water resources on a map using GeoPandas and Folium. 
    The function displays locations with firefighting water and changes the color on the map 
    based on the quantity of available firefighting water.

    Args:
        grid (DataFrame): A DataFrame containing the distribution data of firefighting water. 
                          The 'geometry' column should contain geographic information in WKT format, 
                          and the column specified by column_name should contain the quantity of 
                          firefighting water.
        column_name (str, optional): The name of the column representing the quantity of firefighting 
                                     water. Defaults to '소방용수_수'.

    Note:
        The color_scale function nested within visualizes the amount of firefighting water by 
        assigning specific colors based on the water quantity, enhancing the map's visual appeal and 
        informational value.
    """
    # geometry 열을 GeoPandas의 geometry로 변환
    grid['geometry'] = gpd.GeoSeries.from_wkt(grid['geometry'])
    gdf = gpd.GeoDataFrame(grid, geometry='geometry')
    gdf.crs = "EPSG:4326"

    # 지도 객체 생성 (서울시 중심 좌표로 설정)
    map_fw = folium.Map(location=[37.564, 126.997], zoom_start=11, tiles='OpenStreetMap')

    # 색상을 결정하는 함수(. 여기서는 단순화를 위해 소방용수의 양에 따라 색상을 분류)
    @st.cache_data
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
            return '#808080' 


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

# 3. 소방 인프라 분석 페이지 - 골든타임 초과 시각화 함수(팝업텍스트 생성, 색 생성, 시각화)
@st.cache_data
def display_fire_incidents_map(df):
    """
    Displays a map in Streamlit showing the locations of fire incidents in Seoul, with markers
    color-coded by season and detailed incident information available in a popup.

    Args:
        df (DataFrame): A pandas DataFrame containing fire incident data with columns for latitude ('위도'),
                        longitude ('경도'), number of deaths ('사망수'), number of injuries ('부상자수'),
                        property damage amount ('재산피해금액'), response time ('출동소요시간'),
                        suppression time ('화재진압시간'), location ('시군구명', '읍면동명'),
                        season ('계절'), time of day ('시간대'), and incident date ('화재발생일시').

    The function includes nested functions `create_popup_html` to generate HTML content for popups and
    `get_color` to determine marker colors based on the season of the incident. It then adds markers to
    the map with tooltips showing the response time and popups with detailed incident information.

    Note:
        - The `create_popup_html` function formats the popup content using HTML and CSS for styling.
        - The `get_color` function assigns colors to markers based on the season ('봄': green, '여름': red,
          '가을': orange, '겨울': blue, and default: gray).
    """

    # NaN 값을 가진 행 제거
    df_filtered = df.dropna(subset=['위도', '경도'])
    
    # 서울의 중심 좌표로 지도 생성
    map_seoul = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

    # 팝업 텍스트를 생성하는 함수 (HTML 스타일 적용)
    @st.cache_data
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
    @st.cache_data
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
            return 'gray'  
    
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

# 4. 비상소화장치 위치 제안 페이지 - 송파구 비상소화장치 제안 위치 시각화
@st.cache_data
def display_fire_extinguisher_map(center, locations, zoom_start=13):
    """
    Generates and displays a map with locations and information about emergency fire extinguishers.

    Args:
        center (tuple): The latitude and longitude that will be the center of the map.
        locations (list of tuples): A list of tuples, each representing the location of an emergency fire extinguisher.
                                    Each tuple consists of (latitude, longitude, description, image URL, priority).
        zoom_start (int, optional): The initial zoom level of the map. Defaults to 13.

    Returns:
        None: This function does not return anything but displays a map within a Streamlit application.
    """
    m = folium.Map(location=center, zoom_start=zoom_start)

    # 우선순위에 따른 마커 색상 매핑
    color_mapping = {1: "red", 2: "orange", 3: "green", 4: "blue"}

    for idx, (lat, lon, label, image_path, priority) in enumerate(locations):
        # 마커에 표시할 번호를 포함한 HTML 문자열 생성
        icon_html = f"""<div style="font-family: Arial; font-size: 12px; color: blue;"><b>{idx+1}</b></div>"""
        
        # DivIcon을 사용하여 번호를 포함한 아이콘 생성
        icon = folium.DivIcon(html=icon_html)

        # 우선순위에 해당하는 색상 선택
        marker_color = color_mapping.get(priority, "gray")  # 기본값으로 'gray' 설정

        # DivIcon 아이콘을 사용하는 마커 추가
        folium.Marker([lat, lon], icon=icon).add_to(m)

        # 팝업 추가
        folium.Marker(
            location=[lat, lon],
            popup=f'<b>{idx+1}. {label}</b></b><br>{lat},{lon}</b><br><img src="{image_path}" width="150" height="100">',
            icon=folium.Icon(color=marker_color, icon="info-sign"),
        ).add_to(m)

    # Streamlit을 사용하여 지도 표시
    folium_static(m)

# 4. 비상소화장치 위치 제안 페이지 - 하단 tab1: 송파구 현재 비상소화장치 위치 시각화
@st.cache_data
def create_fire_equip_map(fire_equip):
    """
    Generates and displays a map showing the distribution of fire equipment across a specific area, 
    with markers colored according to the type of area where the equipment is installed.

    Args:
        fire_equip (DataFrame): A pandas DataFrame containing columns for the location ('경위도좌표Y', '경위도좌표X'), 
                                area type ('설치지역'), equipment type ('설치유형구분'), detailed location ('상세위치'), 
                                and address ('주소') of each piece of fire equipment.

    Returns:
        None: This function does not return anything but saves a map as an HTML file and displays it within a Streamlit application.
              The map includes a legend explaining the color coding of the markers according to the installation area.
    """

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

    components.html(map_html, height=600) 
