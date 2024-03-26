import streamlit as st

# HTML과 CSS를 사용하여 스타일링된 마크다운 텍스트 정의
def display_season_colors():
    st.markdown("""
        <style>
            .color-box {
                padding: 10px;
                border-radius: 5px;
                color: #fff;
                margin: 10px 0;
            }
            .spring { background-color: #2ecc71; }
            .summer { background-color: #e74c3c; }
            .autumn { background-color: #f39c12; }
            .winter { background-color: #3498db; }
        </style>
        <div>
            <div class="color-box spring">봄 - 초록색</div>
            <div class="color-box summer">여름 - 빨간색</div>
            <div class="color-box autumn">가을 - 주황색</div>
            <div class="color-box winter">겨울 - 파란색</div>
        </div>
        """, unsafe_allow_html=True)

def create_link_button(title, url, help_text):
    """
    Streamlit의 link_button을 생성하는 함수.

    :param title: 버튼에 표시될 텍스트입니다.
    :param url: 버튼 클릭 시 이동할 URL입니다.
    :param help_text: 버튼에 마우스를 올렸을 때 보여줄 도움말입니다.
    """
    st.link_button(title, url, use_container_width=True, help=help_text)

def display_fire_safety_links():
    """
    다양한 소방 및 화재안전 관련 링크를 표시하는 함수.
    """
    create_link_button("일일 화재 현황 📈", "https://www.nfds.go.kr/dashboard/quicklook.do", "한눈에 화재 현황을 확인해보세요.")
    create_link_button("화재예방법 🛡️", "https://www.nfds.go.kr/bbs/selectBbsList.do?bbs=B04", "화재를 예방하는 방법을 알아보세요.")
    create_link_button("소화기 사용요령 🔥", "https://www.nfds.go.kr/bbs/selectBbsDetail.do?bbs=B06&bbs_no=7753&pageNo=1", "소화기 사용법을 올바르게 알고 화재에 대응하세요.")
    create_link_button("옥내소화전 사용방법 🚒", "https://www.nfds.go.kr/bbs/selectBbsDetail.do?bbs=B06&bbs_no=7756&pageNo=1", "옥내소화전 사용 방법을 숙지하세요.")
    create_link_button("소화기 사용기한 확인 ⏳", "https://bigdata-119.kr/service/frxtInfr#tab04", "소화기의 사용 기한을 확인해 안전을 유지하세요.")
    create_link_button("주택용 소방시설 설치 🏠", "https://fire.seoul.go.kr/pages/cnts.do?id=4808", "취약계층을 위한 주택용 소방시설 설치 정보입니다.")
    create_link_button("소방시설 불법행위신고 🚫", "https://fire.seoul.go.kr/pages/cnts.do?id=4113", "불법 소방시설 행위를 신고해 포상금을 받으세요.")
    create_link_button("안전신문고 📢", "https://www.safetyreport.go.kr/#safereport/safereport", "소방 안전 관련 불법 행위를 신고할 수 있는 곳입니다.")
    create_link_button("소방민원센터 📜", "https://www.safeland.go.kr/somin/index.do", "소방 관련 민원을 신청할 수 있는 곳입니다.")
    create_link_button("소방기술민원센터 💡", "https://www.safeland.go.kr/safeland/index.do", "소방시설 및 화재 예방 관련 자료를 제공합니다.")
    create_link_button("칭찬하기 👏", "https://fire.seoul.go.kr/pages/cnts.do?id=184", "소방관님들에게 감사의 메시지를 전하세요.")

def create_html_button(button_text):
    """
    HTML 버튼을 생성하고 Streamlit 앱에 표시하는 함수
    :param button_text: 버튼에 표시될 텍스트
    """
    button_html=f"""
                <div style='text-align: center; margin-bottom: 20px;'>
                    <button style='
                        border: none;
                        pointer-events: none;
                        color: white;
                        padding: 10px 20px;
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

def add_sidebar_page_link(file_path, label, icon):
    """
    Streamlit 사이드바에 페이지 링크를 추가하는 함수입니다.

    :param file_path: 페이지 파일의 경로입니다.
    :param label: 사이드바에 표시될 레이블입니다.
    :param icon: 레이블 옆에 표시될 아이콘입니다.
    """
    st.sidebar.page_link(file_path, label=label, icon=icon)

def setup_sidebar_links():
    """
    사이드바에 여러 페이지 링크를 추가하는 함수입니다.
    """
    add_sidebar_page_link("서울시_화재사고_현황.py", "서울시 화재사고 현황", "🔥")
    add_sidebar_page_link("pages/1-화재사고_취약지역.py", "화재사고 취약지역", "⚠️")
    add_sidebar_page_link("pages/2-소방_인프라_분석.py", "소방 인프라 분석", "🚒")
    add_sidebar_page_link("pages/3-비상소화장치_위치_제안.py", "비상소화장치 위치 제안", "🧯")
    add_sidebar_page_link("pages/4-건의사항.py", "건의사항", "💬")



