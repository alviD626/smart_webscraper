# app.py

import streamlit as st
import asyncio
from smart_scraper_main import webscraper
from IPython.display import Image as IPImage
import pandas as pd
from tabulate import tabulate

st.set_page_config(page_title="Smart Web Scraper", layout="wide")

st.title("🧠 Smart Web Scraper with LLM Extraction")
st.markdown("Enter a URL to scrape and extract structured content using OpenAI.")

url = st.text_input("🌐 Enter URL to scrape", value="https://www.bbc.com/news")


default_instructions = f"""
Extract the main articles displayed on the homepage '{url}'.
Focus on items that look like news posts or blog entries.
Provide the title, the full article URL, the main image URL, and a short excerpt for each.
"""
instructions = st.text_area("📋 Extraction Instructions", value=default_instructions, height=150)

if st.button("🚀 Run Scraper"):
    with st.spinner("Scraping and processing with LLM..."):
        result, screenshot = asyncio.run(webscraper(url, instructions))

    if screenshot:
        st.image(screenshot, caption="Captured Screenshot", use_column_width=True)

    if result and result.articles:
        df = pd.DataFrame([article.model_dump() for article in result.articles])
        st.dataframe(df)
    else:
        st.warning("No articles extracted.")
