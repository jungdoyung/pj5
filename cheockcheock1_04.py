import streamlit as st
import pandas as pd
import backend as bd
import datetime
import time
import openpyxl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import altair as alt
import numpy as np

# Frontend 기능 구현 시작 ---

# GitHub 정보가 있는지 확인하고 파일 업로드 객체를 출력
github_info_loaded = bd.load_env_info()

# 업로드 가능한 파일 크기 제한 (100MB)
MAX_FILE_SIZE_MB = 100
MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024

#Session_state 변수 초기화
folderlist_init_value = "보고서명을 선택하세요."
templatelist_init_value = "불러올 보고서 양식을 선택하세요."
# 세션 상태에 각 변수 없다면 초기화
bd.init_session_state(False)
bd.refresh_page()
     
    
# 1 프레임
# 보고서 타이틀
col1, col2 = st.columns([0.55,0.45])
with col1:
    st.markdown(
        "<p style='font-size:25px; font-weight:bold; color:#000000;'>Quckly 키워드 보고서 완성 ⚡</p>",
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        "<div style='text-align:right;width:100%;'><p style='font-size:13px; font-weight:normal; color:#aaaaaa; margin-top:10px;'>by <b style='font-size:16px;color:#0099FF'>CheokCeock</b><b style='font-size:22px;color:#009999'>1</b> <b style='font-size:14px;'>prototype v.01</b></p></div>",
        unsafe_allow_html=True
    )

# 2 프레임



# 3 프레임


# 4 프레임
# 작성 보고서 요청사항 세부타이틀
st.markdown(
    "<p style='font-size:18px; font-weight:bold; color:#007BFF;'>작성할 보고서 요청사항</p>",
    unsafe_allow_html=True
)

# 5 프레임
# 파일 업로드

# 6 프레임
# 요청사항 갯수 및 기준일자 설정 
with st.expander("⚙️ 키워드 및 요청사항", expanded=st.session_state['check_setting']):
    if 'request_title' not in st.session_state:
        st.session_state['request_title'] = ""
    request_title = st.text_input("키워드 : '키워드를 입력해주세요.", key="request_title_input")
    st.session_state['request_title'] = request_title

    if 'request_text' not in st.session_state:
        st.session_state['request_text'] = ""
    request_text = st.text_area("요청 : '요청할 내용을 입력해주세요.", key="request_text_area")
    st.session_state['request_text'] = request_text
    

# 7 프레임임
# 요청사항 리스트

        
# 8 프레임
# 보고서 작성 실행 버튼
col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
with col1:
    st.write("")
with col2:   

# 보고서 실행 버튼 클릭 시 함수 호출 수정
    if st.button("🚀 보고서 작성 실행", key="generate_report", use_container_width=True):
        st.session_state['check_result']=True
        st.session_state['check_report'] = False
        st.session_state['check_upload'] = False
        st.session_state['check_setting'] = False
    
        if 'html_report' not in st.session_state:
                st.session_state['html_report'] = ""
            
        if not st.session_state.get("openai_api_key"):
            st.error("먼저 OpenAI API 키를 입력하고 저장하세요!")
        elif not st.session_state['request_title'] or not st.session_state['request_text']:
            st.error("보고서명, 요청사항, 기준일자을 모두 입력해야 합니다!")
        else:

            with st.spinner('결과 보고서 작성 중입니다...'):
                # LLM 함수 호출
                title = st.session_state['request_title']
                request = st.session_state['request_text']
        
                responses = bd.run_llm_with_keyword_and_prompt(
                    st.session_state["openai_api_key"], 
                    title, 
                    request
                )
                st.session_state["response"] = responses
                st.session_state['check_result'] = True
                time.sleep(1)  # 예를 들어, 5초 동안 로딩 상태 유지


with col3:
    st.write("")           

# 9 프레임
# 결과 보고서 세부 타이틀
st.markdown(
    "<p style='font-size:18px; font-weight:bold; color:#007BFF;'>결과 보고서</p>",
    unsafe_allow_html=True
)

