# # utils/llm_extractor.py

# import os
# import json
# from openai import OpenAI
# from dotenv import load_dotenv
# from schemas.article_schema import EuronArticleList

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# async def process_with_llm(html, instructions, truncate=False):
#     if not html:
#         return None

#     max_len = 150000
#     content_to_send = html[:max_len] if truncate and len(html) > max_len else html

#     try:
#         completion = client.chat.completions.create(
#             model="gpt-4o-mini-2024-07-18",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": f"""
#                     You are an expert web scraping agent. Your task is to extract:
#                     1. title
#                     2. articleUrl (absolute URL)
#                     3. imageUrl
#                     4. excerpt
#                     from this page's HTML.

#                     Instructions:
#                     {instructions}

#                     Return ONLY a JSON object matching the expected schema.
#                     """
#                 },
#                 {"role": "user", "content": content_to_send}
#             ],
#             temperature=0.1,
#             response_format={"type": "json_object"}
#         )

#         response_content = completion.choices[0].message.content
#         return EuronArticleList.model_validate_json(response_content)

#     except Exception as e:
#         print(f"❌ Error in LLM extraction: {e}")
#         return None



# utils/llm_extractor.py

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from schemas.article_schema import EuronProduct

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def process_with_llm(html, instructions, truncate=False):
    if not html:
        return None

    max_len = 150000
    content_to_send = html[:max_len] if truncate and len(html) > max_len else html

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {
                    "role": "system",
                    "content": f"""
                    You are an expert web scraping agent. Your task is to extract product information from this page's HTML.
                    IMPORTANT: Only extract information that is explicitly present in the HTML. Do not make assumptions or generate content.

                    For each field:
                    - If the information is not found in the HTML, set it to null (for single values) or empty list [] (for lists)
                    - Do not generate or guess any missing information
                    - Only return data that you can clearly see in the HTML
                    - For lists (images, colors, sizes, details), return an empty list [] if no items are found
                    - For prices, ensure they are returned as float values
                    - For URLs, ensure they are complete and absolute

                    Return a JSON object with this structure:
                    {{
                        "title": "product name" or null if not found,
                        "productUrl": "full product URL" or null if not found,
                        "productCode": "unique product code/SKU" or null if not found,
                        "mainImage": "main product image URL" or null if not found,
                        "images": ["list of all product image URLs"] or [] if none found,
                        "mainColor": "main product color" or null if not found,
                        "colors": ["list of all available colors"] or [] if none found,
                        "description": "detailed product description" or null if not found,
                        "material": "product material/fabric information" or null if not found,
                        "price": price_as_float or null if not found,
                        "currency": "price currency (e.g., EUR, USD)" or null if not found,
                        "sizes": ["list of available sizes"] or [] if none found,
                        "details": ["list of additional product specifications"] or [] if none found
                    }}

                    Instructions:
                    {instructions}

                    Remember: 
                    - If you cannot find a piece of information in the HTML, set it to null or empty list
                    - Do not make up any data
                    - Ensure all URLs are complete and absolute
                    - Convert prices to float values
                    - Return empty lists [] for any list fields that have no items
                    """
                },
                {"role": "user", "content": content_to_send}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )

        response_content = completion.choices[0].message.content
        return EuronProduct.model_validate_json(response_content)

    except Exception as e:
        print(f"❌ Error in LLM extraction: {e}")
        return None