import streamlit as st
from googleapiclient.discovery import build
import pandas as pd

st.set_page_config(page_title="Youtuber Analysis", page_icon="📊", layout="wide")

api_key = st.secrets["YOUTUBE_API_KEY"]
youtube = build('youtube', 'v3', developerKey=api_key)

st.title("📊 유튜버 채널 영상 분석")

channel_name = st.text_input("분석할 유튜버 이름(채널명)을 입력하세요:", placeholder="예: 슈카월드")

if channel_name:
    # 1. 채널 검색을 통해 Channel ID 가져오기
    channel_search = youtube.search().list(
        q=channel_name,
        type='channel',
        part='snippet',
        maxResults=1
    ).execute()
    
    if not channel_search.get('items'):
        st.warning("해당 이름의 채널을 찾을 수 없습니다.")
        st.stop()
        
    channel_id = channel_search['items'][0]['id']['channelId']
    channel_title = channel_search['items'][0]['snippet']['title']
    st.success(f"📢 **{channel_title}** 채널의 데이터를 분석합니다.")
    
    # 2. 해당 채널의 최신 영상들 가져오기
    video_search = youtube.search().list(
        channelId=channel_id,
        part='snippet',
        maxResults=30, # 분석할 샘플 영상 수
        order='date',
        type='video'
    ).execute()
    
    video_ids = [item['id']['videoId'] for item in video_search.get('items', [])]
    
    if video_ids:
        # 3. 영상별 상세 통계(조회수, 좋아요 등) 가져오기
        stats_response = youtube.videos().list(
            id=','.join(video_ids),
            part='snippet,statistics'
        ).execute()
        
        video_data = []
        for item in stats_response.get('items', []):
            snippet = item['snippet']
            stats = item['statistics']
            
            # 일부 영상은 좋아요나 댓글이 비공개일 수 있으므로 예외 처리
            video_data.append({
                "Title": snippet['title'],
                "Link": f"https://www.youtube.com/watch?v={item['id']}",
                "Views": int(stats.get('viewCount', 0)),
                "Likes": int(stats.get('likeCount', 0)),
                "Comments": int(stats.get('commentCount', 0)),
                "Published At": snippet['publishedAt'],
                "Thumbnail": snippet['thumbnails']['high']['url']
            })
            
        df = pd.DataFrame(video_data)
        
        # 4. 정렬 카테고리 선택 UI
        category = st.radio(
            "📈 정렬 기준을 선택하세요:",
            ("가장 반응이 좋은 영상 (댓글 많은 순)", "가장 조회수가 높은 영상", "가장 좋아요가 많은 영상")
        )
        
        if category == "가장 반응이 좋은 영상 (댓글 많은 순)":
            df_sorted = df.sort_values(by="Comments", ascending=False)
        elif category == "가장 조회수가 높은 영상":
            df_sorted = df.sort_values(by="Views", ascending=False)
        elif category == "가장 좋아요가 많은 영상":
            df_sorted = df.sort_values(by="Likes", ascending=False)
            
        # 5. 정렬 결과 출력
        st.write(f"### 🏆 {category} 결과 (Top 5)")
        
        for i in range(min(5, len(df_sorted))):
            row = df_sorted.iloc[i]
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(row['Thumbnail'], use_container_width=True)
            with col2:
                st.markdown(f"#### [{row['Title']}]({row['Link']})")
                st.write(f"👁️ 조회수: {row['Views']:,}회 | ❤️ 좋아요: {row['Likes']:,}개 | 💬 댓글: {row['Comments']:,}개")
                st.write(f"📅 업로드일: {row['Published At'][:10]}")
                with st.expander("▶️ 여기서 바로 보기"):
                    st.video(row['Link'])
                st.write("---")
