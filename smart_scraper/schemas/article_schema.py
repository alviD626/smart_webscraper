# schemas/article_schema.py

from pydantic import BaseModel, Field
from typing import Optional, List

# class EuronArticle(BaseModel):
#     title: str = Field(..., description="The main title of the article")
#     articleUrl: Optional[str] = Field(None, description="The full article URL")  # Changed from HttpUrl to str for Arrow compatibility
#     imageUrl: Optional[str] = Field(None, description="The image URL for the article")  # Changed from HttpUrl to str
#     excerpt: Optional[str] = Field(None, description="A short excerpt of the article")

# class EuronArticleList(BaseModel):
#     articles: List[EuronArticle] = Field(..., description="List of extracted articles")




class EuronProduct(BaseModel):
    title: str = Field(..., description="The name of the product")
    productUrl: Optional[str] = Field(None, description="The full URL of the product")
    productCode: Optional[str] = Field(None, description="The unique product code/SKU")
    mainImage: Optional[str] = Field(None, description="The main product image URL")
    images: Optional[List[str]] = Field(default_factory=list, description="List of all product image URLs")
    mainColor: Optional[str] = Field(None, description="The main color of the product")
    colors: Optional[List[str]] = Field(default_factory=list, description="List of all available colors")
    description: Optional[str] = Field(None, description="Detailed product description")
    material: Optional[str] = Field(None, description="Product material or fabric information")
    price: Optional[float] = Field(None, description="Product price")
    currency: Optional[str] = Field(None, description="Currency of the price (e.g., EUR, USD)")
    sizes: Optional[List[str]] = Field(default_factory=list, description="Available product sizes")
    details: Optional[List[str]] = Field(default_factory=list, description="Additional product details and specifications")

# class EuronArticleList(BaseModel):
#     articles: List[EuronArticle] = Field(..., description="List of extracted products")