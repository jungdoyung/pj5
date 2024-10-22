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

# 2 프레임
# 보고서명 및 폴더 선택, 새 폴더 만들기

if github_info_loaded:
    with st.expander("📝 보고서 선택", expanded=st.session_state['check_report']):

        folder_list =["reportFiles","analysisReportFiles","audioReportFiles", "keywordReportFiles"]

        # 2차원 배열에 각 폴더별 파일 리스트 저장
        file_lists = []
        
        # 각 폴더에 대해 파일 리스트 가져오기
        for folder_name in folder_list:
            # 각 폴더에서 파일 리스트를 가져와서 2차원 배열에 저장
            file_list = bd.get_reportType_file_list_from_github(
                st.session_state['github_repo'], 
                st.session_state['github_branch'], 
                st.session_state['github_token'], 
                folder_name
            )
            
            # 결과를 2차 배열에 추가
            file_lists.append(file_list)

        # 업무 보고서 자동 완성 리스트
        type_list = ["• 업무 보고서 자동 완성", "• 보고서 비교분석 완성","• 음성 파일 보고서 완성","• Quickly 키워드 보고서 완성"]
       
        selected_type = st.radio("보고서 유형 선택하세요.",type_list, key="radio-type")     
        if selected_type == type_list[0]: 
            st.session_state['sub_title']="업무 보고서<br/>리스트 선택"
            st.session_state['report_folder_option'] = [folderlist_init_value] + file_lists[0]
            st.session_state['selected_report_folder_name'] = folder_list[0]
            if st.session_state['report_type_index'] != 0:
                st.session_state['report_type_index'] = 0
                st.session_state['selected_report_folder_index'] = 0
                st.session_state['selected_report_file_name']=""
                st.session_state['check_result'] = False
        elif selected_type == type_list[1]:
            st.session_state['sub_title']="보고서 비교분석<br/>리스트 선택"
            st.session_state['report_folder_option'] = [folderlist_init_value] + file_lists[1]
            st.session_state['selected_report_folder_name'] = folder_list[1]
            if st.session_state['report_type_index'] != 1:
                st.session_state['report_type_index'] = 1
                st.session_state['selected_report_folder_index'] = 0
                st.session_state['selected_report_file_name']=""
                st.session_state['check_result'] = False
        elif selected_type == type_list[2]: 
            st.session_state['sub_title']="음성파일 보고서<br/>리스트 선택"
            st.session_state['report_folder_option'] = [folderlist_init_value] + file_lists[2]
            st.session_state['selected_report_folder_name'] = folder_list[2]
            if st.session_state['report_type_index'] != 2:
                st.session_state['report_type_index'] = 2
                st.session_state['selected_report_folder_index'] = 0
                st.session_state['selected_report_file_name']=""
                st.session_state['check_result'] = False
        elif selected_type == type_list[3]:
            st.session_state['sub_title']="키워드 보고서<br/>리스트 선택"
            st.session_state['report_folder_option'] = [folderlist_init_value] + file_lists[3]
            st.session_state['selected_report_folder_name'] = folder_list[3]
            if st.session_state['report_type_index'] != 3:
                st.session_state['report_type_index'] = 3
                st.session_state['selected_report_folder_index'] = 0
                st.session_state['selected_report_file_name']=""
                st.session_state['check_result'] = False

        st.markdown(
            "<hr style='border-top:1px solid #dddddd;border-bottom:0px solid #dddddd;width:100%;padding:0px;margin:0px'></hr>",
            unsafe_allow_html=True
        )
    
        col1, col2 = st.columns([0.21, 0.79])
        with col1:
            st.write("")
            st.markdown(
                f"<p style='font-size:14px; font-weight:bold; color:#000000;text-align:center;'>{st.session_state['sub_title']}</p>",
                unsafe_allow_html=True
            )
            
        with col2:
            # 폴더 존재 확인 및 생성
            # 'selected_file_name'가 file_list에 있을 때만 index 설정
            #selected_index = st.session_state['selected_report_folder_index']
            #st.session_state['report_folder_option'] = [folderlist_init_value] + file_lists[0]
            # 폴더 선택 selectbox 생성 (새 폴더 추가 후, 선택값으로 설정)
            selected_file_name = st.selectbox(
                "등록된 결과 보고서를 선택하세요.",
                options= st.session_state['report_folder_option'],  # 옵션 리스트에 새 폴더 반영
                index=st.session_state['selected_report_folder_index'],  # 새로 선택된 폴더를 기본값으로 선택
                key="selected_report_folder"
            )
            # 파일 업로드와 요청사항 리스트의 기본 폴더 설정
            if selected_file_name != folderlist_init_value:
                st.session_state['selected_report_file_name'] = f"{selected_file_name}"
                st.session_state['selected_report_folder_index'] = st.session_state['report_folder_option'].index(selected_file_name) 
                st.session_state['check_report'] = False
                st.session_state['check_result'] = True
                #st.success(f"[{selected_file_name}] 보고서명이 선택되었습니다.")  


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
