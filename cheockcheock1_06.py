import streamlit as st
import pandas as pd
import os

from datetime import datetime

import backend as bd





# Frontend 기능 구현 시작 ---

# GitHub 정보가 있는지 확인하고 파일 업로드 객체를 출력
github_info_loaded = bd.load_env_info()

# 1 프레임
# 보고서 타이틀
col1, col2 = st.columns([0.55,0.45])
with col1:
    st.markdown(
        "<p style='font-size:25px; font-weight:bold; color:#000000;'>사용자 만족도 평가 🏆</p>",
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        "<div style='text-align:right;width:100%;'><p style='font-size:15px; font-weight:normal; color:#aaaaaa;margin-top:10px;'>by <b style='font-size:16px;color:#0099FF'>CheokCeock</b><b style='font-size:22px;color:#009999'>1</b> <b style='font-size:14px;'>prototype v.01</b></p></div>",
        unsafe_allow_html=True
    )

if github_info_loaded:
    with st.expander("✏️ 만족도 평가하기", expanded=True):
        col1, col2 = st.columns([0.21, 0.79])
        with col1:
            st.write("")
            st.write("")
            st.markdown(
                "<p style='font-size:14px; font-weight:bold; color:#000000;text-align:center;'>닉네임 또는 이름</p>",
                unsafe_allow_html=True
            )
        with col2:
            nickname = st.text_input("닉네임 또는 이름을 입력하세요:")
        st.markdown(
            "<hr style='border-top:1px solid #dddddd;border-bottom:0px solid #dddddd;width:100%;padding:0px;margin:0px'></hr>",
            unsafe_allow_html=True
        )    
        # 별점 선택 (슬라이더 사용)
        score = st.slider("별점 선택 (1~5, 0.5 단위):", 0.5, 5.0, 1.0)
        # score에 따라 이미지 설정
        star_images = bd.get_star_images(score)
        
        # 별 이미지를 표시할 5개의 열 생성
        col1, col2, col3, col4, col5 = st.columns([0.2, 0.2, 0.2, 0.2, 0.2])
        
        # 각 열에 맞는 별 이미지 출력
        with col1:  # score 1점 별
            st.image(star_images[0], width=100)
        with col2:  # score 2점 별
            st.image(star_images[1], width=100)
        with col3:  # score 3점 별
            st.image(star_images[2], width=100)
        with col4:  # score 4점 별
            st.image(star_images[3], width=100)
        with col5:  # score 5점 별
            st.image(star_images[4], width=100)
   

    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
    with col1:
        st.write("")
    with col2:
        # 평가 버튼
        if st.button("🎯 평가하기", key="appraisal", use_container_width=True):
            if nickname and score:
                file_path = "satisfaction/appraisal.csv"
                bd.add_to_csv(nickname, score, st.session_state['github_token'], st.session_state['github_repo'], st.session_state['github_branch'], file_path)
                st.success(f"{nickname}님의 평가가 성공적으로 등록되었습니다!")
            else:
                st.error("닉네임/이름과 별 개수 선택은 필수입니다.")
    with col3:
        st.write("")
            
else:
    st.warning("GitHub 정보가 설정되지 않았습니다. 먼저 GitHub Token을 입력해 주세요.")








    

