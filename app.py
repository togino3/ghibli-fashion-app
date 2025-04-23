import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO
import json
import os
from datetime import datetime
import uuid

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Setup Streamlit page
st.set_page_config(page_title="🌟 RetailNext Portal", layout="wide")
st.title("🌟 AI Animation Coordinator")

# JSON data file for saving favorites
DATA_FILE = "favorites.json"
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        st.session_state.favorites = json.load(f)

def save_favorite(entry):
    st.session_state.favorites.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.favorites, f, indent=2)

# Tabs for functionality
tabs = st.tabs(["生成", "ポータル"])

# --- Tab 1: Generate Anime-style Fashion ---
with tabs[0]:
    st.subheader("📷 写真と情報をもとにコーディネートを生成")
    with st.form("user_input_form"):
        col1, col2 = st.columns(2)
        with col1:
            uploaded_image = st.file_uploader("自分の写真をアップロード", type=["jpg", "jpeg", "png"])
            country = st.text_input("住んでいる国")
            gender = st.selectbox("性別", ["男", "女", "その他"])
            age = st.slider("年齢(1〜100)", min_value=1, max_value=100, value=25)
        with col2:
            body_shape = st.selectbox("体型", ["スリム", "マッチョ", "ガッチリ"])
            color = st.text_input("好きな色")
            concept = st.text_input("ファッションテーマ (例: 夏系, ストリート, キャンプ etc)")
            anime_style = st.selectbox(
                "アニメスタイル",
                ["日本レトロ", "ディズニー", "アメリカンコミック", "CG"]
            )
            submitted = st.form_submit_button("アニメ風コーディネート生成")

    if submitted and uploaded_image:
        prompt = (
            f"Please create a fashion coordination image that fits the following customer's preferences. "
            f"The customer lives in {country}, is a {age}-year-old {gender} with a {body_shape} body type. "
            f"Favorite color is {color}, and the fashion theme is {concept}. "
            f"Use an {anime_style} animation style. Include stylish outfit design, full-body fashion, artistic composition, and a harmonious background."
        )

        with st.spinner("AIコーディネート生成中..."):
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                n=1
            )
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            ghibli_image = Image.open(BytesIO(image_response.content))

        st.image(ghibli_image, caption="生成されたアニメ風コーディネート", use_column_width=True)

        if st.button("❤️ お気に入りとして登録"):
            new_favorite = {
                "id": str(uuid.uuid4()),
                "image_url": image_url,
                "country": country,
                "gender": gender,
                "age": age,
                "body_shape": body_shape,
                "color": color,
                "concept": concept,
                "anime_style": anime_style,
                "timestamp": datetime.now().isoformat()
            }
            save_favorite(new_favorite)
            st.success("お気に入りに登録しました！")
