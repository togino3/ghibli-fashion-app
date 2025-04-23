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
            age = st.slider("年齢", 10, 80, 25)
            height = st.number_input("身長(cm)", min_value=100, max_value=250, value=170)
            weight = st.number_input("体重(kg)", min_value=30, max_value=150, value=60)
        with col2:
            body_shape = st.selectbox("体型", ["スリム", "マッチョ", "ガッチリ"])
            color = st.text_input("好きな色")
            concept = st.text_input("ファッションテーマ (夏系, ギャル系, ヨーロッパ系 etc)")
            submitted = st.form_submit_button("アニメ風コーディネート生成")

    if submitted and uploaded_image:
        prompt = (
            f"Create a nostalgic 1990s Japanese anime-style fashion illustration. "
            f"The character lives in {country}, is a {age}-year-old {gender} with a {body_shape} body type, "
            f"height {height}cm, weight {weight}kg. Favorite color is {color}. "
            f"Fashion theme: {concept}. Use soft watercolor tones, retro styling, emotional and dreamy atmosphere, "
            f"background with natural or urban Japanese setting from the 1990s."
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
                "height": height,
                "weight": weight,
                "color": color,
                "concept": concept,
                "timestamp": datetime.now().isoformat()
            }
            save_favorite(new_favorite)
            st.success("お気に入りに登録しました！")
