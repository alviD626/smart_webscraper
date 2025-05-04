# schemas/article_schema.py

from pydantic import BaseModel, Field
from typing import Optional, List

class EuronArticle(BaseModel):
    title: str = Field(..., description="The main title of the article")
    articleUrl: Optional[str] = Field(None, description="The full article URL")  # Changed from HttpUrl to str for Arrow compatibility
    imageUrl: Optional[str] = Field(None, description="The image URL for the article")  # Changed from HttpUrl to str
    excerpt: Optional[str] = Field(None, description="A short excerpt of the article")

class EuronArticleList(BaseModel):
    articles: List[EuronArticle] = Field(..., description="List of extracted articles")




