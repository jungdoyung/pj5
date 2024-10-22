import streamlit as st
import pandas as pd
import backend as bd
import datetime
import time
import openpyxl

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
        "<p style='font-size:25px; font-weight:bold; color:#000000;'>업무 보고서 자동 완성 📚</p>",
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
        tab1, tab2, tab3 = st.tabs(["• 등록된 보고서명 선택하기", "• 저장된 보고서 양식 불러오기","• 새로운 보고서명 만들기"])
        with tab1:
            col1, col2 = st.columns([0.21, 0.79])
            with col1:
                st.write("")
                st.markdown(
                    "<p style='font-size:14px; font-weight:bold; color:#000000;text-align:center;'>등록된<br/>보고서명 선택 </p>",
                    unsafe_allow_html=True
                )
            with col2:
                # 폴더 존재 확인 및 생성
                
                folder_list = bd.get_folder_list_from_github(st.session_state['github_repo'], st.session_state['github_branch'], st.session_state['github_token'])
                # st.selectbox bd.위젯 생성 (이제 session_state['selected_folder'] 사용 가능)
    
                # 'selected_folder'가 folder_list에 있을 때만 index 설정
                selected_index = st.session_state['selected_folder_index']
                if st.session_state['selected_folder_name'] in folder_list:
                    selected_index = folder_list.index(st.session_state['selected_folder_name']) + 1
                #else:
                    #selected_index = 0  # 기본값으로 '주제를 선택하세요.' 선택
                st.session_state['selected_folder_index'] = selected_index
                st.session_state['folder_list_option'] = [folderlist_init_value] + folder_list
                # 폴더 선택 selectbox 생성 (새 폴더 추가 후, 선택값으로 설정)
                selected_folder = st.selectbox(
                    "등록된 보고서명 리스트",
                    options=st.session_state['folder_list_option'],  # 옵션 리스트에 새 폴더 반영
                    index=st.session_state['selected_folder_index'],  # 새로 선택된 폴더를 기본값으로 선택
                    key="selected_folder"
                )

                st.session_state['selected_folder_name'] = f"{selected_folder}" 
                # 파일 업로드와 요청사항 리스트의 기본 폴더 설정
                if selected_folder != folderlist_init_value:
                    st.session_state['upload_folder'] = f"uploadFiles/{selected_folder}"
                     
                    st.session_state['selected_template_name'] = templatelist_init_value
                    st.session_state['check_report']=False
                    st.session_state['check_setting']=True
                    st.session_state['selected_template_index'] = 0
                    bd.refresh_page()
                    #st.success(f"[{selected_folder}] 보고서명이이 선택되었습니다.")
                #else:   
                    #st.warning("보고서명을 선택하세요.")
        with tab2:
            col1, col2 = st.columns([0.21, 0.79])
            with col1:
                st.write("")
                st.markdown(
                    "<p style='font-size:14px; font-weight:bold; color:#000000;text-align:center;'>저장된 보고서<br/>양식 불러오기</p>",
                    unsafe_allow_html=True
                )
            with col2:    
                repo = st.session_state["github_repo"]
                branch = st.session_state["github_branch"]
                token = st.session_state["github_token"]
                 # templateFiles 폴더 내 JSON 파일 리스트 가져오기
                template_files = bd.get_template_files_list(repo, branch, token)
                
                if template_files:
                    # 'selected_template'가 template_files에 있을 때만 index 설정
                    #selected_temp_index = st.session_state['selected_template_index']
                    if st.session_state['selected_template_name'] in template_files:
                        selected_temp_index = template_files.index(st.session_state['selected_template_name']) + 1                         
                    else:
                        selected_temp_index = 0
                    st.session_state['selected_template_index'] = selected_temp_index  
                    st.session_state['template_list_option'] = [templatelist_init_value] + template_files
                    #보고서 양식 파일 리스트
                    selected_template = st.selectbox(
                        "불러올 보고서 양식 파일 리스트", 
                        options=st.session_state['template_list_option'], 
                        index=st.session_state['selected_template_index'],
                        key="selected_template"
                    )
                    # 선택한 템플릿 불러오기
                    st.session_state['selected_template_name'] = selected_template
                    if selected_template != templatelist_init_value:
                        
                        template_data = bd.load_template_from_github(repo, branch, token, selected_template)
                        if template_data:
                            bd.apply_template_to_session_state(f"templateFiles/{selected_template}")
                            #st.success(f"{selected_template} 양식을 성공적으로 불러왔습니다.")

        with tab3:
            col1, col2, col3 = st.columns([0.21, 0.5,0.29])
            with col1:
                st.write("")
                st.markdown(
                    "<p style='font-size:14px; font-weight:bold; color:#000000;text-align:center;'>새로운 보고서명<br/>만들기</p>",
                    unsafe_allow_html=True
                )
            with col2:
                new_folder_name = st.text_input("새로 등록할 보고서명 입력", max_chars=20, key="new_folder_name", value=st.session_state['new_folder_text'])
            with col3:
                st.markdown(
                    "<p style='font-size:18px; margin-top:27px;'></p>",
                    unsafe_allow_html=True
                )
                if st.button("보고서명 등록", key="new_folder", use_container_width=True):
                    if not new_folder_name:
                        st.warning("새로 등록할 보고서명을 입력하세요.")
                    elif new_folder_name in folder_list:
                        st.warning("이미 존재합니다.")
                    else:
                        # 폴더 생성 후 목록에 추가
                        folder_created = bd.create_new_folder_in_github(st.session_state['github_repo'], new_folder_name, st.session_state['github_token'], st.session_state['github_branch'])
                        if folder_created:
                            folder_list.append(new_folder_name)  # 새 폴더를 리스트에 추가
                            #st.session_state['selected_folder_index'] = len(folder_list) + 1
                            #st.session_state['selected_template_index'] = 0
                            st.session_state['folder_list_option'] = [folderlist_init_value] + folder_list
                            st.session_state['upload_folder'] = f"uploadFiles/{new_folder_name}"
                            st.session_state['selected_folder_name'] = f"{new_folder_name}"
                            st.session_state['selected_template_name'] = templatelist_init_value
                            st.session_state['check_report']=False
                            st.session_state['check_setting']=True
                            bd.refresh_page()
                            bd.init_session_state(True)
                            st.success("새로운 보고서명 등록 성공하였습니다.")            
        #st.markdown(
            #"<hr style='border-top:1px solid #dddddd;border-bottom:0px solid #dddddd;width:100%;padding:0px;margin:0px'></hr>",
            #unsafe_allow_html=True
        #)
      
