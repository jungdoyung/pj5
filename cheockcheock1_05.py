import streamlit as st
import backend as bd
import time
import io
import os

# Frontend 기능 구현 시작 ---

# GitHub 정보가 있는지 확인하고 파일 업로드 객체를 출력
github_info_loaded = bd.load_env_info()

#Session_state 변수 초기화
folderlist_init_value = "보고서를 선택하세요."

# 세션 상태에 각 변수 없다면 초기화
if 'report_folder_option' not in st.session_state:
    st.session_state['report_folder_option'] = []
if 'selected_report_folder_index' not in st.session_state:
    st.session_state['selected_report_folder_index'] = 0
if 'selected_report_file_name' not in st.session_state:
    st.session_state['selected_report_file_name']=""
if 'selected_report_folder_name' not in st.session_state:
    st.session_state['selected_report_folder_name']=""
if 'check_result' not in st.session_state:  
    st.session_state['check_result'] = False
if 'check_report' not in st.session_state:
    st.session_state['check_report'] = True
if 'sub_title' not in st.session_state:
    st.session_state['sub_title'] = ""
if 'report_type_index' not in st.session_state:
    st.session_state['report_type_index'] = 0
    
# 1 프레임
# 보고서 타이틀
col1, col2 = st.columns([0.55,0.45])
with col1:
    st.markdown(
        "<p style='font-size:25px; font-weight:bold; color:#000000;'>결과 보고서 현황 📋</p>",
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        "<div style='text-align:right;width:100%;'><p style='font-size:13px; font-weight:normal; color:#aaaaaa; margin-top:10px;'>by <b style='font-size:16px;color:#0099FF'>CheokCeock</b><b style='font-size:22px;color:#009999'>1</b> <b style='font-size:14px;'>prototype v.01</b></p></div>",
        unsafe_allow_html=True
    )


# 3 프레임
# 결과 보고서 보기/ 결과 보고서 저장
file_content = None
result_path = None

with st.expander("📊 결과 보고서 보기", expanded=st.session_state['check_result']):
    if "selected_report_file_name" in st.session_state and st.session_state['selected_report_file_name']:
        st.markdown(
            "<hr style='border-top:1px solid #dddddd;border-bottom:0px solid #dddddd;width:100%;padding:0px;margin:0px'></hr>",
            unsafe_allow_html=True
        )  
        st.session_state['check_result'] = True
        st.session_state['check_report'] = False
        with st.spinner('선택한 결과 보고서를 불러오는 중입니다...'):
            result_folder = st.session_state['selected_report_folder_name']
            result_file = st.session_state['selected_report_file_name']
            result_path = f"{result_folder}/{result_file}"
            # GitHub에서 HTML 파일 데이터 가져오기
            file_content = bd.get_file_from_github(
                st.session_state['github_repo'], 
                st.session_state['github_branch'], 
                f"{result_path}",  # 폴더 경로와 파일 이름을 합침
                st.session_state['github_token']
            )
            time.sleep(1)  # 예를 들어, 5초 동안 로딩 상태 유지
        if file_content:
            # HTML 파일 내용을 화면에 출력
            #st.markdown(file_content, unsafe_allow_html=True)
            html_content = file_content.getvalue().decode('utf-8')

            st.components.v1.html(html_content, height=1024, scrolling=True)
        else:
            st.error(f"{selected_file} 파일 데이터를 가져오는 데 실패했습니다.")
            


    st.markdown(
        "<hr style='border-top:1px solid #dddddd;border-bottom:0px solid #dddddd;width:100%;padding:0px;margin:0px'></hr>",
        unsafe_allow_html=True
    )
    
# 결과 저장 버튼
    col1, col2 = st.columns([0.5, 0.5])
    with col1:   
        if file_content and result_path:
            # 폴더명을 제외한 순수 파일명만 추출
            pure_file_name = os.path.basename(result_path)
            if st.download_button(
                label="📥 다운로드",
                use_container_width=True,
                data=file_content.getvalue(),
                file_name=pure_file_name,
                mime="text/html"
            ):
                st.session_state['check_result'] = True
                st.session_state['check_report'] = False

        else:
            st.warning("결과 보고서를 먼저 선택하세요.")
    with col2:
        st.write("")

    
# Frontend 기능 구현 끝 ---
