import streamlit as st

st.set_page_config(
    page_title="NextTube",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 NextTube: YouTube Alternative Client")
st.markdown("""
YouTube Data API를 활용한 맞춤형 유튜브 대체 플랫폼에 오신 것을 환영합니다!
왼쪽 사이드바의 메뉴를 이용해 원하는 기능을 선택하세요.

* **📺 Watch & Search**: 유튜브 영상을 광고 없이 깔끔하게 검색하고 즉시 시청할 수 있습니다.
* **📊 Youtuber Analysis**: 특정 유튜버를 검색하여 가장 반응이 좋은 영상, 급상승 영상, 좋아요가 많은 영상 등을 분석합니다.
""")
