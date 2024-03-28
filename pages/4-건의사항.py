import streamlit as st
import pandas as pd
import os
from utils.ui_helpers import setup_sidebar_links
from utils.data_loader import load_data

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded", page_icon='💬'
)

setup_sidebar_links()

def main():
    # 페이지 제목 및 설명
    st.header('건의사항 페이지', divider='gray')
    st.markdown("""
    대시보드를 개선해 나갈 수 있도록 **건의사항을 남겨주세요🙇‍♂️**
    - 🛠 **기능 개선이 필요한 부분**
    - ✨ **추가되었으면 하는 새로운 기능**
    - 🐞 **사용 중 발견한 버그나 오류**
    """)

    # 건의사항 파일 경로
    file_path = 'recommendations/건의사항.csv'  

    with st.container(border=True):
        # 사용자로부터의 입력 처리
        anonymous = st.checkbox('익명으로 제출하기')
        if anonymous:
            username = "익명"
            email = "익명"
        else:
            username = st.text_input('이름', key='username')  
            email = st.text_input('이메일', key='email')

        category = st.selectbox('카테고리', ['기능 개선', '새 기능 제안', '버그 신고', '기타'], key='category')
        suggestion = st.text_area('건의사항', key='suggestion')
        file = st.file_uploader("문제를 보여줄 스크린샷이나 문서 첨부", type=['png', 'jpg', 'jpeg', 'pdf'], key='file')

        if file is not None:
            specific_file_path = f'recommendations/{file.name}'
            with open(specific_file_path, "wb") as f:
                f.write(file.getbuffer())
            st.success('파일이 성공적으로 업로드되었습니다.')
            file_info = specific_file_path
        else:
            file_info = "첨부파일 없음"

        submit_button = st.button('제출')

    # 제출 버튼 클릭 시 데이터 처리
    if submit_button:
        new_data = {'이름': username, '이메일': email, '카테고리': category, '건의사항': suggestion, '파일': file_info}
        df = pd.DataFrame([new_data])  # 새로운 데이터프레임 생성
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)  # 기존 파일에 데이터 추가
        else:
            df.to_csv(file_path, mode='w', header=True, index=False)  # 새 파일 생성
        st.success('건의사항이 성공적으로 제출되었습니다.')

    # 파일 존재 여부 및 건의사항 처리
    if os.path.exists(file_path):
        df_건의사항 = pd.read_csv(file_path)  # 파일 로드
        st.divider()
        if '건의사항' in df_건의사항.columns:  # '건의사항' 열 존재 확인
            selected_indices = st.multiselect(
                '해결된 건의사항을 선택하세요.', 
                df_건의사항.index, 
                format_func=lambda x: df_건의사항.loc[x, '건의사항']  # 건의사항 내용으로 선택 목록 표시
            )
            if st.button('선택 항목 삭제'):
                df_건의사항 = df_건의사항.drop(index=selected_indices)  # 선택된 건의사항 삭제
                df_건의사항.to_csv(file_path, index=False)  # 변경사항 저장
                st.success('선택한 항목이 삭제되었습니다.')
            st.dataframe(df_건의사항, width=800, height=300)  # 업데이트된 건의사항 표시
    
if __name__ == "__main__":
    main()
