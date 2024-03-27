import streamlit as st

# 0. 모든 페이지 - 사이드바에 페이지 링크 추가
@st.cache_data
def setup_sidebar_links():
    """
    Adds links to various pages in the sidebar of the Streamlit application.

    This function utilizes Streamlit's sidebar functionality to add navigation links
    that allow users to easily switch between different pages of the application.
    Each link is associated with a specific page of the application and is represented
    with a unique icon for intuitive navigation.

    Args:
        None

    Returns:
        None

    Notes:
        - This function must be called at the start of the Streamlit app to ensure the
          sidebar links are setup before any page content is rendered.
        - The `@st.cache_data` decorator is used to cache the setup of sidebar links,
          preventing unnecessary re-executions and enhancing app performance.
    """
    st.sidebar.page_link("서울시_화재사고_현황.py", label="서울시 화재사고 현황", icon="🔥")
    st.sidebar.page_link("pages/1-화재사고_취약지역.py", label="화재사고 취약지역", icon="⚠️")
    st.sidebar.page_link("pages/2-소방_인프라_분석.py", label="소방 인프라 분석", icon="🚒")
    st.sidebar.page_link("pages/3-비상소화장치_위치_제안.py", label="비상소화장치 위치 제안", icon="🧯")
    st.sidebar.page_link("pages/4-건의사항.py", label="건의사항", icon="💬")

# 3. 소방 인프라 분석 페이지 - 계절별 색상 마크다운 박스 함수
@st.cache_data
def display_season_colors():
    """
    Displays a visual guide for seasonal colors used in the application's graphs and maps.
    This function creates a markdown section in the Streamlit application that visually
    demonstrates the color scheme associated with each season. Spring is represented by green,
    summer by red, autumn by orange, and winter by blue. Each season's color is displayed in a
    flexible, responsive box that adjusts to the screen size.

    Args:
        None

    Returns:
        None

    Notes:
        This function uses HTML and CSS for styling the color guide. The unsafe_allow_html
        parameter of the st.markdown method is set to True to enable HTML rendering.
    """
    st.markdown("""
        <style>
            .color-box-container {
                display: flex;
                justify-content: space-around; /* 가로로 나열하며 동일한 간격 유지 */
                flex-wrap: wrap; /* 필요한 경우 줄 바꿈 */
            }
            .color-box {
                padding: 10px;
                border-radius: 5px;
                color: #fff;
                margin: 10px;
                font-weight: bold;
                text-align: center; /* 글자 가운데 정렬 */
                flex: 1; /* Flex 항목들이 유연하게 늘어나서 사용 가능한 공간을 채움 */
                min-width: 120px; /* 최소 너비 설정 */
            }
            .spring { background-color: #2ecc71; }
            .summer { background-color: #e74c3c; }
            .autumn { background-color: #f39c12; }
            .winter { background-color: #3498db; }
        </style>
        <div class="color-box-container">
            <div class="color-box spring">봄 - 초록색</div>
            <div class="color-box summer">여름 - 빨간색</div>
            <div class="color-box autumn">가을 - 주황색</div>
            <div class="color-box winter">겨울 - 파란색</div>
        </div>
        """, unsafe_allow_html=True)

    

# 3,4 페이지 버튼 스타일 html 함수 
@st.cache_data
def create_html_button(button_text):
    """
    Generates and displays an HTML button within a Streamlit application. The button is styled
    and displayed based on the provided button text. This function is primarily for display
    purposes as the button is non-interactive (pointer-events are disabled).

    Args:
        button_text (str): The text to be displayed on the button. This string is directly
                           inserted into the HTML template for the button.

    Returns:
        None

    Notes:
        This function uses HTML for the button's styling and markdown for its display within
        the Streamlit app. The `unsafe_allow_html` parameter is set to True to enable the rendering
        of HTML content. The button created by this function is non-interactive, as it is intended
        for display purposes only.
    """
    button_html = f"""
                <div style='text-align: center; margin-bottom: 20px;'>
                    <button style='
                        border: none;
                        pointer-events: none;
                        color: white;
                        padding: 6px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        font-weight: bold;
                        margin: 4px 2px;
                        cursor: pointer;
                        background-color: #ED1B24;
                        border-radius: 8px;'>
                    {button_text}
                    </button>
                </div>
                """
    st.markdown(button_html, unsafe_allow_html=True)


# 4. 비상소화장치 위치 제안 - 오른쪽 열: 각 위치별 상세정보
@st.cache_data
def show_location_info(st, location_number, location_details, images):
    """
    Displays detailed information about a specific location along with related images
    within a Streamlit application. This function creates a popover component that shows
    the location details and images when interacted with.

    Args:
        st: The Streamlit library module, used to render the components in the app.
        location_number (str): A string identifier for the location (e.g., "Location 1"),
                               which is displayed as the title of the popover.
        location_details (str): A descriptive text about the location. This can include
                                HTML content for styled display within the Streamlit app.
        images (list of tuples): A list of tuples, where each tuple contains the file path
                                 to an image and a caption for that image. The images are
                                 displayed within the popover with their corresponding captions.

    Returns:
        None

    Notes:
        This function uses the `st.popover` method to create a clickable popover component.
        The `unsafe_allow_html=True` parameter allows the use of HTML in the markdown for
        `location_details`, enabling styled text display. Images are displayed with a fixed
        width of 400 pixels.
    """
    with st.popover(f"**{location_number}**", use_container_width=True):
        st.markdown(location_details, unsafe_allow_html=True)
        for img_path, caption in images:
            st.image(img_path, caption=caption, width=400)

