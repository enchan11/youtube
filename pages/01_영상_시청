import streamlit as st
from googleapiclient.discovery import build

st.set_page_config(page_title="Search & Watch", page_icon="📺", layout="wide")

# API 키 불러오기
try:
    api_key = st.secrets["YOUTUBE_API_KEY"]
except KeyError:
    st.error("⚠️ .streamlit/secrets.toml 파일에 'YOUTUBE_API_KEY'를 설정해주세요.")
    st.stop()

youtube = build('youtube', 'v3', developerKey=api_key)

st.title("📺 영상 검색 및 시청")

search_query = st.text_input("검색어를 입력하세요:", placeholder="예: 플레이리스트, 테크 리뷰 등")

if search_query:
    # 유튜브 검색 API 호출
    search_response = youtube.search().list(
        q=search_query,
        part='snippet',
        maxResults=12,
        type='video'
    ).execute()
    
    # 그리드 레이아웃 구성 (3열)
    cols = st.columns(3)
    
    for idx, item in enumerate(search_response.get('items', [])):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        thumbnail_url = item['snippet']['thumbnails']['high']['url']
        channel_title = item['snippet']['channelTitle']
        
        with cols[idx % 3]:
            st.image(thumbnail_url, use_container_width=True)
            st.subheader(title[:40] + "..." if len(title) > 40 else title)
            st.caption(f"채널명: {channel_title}")
            
            # 모달(Expander)을 활용한 즉시 시청 기능
            with st.expander("▶️ 영상 시청하기"):
                st.video(f"https://www.youtube.com/watch?v={video_id}")
