# # app.py

# import streamlit as st
# import asyncio
# from smart_scraper_main import webscraper
# from IPython.display import Image as IPImage
# import pandas as pd
# from tabulate import tabulate

# st.set_page_config(page_title="Smart Web Scraper", layout="wide")

# st.title("🧠 Smart Web Scraper with LLM Extraction")
# st.markdown("Enter a URL to scrape and extract structured content using OpenAI.")

# url = st.text_input("🌐 Enter URL to scrape", value="https://www.bbc.com/news")


# default_instructions = f"""
# Extract the main articles displayed on the homepage '{url}'.
# Focus on items that look like news posts or blog entries.
# Provide the title, the full article URL, the main image URL, and a short excerpt for each.
# """
# instructions = st.text_area("📋 Extraction Instructions", value=default_instructions, height=150)

# if st.button("🚀 Run Scraper"):
#     with st.spinner("Scraping and processing with LLM..."):
#         result, screenshot = asyncio.run(webscraper(url, instructions))

#     if screenshot:
#         st.image(screenshot, caption="Captured Screenshot", use_column_width=True)

#     if result and result.articles:
#         df = pd.DataFrame([article.model_dump() for article in result.articles])
#         st.dataframe(df)
#     else:
#         st.warning("No articles extracted.")






# app.py

import streamlit as st
import asyncio
from smart_scraper_main import webscraper
import pandas as pd
from tabulate import tabulate

st.set_page_config(page_title="Smart Product Scraper", layout="wide")

st.title("🧠 Smart Product Scraper with LLM Extraction")
st.markdown("""
Enter a product URL to scrape and extract structured product information using OpenAI.
The scraper will extract detailed product information including title, price, images, and specifications.
""")

url = st.text_input("🌐 Enter URL to scrape", value="https://en.zalando.de/pepe-jeans-shirt-dress-mousse-white-pe121c0z9-a11.html")

default_instructions = f"""
Extract detailed product information from the page '{url}'.
For the product, return:
1. title (product name)
2. productUrl (full product URL)
3. productCode (unique product code/SKU)
4. mainImage (main product image URL)
5. images (list of all product image URLs)
6. mainColor (main product color)
7. colors (list of all available colors)
8. description (detailed product description)
9. material (product material/fabric information)
10. price (product price as float)
11. currency (price currency, e.g., EUR, USD)
12. sizes (list of available sizes)
13. details (list of additional product specifications)

IMPORTANT:
- Return null for any fields where information is not found
- Return empty lists [] for any list fields with no items
- Ensure all URLs are complete and absolute
- Convert prices to float values
"""

instructions = st.text_area("📋 Extraction Instructions", value=default_instructions, height=200)

if st.button("🚀 Run Scraper"):
    with st.spinner("Scraping and processing with LLM..."):
        result = asyncio.run(webscraper(url, instructions))

    if result:
        st.success(f"✅ Successfully extracted {len(result)} products")
        
        # Convert products to DataFrame
        df = pd.DataFrame([product.model_dump() for product in result])
        
        # Display the DataFrame with all columns
        st.dataframe(df, use_container_width=True)
        
        # Add download button for the data
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Product Data",
            csv,
            "products.csv",
            "text/csv",
            key='download-csv'
        )
    else:
        st.warning("❌ No products were extracted. Please check the URL and try again.")
