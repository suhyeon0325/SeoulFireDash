import streamlit as st
import pandas as pd
import os
from utils.data_loader import set_page_config
from streamlit_option_menu import option_menu
# 페이지 설정
st.set_page_config(
    page_title="건의사항",
    initial_sidebar_state="expanded",
)
def menu():
    with st.sidebar:
        # 옵션 메뉴를 사용하여 메인 메뉴 생성
        selected = option_menu("메인 메뉴", ["화재사고 현황", '화재사고 취약지역', "소방 인프라 분석", "비상소화장치 위치 제안", "건의사항"], 
                                icons=['bi-fire', 'bi-exclamation-triangle-fill', 'bi-truck', 'bi-lightbulb', 'bi-chat-dots'], 
                                menu_icon="house", default_index=0)

    # 선택된 메뉴에 따라 페이지 전환
    if selected == '화재사고 현황':
        st.switch_page("서울시_화재사고_현황.py")
    elif selected == '화재사고 취약지역':
        st.switch_page("pages/1 - 화재사고_취약지역.py")
    elif selected == '소방 인프라 분석':
        st.switch_page('pages/2 - 서울시_소방_인프라.py')
    elif selected == '비상소화장치 위치 제안':
        st.switch_page('pages/3 - 비상소화장치_위치_제안.py')
    elif selected == '건의사항':
        st.switch_page('pages/4 - 건의사항.py')

# 메뉴 함수 호출
menu()
def main():
    help_text = """
    대시보드를 함께 개선해 나갈 수 있도록 건의사항을 남겨주세요:
     - 기능 개선이 필요한 부분
     - 추가되었으면 하는 새로운 기능
     - 사용 중 발견한 버그나 오류
    상황을 구체적으로 설명해 주시면 더욱 정확하게 반영할 수 있습니다. 감사합니다.
    """


    st.header('건의사항 페이지', help=help_text, divider='gray')

    with st.container(border=True):
    # 사용자로부터 입력 받기
        username = st.text_input('이름')
        email = st.text_input('email')
        suggestion = st.text_area('건의사항')
        submit_button = st.button('제출')
        
        # new_data = {'이름': username, '이메일': email, '건의사항': suggestion}
        # df = pd.DataFrame([new_data])
        # st.write(df)
        file_path = 'recommendations/건의사항.csv'
        # file_path는 수현님이 저장하기를 원하시는 경로로 위치해주시면 되요
    
    st.divider()
    
    if submit_button:
    # 이후 단계에서 건의사항을 저장하는 코드를 추가
        new_data = {'이름': username, '이메일': email, '건의사항': suggestion}
        df = pd.DataFrame([new_data])
        # st.write(df)
    # 건의사항을 CSV 파일에 추가하기
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, mode='w', header=True, index=False)
    if os.path.exists(file_path):
        df_건의사항 = pd.read_csv(file_path)
        # 선택 가능한 건의사항 리스트를 표시
        selected_indices = st.multiselect('해결된 건의사항을 선택하세요.', df_건의사항.index, format_func=lambda x: df_건의사항['건의사항'][x])
        
        if st.button('선택 항목 삭제'):
            # 선택된 인덱스를 제외하고 나머지 데이터를 필터링
            df_건의사항 = df_건의사항.drop(index=selected_indices)
            # 변경된 데이터프레임을 다시 CSV에 저장
            df_건의사항.to_csv(file_path, index=False)
            st.success('선택한 항목이 삭제되었습니다.')
        st.dataframe(df_건의사항, width=500, height=300)       
    # if os.path.exists(file_path):
    #     df_건의사항 = pd.read_csv(file_path)
    #     selected_indices = st.multiselect('해결된 건의사항을 선택하세요.', df_건의사항.index)
    #     if st.button('선택 항목 삭제'):
    #         df_건의사항 = df_건의사항.drop(selected_indices)
    #         df_건의사항.to_csv(file_path, index=False)
    #         st.success('선택한 항목이 삭제되었습니다.')
    #     st.write(df_건의사항)
    
    # df_건의사항 = pd.read_csv('/Users/youngki/Desktop/streamlit_semi/data/건의사항.csv')
    # st.write(df_건의사항)
    
    
if __name__ =="__main__":
    main()