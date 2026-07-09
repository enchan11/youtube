import streamlit as st
from googleapiclient.discovery import build
import yt_dlp

st.set_page_config(page_title="Search & Watch", page_icon="📺", layout="wide")

# API 키 불러오기
api_key = st.secrets["YOUTUBE_API_KEY"]
youtube = build('youtube', 'v3', developerKey=api_key)

# 유튜브 실제 스트리밍 MP4 주소를 추출하는 함수
def get_raw_video_url(youtube_url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',  # MP4 포맷 중 가장 좋은 화질
        'quiet': True,
        'no_warnings': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(youtube_url, download=False)
            return info['url']  # 실제 미디어 소스 URL 리턴
        except Exception as e:
            return None

st.title("📺 순수 자체 플레이어 영상 시청")

search_query = st.text_input("검색어를 입력하세요:", placeholder="예: 플레이리스트, 테크 리뷰 등")

if search_query:
    search_response = youtube.search().list(
        q=search_query,
        part='snippet',
        maxResults=12,
        type='video'
    ).execute()
    
    cols = st.columns(3)
    
    for idx, item in enumerate(search_response.get('items', [])):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        thumbnail_url = item['snippet']['thumbnails']['high']['url']
        channel_title = item['snippet']['channelTitle']
        youtube_link = f"https://www.youtube.com/watch?v={video_id}"
        
        with cols[idx % 3]:
            st.image(thumbnail_url, use_container_width=True)
            st.subheader(title[:40] + "..." if len(title) > 40 else title)
            st.caption(f"채널명: {channel_title}")
            
            # 모달을 열었을 때 주소를 추출하고 재생
            with st.expander("▶️ 자체 플레이어로 시청"):
                # 사용자 경험을 위해 로딩 스피너 작동
                with st.spinner("영상을 불러오는 중..."):
                    raw_video_url = get_raw_video_url(youtube_link)
                
                if raw_video_url:
                    # 유튜브 UI가 없는 브라우저 기본 순수 비디오 태그로 재생됩니다.
                    st.video(raw_video_url)
                else:
                    st.error("영상을 추출할 수 없습니다. (저작권 또는 제한된 영상)")
