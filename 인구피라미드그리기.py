import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# ✅ 페이지 탭 제목 수정
st.set_page_config(page_title="인구 피라미드 그리기", layout="wide")

# ✅ 메인 제목
st.title("인구 피라미드 그리기")

# ✅ 간단 안내 문구 (간격 줄이기 + 강조 문구)
st.write("자동으로 인구 피라미드를 그려드릴게요.")
st.markdown("**<span style='color:red'>인구 피라미드의 제목</span>을 입력해 주세요!**", unsafe_allow_html=True)

# ✅ 사용자 입력창
title_prefix = st.text_input("", "2025년 포항시")
custom_title = f"{title_prefix} 인구 피라미드"

# ✅ 파일 업로드 (설명 제거한 간단 버전)
uploaded_file = st.file_uploader(" ", type=["xlsx"])  # 라벨 비움

if uploaded_file:
    data = pd.read_excel(uploaded_file)

    # 데이터 전처리
    data['남자'] = data['남자'].astype(str).str.replace(',', '').astype(int)
    data['여자'] = data['여자'].astype(str).str.replace(',', '').astype(int)

    age_sgmt = data['연령대']
    male_data = data['남자'] * -1
    female_data = data['여자']

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=male_data,
        y=age_sgmt,
        name='남성',
        orientation='h',
        text=male_data.abs().apply(lambda x: f"{x:,}명"),
        hovertext=[f"남성 {age}: {val:,}명" for age, val in zip(age_sgmt, male_data.abs())],
        hoverinfo='text',
        marker=dict(color='#4D96FF')
    ))

    fig.add_trace(go.Bar(
        x=female_data,
        y=age_sgmt,
        name='여성',
        orientation='h',
        text=female_data.apply(lambda x: f"{x:,}명"),
        hovertext=[f"여성 {age}: {val:,}명" for age, val in zip(age_sgmt, female_data)],
        hoverinfo='text',
        marker=dict(color='#FF6B6B')
    ))

    x_max = int(max(male_data.abs().max(), female_data.max(), 3000000))
    tick_vals = list(range(-x_max, x_max + 1, 1000000))
    tick_texts = [f'{abs(val)//10000}백만' if val != 0 else '0' for val in tick_vals]

    fig.update_layout(
        title=custom_title,
        title_font_size=22,
        title_x=0.5,
        margin=dict(t=80),
        barmode='overlay',
        bargap=0.0,
        bargroupgap=0,
        xaxis=dict(
            tickvals=tick_vals,
            ticktext=tick_texts,
            title='인구 수(백만명)',
            title_font_size=14
        )
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    # ✅ 스마일 이모지로 안내
    st.markdown("😀 인구데이터.xlsx 파일을 업로드해주세요.")
