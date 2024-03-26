import streamlit as st
import pandas as pd
import geopandas as gpd

# csv 데이터 로딩 함수
@st.cache_data
def load_data(csv_file, encoding=None):
    if encoding:
        return pd.read_csv(csv_file, encoding=encoding)
    else:
        return pd.read_csv(csv_file)

# SHP 데이터 로딩 함수
@st.cache_data
def load_shp_data(shp_file):
    return gpd.read_file(shp_file)

# GeoJson 데이터 로딩 함수
@st.cache_data
def load_json_data(geojson_file):
    return gpd.read_file(geojson_file)

# Excel 데이터 로딩 함수
@st.cache_data
def load_excel_data(excel_file):
    return pd.read_excel(excel_file)

# 비상소화장치 위치 데이터 로딩 함수
@st.cache_data
def get_locations_data():
    """
    비상 소화장치 위치 데이터를 반환하는 함수.
    각 위치의 위도, 경도, 설명 및 이미지 URL 포함.
    """
    locations = [
                (37.5085071, 127.0825862, '잠실동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/01_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.50511389, 127.0817572, '잠실동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/02_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.50231025, 127.0901942, '삼전동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/03_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.50094046, 127.0936817, '삼전동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/04_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.504103, 127.090679, '삼전동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/05_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.49991962, 127.0974103, '석촌동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/06_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.50097974,127.1000492, '석촌동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/07_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.50884075,127.1087034, '송파동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/08_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.511740, 127.110053, '방이동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/09_%EC%A2%8C%ED%91%9C.png?raw=true'),  
                (37.51299316, 127.1161285, '방이동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/10_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.499000, 127.120611, '가락본동, 가락1동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/11_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.496917, 127.120417, '가락본동, 가락1동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/12_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.500694, 127.112639, '송파2동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/13_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.492321, 127.154682, '마천1동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/14_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.499138, 127.149098, '마천2동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/15_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.493358, 127.142836, '거여1동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/16_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.497698, 127.143332, '거여1동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/17_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.503962, 127.140793, '오금동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/18_%EC%A2%8C%ED%91%9C.png?raw=true'),
                (37.502313, 127.134786, '오금동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/19_%EC%A2%8C%ED%91%9C.png?raw=true')
            ]
    return locations