# 10 프레임
# 결과 보고서 LLM 응답 보기/ 결과 보고서 저장/ 보고서 양식 저장
html_result_value = "<div id='html_result_value'>"
with st.expander("📊 결과 보고서 보기", expanded=st.session_state['check_result']):
    if "response" in st.session_state:
        st.markdown(
            "<hr style='border-top:1px solid #dddddd;border-bottom:0px solid #dddddd;width:100%;padding:0px;margin:0px'></hr>",
            unsafe_allow_html=True
        )  
        st.session_state['check_result'] = True


        for idx, response in enumerate(st.session_state["response"]):
            
            html_response_value = f"<div style='border: 0px solid #cccccc; padding: 1px;'>{response}</div>"
            html_result_value += html_response_value
            st.components.v1.html(html_response_value, height=1024, scrolling=True)

    html_result_value += "</div>"
    st.markdown(
        "<hr style='border-top:1px solid #dddddd;border-bottom:0px solid #dddddd;width:100%;padding:0px;margin:0px'></hr>",
        unsafe_allow_html=True
    )
    
# 결과 저장 버튼
    col1, col2 = st.columns([0.5, 0.5])
    with col1:   
        if st.button("💾 결과 내용 저장", key="save_result", use_container_width=True):
            st.session_state['check_result'] = True
            st.session_state['check_report'] = False
            st.session_state['check_upload'] = False
            st.session_state['check_setting'] = False
            st.session_state['check_request'] = False
            if "response" in st.session_state:                
                
                folder_name = st.session_state['request_title']
                report_date_str = st.session_state.get('report_date_str', datetime.datetime.now().strftime('%Y%m%d'))
                
                # save_html_response 함수를 사용하여 HTML 파일 저장
                file_name, temp_file_path = bd.save_html_response(html_result_value, folder_name, report_date_str)

                # 파일 저장 경로 (reportFiles/{폴더명}/{일자})
                github_folder = f"keywordReportFiles/{folder_name}/{report_date_str}"

                # 폴더 존재 확인 및 생성
                bd.check_and_create_github_folder(github_folder, st.session_state['github_repo'], st.session_state['github_branch'], st.session_state['github_token'])
                
                # GitHub에 HTML 파일 저장
                sha = bd.get_file_sha(st.session_state['github_repo'], f"{github_folder}/{file_name}", st.session_state['github_token'], branch=st.session_state['github_branch'])
                bd.upload_file_to_github(st.session_state['github_repo'], github_folder, file_name, open(temp_file_path, 'rb').read(), st.session_state['github_token'], branch=st.session_state['github_branch'], sha=sha)
                st.session_state['check_result'] = True
                st.success(f"{file_name} 파일이 생성되었습니다.")
                if st.download_button(
                    label="📥 다운로드",
                    use_container_width=True,
                    data=open(temp_file_path, 'r', encoding='utf-8').read(),
                    file_name=file_name,
                    mime="text/html"
                ):
                    st.session_state['check_result'] = True
                    st.session_state['check_report'] = False
                    st.session_state['check_upload'] = False
                    st.session_state['check_setting'] = False
                    st.session_state['check_request'] = False

            else:
                st.warning("결과 보고서를 먼저 실행하세요.")
    with col2:
        st.write("")
        #if st.button("🗃️ 보고서 양식 저장", key="save_template", use_container_width=True):
            #st.session_state['check_result'] = True
            #st.session_state['check_report'] = False
            #st.session_state['check_upload'] = False
            #st.session_state['check_setting'] = False
            #st.session_state['check_request'] = False
            #bd.save_template_to_json()


# 11 프레임
# 결과 보고서 HTML 보기
#if "html_report" in st.session_state:
    #st.write("파일 데이터 추출 보기")
    #html_report_value = f"<div style='border: 2px solid #cccccc; padding: 2px;'>{st.session_state['html_report']}</div>"
    #st.components.v1.html(html_report_value, height=10240, scrolling=True)

# 12 프레임
# 전달된 프롬프트
#st.text_area("전달된 프롬프트:", value="\n\n".join(global_generated_prompt), height=150)
    
# Frontend 기능 구현 끝 ---
