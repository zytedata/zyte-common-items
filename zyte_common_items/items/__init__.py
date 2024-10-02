# flake8: noqa
from ._compat import RequestListCaster
from .article import Article, ArticleMetadata
from .article_list import ArticleFromList, ArticleList, ArticleListMetadata
from .article_navigation import ArticleNavigation, ArticleNavigationMetadata
from .business_place import BusinessPlace, BusinessPlaceMetadata
from .custom_attributes import (
    CustomAttributes,
    CustomAttributesMetadata,
    CustomAttributesValues,
)
from .job_posting import JobPosting, JobPostingMetadata
from .job_posting_navigation import JobPostingNavigation, JobPostingNavigationMetadata
from .product import Product, ProductMetadata, ProductVariant
from .product_list import ProductFromList, ProductList, ProductListMetadata
from .product_navigation import ProductNavigation, ProductNavigationMetadata
from .real_estate import RealEstate, RealEstateMetadata
from .search_request_template import (
    SearchRequestTemplate,
    SearchRequestTemplateMetadata,
)
from .serp import Serp, SerpMetadata, SerpOrganicResult
from .social_media_post import SocialMediaPost, SocialMediaPostMetadata