else:
    st.warning("GitHub 정보가 설정되지 않았습니다. 먼저 GitHub Token을 입력해 주세요.")


# 3 프레임
# 보고서 타이틀 보기
col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
with col1:
    st.write("")
with col2:   
    report_title = "작성할 보고서를 선택하세요."
    title_style="font-size:15px; font-weight:normal; color:#cccccc;border: 1px solid #dddddd;letter-spacing: 1px;"
    if 'selected_folder_name' in st.session_state:
        if st.session_state['selected_folder_name'] != folderlist_init_value:
            report_title = " [" + st.session_state['selected_folder_name'] + "] 보고서"
            title_style="font-size:20px; font-weight:bold; color:#000000;border: 0px solid #dddddd;letter-spacing: 4px;"
    st.markdown(
        f"<div style='text-align:center;{title_style};border-radius: 10px;width:100%;padding: 10px;margin-top:10px;margin-bottom:10px;'>{report_title}</div>",
        unsafe_allow_html=True
    )
   
with col3:
    st.write("")

# 4 프레임
# 작성 보고서 요청사항 세부타이틀
st.markdown(
    "<p style='font-size:18px; font-weight:bold; color:#007BFF;'>작성 보고서 요청사항</p>",
    unsafe_allow_html=True
)

# 5 프레임
# 파일 업로드
# 지원되는 파일 형식 리스트
supported_file_types = ['xlsx', 'pptx', 'docx', 'csv', 'png', 'jpg', 'jpeg', 'pdf', 'txt', 'log']

