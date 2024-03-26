import streamlit as st
import pandas as pd
import os
from utils.etc import setup_sidebar_links


# 페이지 설정
st.set_page_config(
   layout="wide",
   initial_sidebar_state="expanded", page_icon='💬'
)
setup_sidebar_links()
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
        # 익명 기능 선택
        anonymous = st.checkbox('익명으로 제출하기')
        if anonymous:
            username = "익명"
            email = "익명"
        else:
            username = st.text_input('이름')
            email = st.text_input('이메일')

        category = st.selectbox('카테고리', ['기능 개선', '새 기능 제안', '버그 신고', '기타'])
        suggestion = st.text_area('건의사항')
        file = st.file_uploader("문제를 보여줄 스크린샷이나 문서 첨부", type=['png', 'jpg', 'jpeg', 'pdf'])

        # 파일 처리 예시
        if file is not None:
            # 파일 저장 경로 지정
            file_path = f'recommendations/{file.name}'
            # 파일 저장
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            # 저장된 파일 경로를 출력하거나 로깅
            st.success('파일이 성공적으로 업로드되었습니다.')
            file_info = file_path  # 파일 경로를 건의사항과 함께 저장할 때 사용
        else:
            file_info = "첨부파일 없음"

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