# smart_scraper_main.py

from utils.browser_agent import WebScraperAgent
from utils.llm_extractor import process_with_llm
from schemas.article_schema import EuronArticleList
import asyncio
from IPython.display import Image as IPImage, display
import pandas as pd
from tabulate import tabulate


async def webscraper(target_url, instructions):
    result = None
    screenshot_bytes = None
    scraper = WebScraperAgent()

    try:
        await scraper.init_browser()
        html_content = await scraper.scrape_content(target_url)

        if html_content:
            screenshot_bytes = await scraper.screenshot_buffer()
            result = await process_with_llm(html_content, instructions, truncate=True)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await scraper.close()

    return result, screenshot_bytes


async def main():
    target_url = "https://www.bbc.com/news"


    instructions = f"""
    Extract featured or promoted courses shown on the homepage '{target_url}'.
    For each course, return:
    1. title (course name),
    2. articleUrl (link to the course),
    3. imageUrl (thumbnail),
    4. excerpt (short course description or rating).
    """



    print("--- Running Web Scraper ---")
    result, screenshot = await webscraper(target_url, instructions)
    print("\n--- Scraping Finished ---")

    if screenshot:
        try:
            display(IPImage(data=screenshot))
        except Exception:
            with open("euron_screenshot.png", "wb") as f:
                f.write(screenshot)
            print("Screenshot saved to euron_screenshot.png")

    if result and result.articles:
        print("\n--- Extracted Articles ---")
        df = pd.DataFrame([article.model_dump() for article in result.articles])
        print(tabulate(df, headers='keys', tablefmt='grid'))
    elif result:
        print("\n--- No articles extracted ---")
    else:
        print("\n--- No results ---")


if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            print("Async loop running. Use 'await main()' in notebook.")
        else:
            asyncio.run(main())
    except RuntimeError:
        asyncio.run(main())