if github_info_loaded:
    with st.expander("⬆️ 데이터 파일 업로드", expanded=st.session_state['check_upload']):
        uploaded_files = st.file_uploader("파일을 여러 개 드래그 앤 드롭하여 업로드하세요. (최대 100MB)", accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_type = uploaded_file.name.split('.')[-1].lower()

                if file_type not in supported_file_types:
                    st.error(f"지원하지 않는 파일입니다: {uploaded_file.name}")
                    continue

                if uploaded_file.size > MAX_FILE_SIZE_BYTES:
                    st.warning(f"'{uploaded_file.name}' 파일은 {MAX_FILE_SIZE_MB}MB 제한을 초과했습니다. 파일 크기를 줄이거나 GitHub에 직접 푸시하세요.")
                else:
                    file_content = uploaded_file.read()
                    file_name = uploaded_file.name
                    #folder_name = 'uploadFiles'
                    folder_name = st.session_state.get('upload_folder', 'uploadFiles')

                    sha = bd.get_file_sha(st.session_state['github_repo'], f"{folder_name}/{file_name}", st.session_state['github_token'], branch=st.session_state['github_branch'])

                    if sha:
                        st.warning(f"'{file_name}' 파일이 이미 존재합니다. 덮어쓰시겠습니까?")
                        col1, col2 = st.columns(2)

                        with col1:
                            if st.button(f"'{file_name}' 덮어쓰기", key=f"overwrite_{file_name}"):
                                bd.upload_file_to_github(st.session_state['github_repo'], folder_name, file_name, file_content, st.session_state['github_token'], branch=st.session_state['github_branch'], sha=sha)
                                st.success(f"'{file_name}' 파일이 성공적으로 덮어쓰기 되었습니다.")
                                uploaded_files = None
                                break

                        with col2:
                            if st.button("취소", key=f"cancel_{file_name}"):
                                st.info("덮어쓰기가 취소되었습니다.")
                                uploaded_files = None
                                break
                    else:
                        bd.upload_file_to_github(st.session_state['github_repo'], folder_name, file_name, file_content, st.session_state['github_token'])
                        st.success(f"'{file_name}' 파일이 성공적으로 업로드되었습니다.")
                        uploaded_files = None
else:
    st.warning("GitHub 정보가 저장되기 전에는 파일 업로드를 할 수 없습니다. 먼저 GitHub 정보를 입력해 주세요.")

# 6 프레임
# 요청사항 갯수 및 기준일자 설정 
with st.expander("⚙️ 요청사항 및 기준일자 설정", expanded=st.session_state['check_setting']):
    col1, col2, col3 = st.columns([0.5, 0.25, 0.25])
    with col1:
        st.markdown(
            "<p style='font-size:14px; font-weight:normal; color:#444444; margin-top:35px;text-align:left;'>✔️ 작성에 필요한 요청사항 갯수를 설정해주세요.</p>",
            unsafe_allow_html=True
        )
        
    with col2:
        # 요청사항 갯수 입력 (1-9)
        num_requests = st.number_input(
            "🔢 요청사항 갯수 입력창",
            min_value=1,
            max_value=9,
            value=1,
            step=1,
            key="num_requests"
        )
    
    with col3:
        st.markdown(
            "<p style='font-size:18px; margin-top:27px;'></p>",
            unsafe_allow_html=True
        )
        if st.button("설정", key="set_requests", use_container_width=True):
            # 설정 버튼 클릭 시 요청사항 리스트 초기화 및 새로운 요청사항 갯수 설정
            st.session_state['rows'] = [
                {"제목": "", "요청": "", "파일": "", "데이터": "", "파일정보": "1"}
                for _ in range(st.session_state['num_requests'])
            ]
            st.success(f"{st.session_state['num_requests']}개의 요청사항이 설정되었습니다.")
            st.session_state['check_request']=True
            st.session_state['check_setting']=False
            bd.refresh_page()
            bd.init_session_state(True)
    col1, col2 = st.columns([0.5, 0.5])
    with col1 :
        st.markdown(
            "<hr style='border-top:1px solid #dddddd;border-bottom:0px solid #dddddd;width:100%;padding:0px;margin:0px'></hr>",
            unsafe_allow_html=True
        )      
    with col2 :
        st.markdown(
            "<hr style='border-top:1px solid #dddddd;border-bottom:0px solid #dddddd;width:100%;padding:0px;margin:0px'></hr>",
            unsafe_allow_html=True
        )
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        # 오늘 날짜 가져오기
        today = datetime.date.today()
        
        # 'report_date_str' 세션 값이 있는지 확인하고, 없으면 'YYYYMMDD' 형식으로 today 값 설정
        if 'report_date_str' not in st.session_state:
            st.session_state['report_date_str'] = today.strftime('%Y%m%d')
        
        
        # 세션에 저장된 'YYYYMMDD' 형식을 date 객체로 변환
        saved_date = today
        # 날짜 문자열을 검사하여 잘못된 형식일 때 예외 처리
        if 'report_date_str' in st.session_state and st.session_state['report_date_str']:
            try:
                # 저장된 날짜 문자열이 있으면 파싱
                saved_date = datetime.datetime.strptime(st.session_state['report_date_str'], '%Y%m%d').date()
            except ValueError:
                # 날짜 형식이 맞지 않으면 오늘 날짜로 설정
                st.warning("잘못된 날짜 형식입니다. 기본값으로 오늘 날짜를 사용합니다.")
        else:
            # 저장된 날짜가 없거나 빈 문자열일 경우 오늘 날짜로 설정
            saved_date = today
    
        report_date = st.date_input(
            "📅 보고서 기준일자 선택",
            value=saved_date,
            min_value=datetime.date(2000, 1, 1),
            max_value=today,
            key="report_date"
        )
        # 날짜를 YYYYMMDD 형식으로 변환
        # 날짜 데이터 메모리에 저장
        st.session_state['report_date_str'] = report_date.strftime("%Y%m%d")
    with col2:
        st.markdown(
            "<p style='font-size:14px; font-weight:normal; color:#444444; margin-top:35px;text-align:left;'>✔️ 보고서 저장을 위해 기준일자를 설정해주세요.</p>",
            unsafe_allow_html=True
        )

# 7 프레임임
# 요청사항 리스트
with st.expander("✍️ 요청사항 리스트", expanded=st.session_state['check_request']):
    if 'rows' not in st.session_state:
        st.session_state['rows'] = [{"제목": "", "요청": "", "파일": "", "데이터": "", "파일정보":"1"}]

    rows = st.session_state['rows']
    checked_rows = []

    for idx, row in enumerate(rows):
        with st.container():
            #col1, col2 = st.columns([0.01, 0.99]) 
            #with col1:
                #row_checked = st.checkbox("", key=f"row_checked_{idx}", value=row.get("checked", False))  # 체크박스만 추가
                #st.write("")
            #with col2:
            st.markdown(
                f"<p style='font-size:16px; font-weight:bold; color:#000000; margin-top:5px;'>{idx+1}. 요청사항</p>",
                unsafe_allow_html=True
            )
        
            row['제목'] = st.text_input(f"제목 : '{idx+1}.요청사항'의 제목을 입력해주세요.", row['제목'], key=f"title_{idx}")
            row['요청'] = st.text_area(f"요청 : '{idx+1}.요청사항'의 요청할 내용을 입력해주세요.", row['요청'], key=f"request_{idx}")
     
            file_list = ['파일을 선택하세요.']
            if st.session_state.get('github_token') and st.session_state.get('github_repo'):
                file_list += bd.get_github_files(st.session_state['github_repo'], st.session_state['github_branch'], st.session_state['github_token'])

            selected_file = st.selectbox(f"파일 선택 : '{idx+1}.요청사항'의 파일을 선택해주세요.", options=file_list, key=f"file_select_{idx}")

            if selected_file != '파일을 선택하세요.':
                st.session_state['rows'][idx]['파일'] = selected_file
           
                file_path = selected_file
                file_content = bd.get_file_from_github(
                    st.session_state["github_repo"], 
                    st.session_state["github_branch"], 
                    file_path, 
                    st.session_state["github_token"]
                )

                if file_content:
                    file_type = file_path.split('.')[-1].lower()
                    
                    # 파일 형식 검증 (지원되는 파일만 처리)
                    if file_type not in supported_file_types:
                        st.error(f"지원하지 않는 파일입니다: {file_path}")
                        row['데이터'] = ""
                    else:      
                        bd.handle_file_selection(file_path, file_content, file_type, idx)
                        
                else:
                    st.error(f"{selected_file} 파일을 GitHub에서 불러오지 못했습니다.")  
            st.text_input(f"{idx+1}.요청사항 선택한 파일", row['파일'], disabled=True, key=f"file_{idx}")
        
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
        if not st.session_state.get("openai_api_key"):
            st.error("먼저 OpenAI API 키를 입력하고 저장하세요!")
        elif not st.session_state['rows'] or all(not row["제목"] or not row["요청"] or not row["파일"] for row in st.session_state['rows']):
            st.error("요청사항의 제목, 요청, 파일을 모두 입력해야 합니다!")
        else:
            with st.spinner('요청사항과 파일 데이터을 추출 중입니다...'):
        
                # 파일 데이터 가져와서 HTML 보고서 생성
                #file_data_list = []
                html_viewer_data = ""
                for idx, row in enumerate(st.session_state['rows']):
                    file_path = st.session_state['rows'][idx]['파일']
                    file_content = bd.get_file_from_github(st.session_state["github_repo"], st.session_state["github_branch"], file_path, st.session_state["github_token"])
                    file_type = file_path.split('.')[-1].lower()
                    report_html = ""
                    if file_content:
                        if file_type == 'xlsx':
                            selected_sheets = bd.parse_sheet_selection(row['파일정보'], len(openpyxl.load_workbook(file_content).sheetnames))
                            file_data_dict = bd.extract_sheets_from_excel(file_content, selected_sheets)
                            if file_data_dict is not None:
                                # 제목 입력 값 가져오기
                                report_html +=  f"<h3>{idx + 1}. {row['제목']}</h3>\n"
                                for sheet_name, df in file_data_dict.items():
                                    wb = openpyxl.load_workbook(file_content)
                                    ws = wb[sheet_name]
                                    html_data = bd.convert_df_to_html_with_styles_and_merging(ws, df)
                                    report_html += f"<div style='text-indent: 20px;'>{html_data}</div>\n"
    
                        else:
                            file_data = bd.extract_data_from_file(file_content, file_type)
                            report_html += f"<h3>{idx + 1}. {row['제목']}</h3>\n<p>{file_data}</p>"
                        if idx > 0 :
                            report_html += "<p/>"
                        html_viewer_data += report_html    
                        #file_data_list.append(row['데이터'])
                    st.session_state['html_report'] = html_viewer_data
                time.sleep(1)  # 예를 들어, 5초 동안 로딩 상태 유지

            with st.spinner('결과 보고서 작성 중입니다...'):
                # LLM 함수 호출
                titles = [row['제목'] for row in st.session_state['rows']]
                requests = [row['요청'] for row in st.session_state['rows']]
        
                responses = bd.run_llm_with_file_and_prompt(
                    st.session_state["openai_api_key"], 
                    titles, 
                    requests, 
                    st.session_state['html_report']
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
            #st.text_area(f"응답 {idx+1}:", value=response, height=300)

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
                
                folder_name = st.session_state['selected_folder_name']
                report_date_str = st.session_state.get('report_date_str', datetime.datetime.now().strftime('%Y%m%d'))
                
                # save_html_response 함수를 사용하여 HTML 파일 저장
                file_name, temp_file_path = bd.save_html_response(html_result_value, folder_name, report_date_str)

                # 파일 저장 경로 (reportFiles/{폴더명}/{일자})
                github_folder = f"reportFiles/{folder_name}/{report_date_str}"

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
          if st.button("🗃️ 보고서 양식 저장", key="save_template", use_container_width=True):
               st.session_state['check_result'] = True
               st.session_state['check_report'] = False
               st.session_state['check_upload'] = False
               st.session_state['check_setting'] = False
               st.session_state['check_request'] = False
               bd.save_template_to_json()


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
