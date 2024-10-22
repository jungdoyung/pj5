import streamlit as st
import importlib
import os
import backend as bd
# 메뉴명 리스트
sub_menu_list=['📚업무 보고서 자동 완성', '📈보고서 비교분석 자동 완성', '🎧음성 파일 보고서 완성', '⚡Quickly 키워드 보고서 완성','📋결과 보고서 현황', '👥프로젝트 및 팀 소개', '🏆사용자 만족도 평가']

if 'selected_menu01_index' not in st.session_state:
    st.session_state['selected_menu01_index'] =0
     
# 파일명 리스트
file_list=["cheockcheock1_01.py","cheockcheock1_02.py","cheockcheock1_03.py","cheockcheock1_04.py","cheockcheock1_05.py","cheockcheock1_team.py","cheockcheock1_06.py"]


# 사이드바에 타이트 추가 : 척척하나
st.sidebar.markdown(
    """
    <div style='background-color:#E7EAF1;text-align:center;width:100%;padding-bottom:6px;border-radius:8px;'>
    <b style='font-size:22px;color:#0099FF;font-style:italic;'>CheockCheock</b><b style='font-size:30px;color:#009999;'>☝️</b>
    </div>
    """,
    unsafe_allow_html=True
)

# 메뉴 리스트
selected_menu = st.sidebar.selectbox("메뉴 선택하세요.", sub_menu_list, index=st.session_state['selected_menu01_index'])
if selected_menu:
    # 선택한 option Index
    idx  = sub_menu_list.index(selected_menu)
    # 선택한 Index을 session에 저장
    st.session_state['selected_menu01_index'] = idx
    # 파일명 가져오기
    selected_file = file_list[idx]
    # 선택한 파일 코드 실행
    bd.exec_page(selected_file)
else:
    st.session_state['selected_menu01_index'] = 0
    
# 사이드바 하단 문구
st.sidebar.markdown(
    """
    <div style='font-size:12px; font-weight:normal; color:#999999;text-align:center;width:90%;border-top:0px dotted #cccccc;margin-left:5%;margin-right:5%'>ⓒ LepoLab. Challenger_5 Team</div>
    """,
    unsafe_allow_html=True
)
