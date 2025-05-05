# # smart_scraper_main.py

# from utils.browser_agent import WebScraperAgent
# from utils.llm_extractor import process_with_llm
# from schemas.article_schema import EuronArticleList
# import asyncio
# from IPython.display import Image as IPImage, display
# import pandas as pd
# from tabulate import tabulate


# async def webscraper(target_url, instructions):
#     result = None
#     screenshot_bytes = None
#     scraper = WebScraperAgent()

#     try:
#         await scraper.init_browser()
#         html_content = await scraper.scrape_content(target_url)

#         if html_content:
#             screenshot_bytes = await scraper.screenshot_buffer()
#             result = await process_with_llm(html_content, instructions, truncate=True)

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         await scraper.close()

#     return result, screenshot_bytes


# async def main():
#     target_url = "https://www.bbc.com/news"


#     instructions = f"""
#     Extract featured or promoted courses shown on the homepage '{target_url}'.
#     For each course, return:
#     1. title (course name),
#     2. articleUrl (link to the course),
#     3. imageUrl (thumbnail),
#     4. excerpt (short course description or rating).
#     """



#     print("--- Running Web Scraper ---")
#     result, screenshot = await webscraper(target_url, instructions)
#     print("\n--- Scraping Finished ---")

#     if screenshot:
#         try:
#             display(IPImage(data=screenshot))
#         except Exception:
#             with open("euron_screenshot.png", "wb") as f:
#                 f.write(screenshot)
#             print("Screenshot saved to euron_screenshot.png")

#     if result and result.articles:
#         print("\n--- Extracted Articles ---")
#         df = pd.DataFrame([article.model_dump() for article in result.articles])
#         print(tabulate(df, headers='keys', tablefmt='grid'))
#     elif result:
#         print("\n--- No articles extracted ---")
#     else:
#         print("\n--- No results ---")


# if __name__ == "__main__":
#     try:
#         loop = asyncio.get_running_loop()
#         if loop.is_running():
#             print("Async loop running. Use 'await main()' in notebook.")
#         else:
#             asyncio.run(main())
#     except RuntimeError:
#         asyncio.run(main())




# smart_scraper_main.py

from utils.browser_agent import WebScraperAgent
from utils.llm_extractor import process_with_llm
from schemas.article_schema import EuronProduct
import asyncio
import pandas as pd
from tabulate import tabulate
from typing import List, Optional

async def webscraper(url: str, instructions: str) -> List[EuronProduct]:
    """
    Scrape a product URL and extract product information.
    Returns a list of EuronProduct objects.
    """
    agent = WebScraperAgent()
    try:
        # Initialize browser and get HTML content
        print(f"🔍 Scraping product page: {url}")
        html = await agent.scrape_content(url)
        
        if not html:
            print("❌ Failed to get content from the product page")
            return []
            
        # Process the product with LLM
        product = await process_with_llm(html, instructions, truncate=True)
        if product:
            print(f"✅ Successfully processed product")
            return [product]
        else:
            print("❌ Failed to process product")
            return []
        
    except Exception as e:
        print(f"❌ Error in webscraper: {str(e)}")
        return []
        
    finally:
        await agent.close()

async def main():
    target_url = "https://en.zalando.de/pepe-jeans-shirt-dress-mousse-white-pe121c0z9-a11.html"

    instructions = f"""
    Extract detailed product information from the page '{target_url}'.
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

    print("--- Running Product Scraper ---")
    result = await webscraper(target_url, instructions)
    print("\n--- Scraping Finished ---")

    if result:
        print("\n--- Extracted Product ---")
        df = pd.DataFrame([product.model_dump() for product in result])
        print(tabulate(df, headers='keys', tablefmt='grid'))
    else:
        print("\n--- No product extracted ---")

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            print("Async loop running. Use 'await main()' in notebook.")
        else:
            asyncio.run(main())
    except RuntimeError:
        asyncio.run(main())
