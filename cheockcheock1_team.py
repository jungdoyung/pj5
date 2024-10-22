import streamlit as st
import importlib
import os
import backend as bd

# 1 프레임
# 보고서 타이틀
col1, col2 = st.columns([0.55, 0.45])
with col1:
    st.markdown(
        "<p style='font-size:25px; font-weight:bold; color:#000000;'>✨ 프로젝트 및 팀원소개 ✨</p>",
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        "<div style='text-align:right;width:100%;'><p style='font-size:13px; font-weight:normal; color:#aaaaaa; margin-top:10px;'>by <b style='font-size:16px;color:#0099FF'>CheokCeock</b><b style='font-size:22px;color:#009999'>1</b> <b style='font-size:14px;'>prototype v.01</b></p></div>",
        unsafe_allow_html=True
    )

st.markdown("<hr style='border-top:1px solid #dddddd;'>", unsafe_allow_html=True)
st.markdown("## 프로젝트 소개")    
with st.container():
    st.image("checkcheck.jpg", width=150)
    st.markdown("### CheokCeock1")
    st.markdown("""
        **추진 배경**  
        **매일 반복적이고 고정된 형식의 업무 처리 및 보고서 작성 수행을 보다 효율적으로 자동화하여 시간 절약 및 정확도를 개선 하기 위함.**  
    """)


# 팀원 소개 섹션
st.markdown("<hr style='border-top:1px solid #dddddd;'>", unsafe_allow_html=True)
st.markdown("## 팀원 소개")

# 팀원 1 소개
with st.container():
#        st.image("team_member1.jpg", width=150)  # 팀원 1의 이미지 경로
    st.markdown("### 고종현 과장(인프라보안팀)")
    st.markdown("""
        **역할**: 팀 리더👑  
        **소개**: 고종현 팀장은 풍부한 경험과 탁월한 리더십으로 팀을 이끌었고, 그의 전략적 사고와 문제 해결 능력은 프로젝트의 성공적으로 이끌었습니다.  
    """)
#        st.markdown("<hr style='border-top:1px solid #dddddd;'>", unsafe_allow_html=True)  # 구분선

# 팀원 2 소개
with st.container():
#        st.image("team_member2.jpg", width=150)
    st.markdown("### 정도용 차장(내부통제지원팀)")
    st.markdown("""
        **역할**: 데이터 분석가👨‍💻  
        **소개**: 정도용 팀원의 심도 있는 데이터 분석 능력은 프로젝트의 핵심 인사이트를 도출하는 데 큰 도움이 되었습니다.  
    """)
#        st.markdown("<hr style='border-top:1px solid #dddddd;'>", unsafe_allow_html=True)  # 구분선    
    
# 팀원 3 소개
with st.container():
#        st.image("team_member3.jpg", width=150)  # 팀원 3의 이미지 경로
    st.markdown("### 김상영 대리(외환팀)")
    st.markdown("""
        **역할**: 프론트엔드 개발자👨‍💻  
        **소개**: 김상영 팀원의 혁신적인 아이디어와 효율적인 개발 능력은 프로젝트의 성공적인 개발에 기여했습니다.  
    """)
#        st.markdown("<hr style='border-top:1px solid #dddddd;'>", unsafe_allow_html=True)  # 구분선

# 팀원 4 소개
with st.container():
#        st.image("team_member4.jpg", width=150)  # 팀원 4의 이미지 경로
    st.markdown("### 배근일 대리(인프라팀)")
    st.markdown("""
        **역할**: 백엔드 개발자👨‍💻  
        **소개**: 배근일 팀원의 서버 및 데이터베이스 관리 능력은 프로젝트의 백엔드 구성에 큰 도움이 되었습니다.        
    """)
    st.markdown("<hr style='border-top:1px solid #dddddd;'>", unsafe_allow_html=True)  # 구분선
