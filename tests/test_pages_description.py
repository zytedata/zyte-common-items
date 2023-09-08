import pytest
from web_poet import HttpResponse, field

from zyte_common_items import (
    BusinessPlacePage,
    JobPostingPage,
    ProductPage,
    RealEstatePage,
)

HTML = b"""
<!DOCTYPE html>
<html>
    <body>
        <article><div>\xe2\x82\xact&eacute;xt</div><p style="color:blue">text2&gt;</p><div class="twitter-tweet">tw</div></article>
    </body>
</html>
"""


DESCR_HTML_CLEANED = """<article>

<p>€téxt</p>

<p>text2&gt;</p>

<div class="twitter-tweet">tw</div>

</article>"""


TEXT_CLEANED = "€téxt\n\ntext2>\n\ntw"


DESCR_HTML_WRAPPED = """<article>

<p>€téxt</p>

<p>text2&gt;</p>

<p>tw</p>

</article>"""


@pytest.mark.asyncio
async def test_descriptionHtml_selector():
    # descriptionHtml is extracted from the returned node
    # description is produced from descriptionHtml (with html-text)
    class CustomProductPage(ProductPage):
        call_count = 0

        @field
        def descriptionHtml(self):
            self.call_count += 1
            return self.css("article")

    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=HTML))
    assert page.call_count == 0
    assert page.descriptionHtml == DESCR_HTML_CLEANED
    assert page.call_count == 1
    assert await page.description == TEXT_CLEANED
    assert page.call_count == 1

    page = CustomProductPage(response=HttpResponse(url=url, body=HTML))
    assert page.call_count == 0
    assert await page.description == TEXT_CLEANED
    assert page.call_count == 1
    assert page.descriptionHtml == DESCR_HTML_CLEANED
    assert page.call_count == 2  # we want this to be 1


@pytest.mark.asyncio
async def test_descriptionHtml_explicit():
    # descriptionHtml is returned as is
    # description is produced from descriptionHtml
    class CustomProductPage(ProductPage):
        call_count = 0

        @field
        def descriptionHtml(self):
            self.call_count += 1
            return self.css("article").get()

    html = '<article><div>€téxt</div><p style="color:blue">text2&gt;</p><div class="twitter-tweet">tw</div></article>'

    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=HTML))
    assert page.call_count == 0
    assert page.descriptionHtml == html
    assert page.call_count == 1
    assert await page.description == TEXT_CLEANED
    assert page.call_count == 2  # we want this to be 1
    assert await page.description == TEXT_CLEANED
    assert page.call_count == 2  # we want this to be 1

    page = CustomProductPage(response=HttpResponse(url=url, body=HTML))
    assert page.call_count == 0
    assert await page.description == TEXT_CLEANED
    assert page.call_count == 1
    assert page.descriptionHtml == html
    assert page.call_count == 2  # we want this to be 1


@pytest.mark.asyncio
async def test_descriptionHtml_async():
    class CustomProductPage(ProductPage):
        @field
        async def descriptionHtml(self):
            return self.css("article")

    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=HTML))
    assert await page.descriptionHtml == DESCR_HTML_CLEANED
    assert await page.description == TEXT_CLEANED

    page = CustomProductPage(response=HttpResponse(url=url, body=HTML))
    assert await page.description == TEXT_CLEANED
    assert await page.descriptionHtml == DESCR_HTML_CLEANED


@pytest.mark.asyncio
async def test_description_selector():
    # description is extracted from the returned node
    # descriptionHtml is extracted from the same node
    class CustomProductPage(ProductPage):
        call_count = 0

        @field
        def description(self):
            self.call_count += 1
            return self.css("article")

    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=HTML))
    assert page.call_count == 0
    assert page.description == TEXT_CLEANED
    assert page.call_count == 1
    assert await page.descriptionHtml == DESCR_HTML_CLEANED
    assert page.call_count == 1

    page = CustomProductPage(response=HttpResponse(url=url, body=HTML))
    assert page.call_count == 0
    assert await page.descriptionHtml == DESCR_HTML_CLEANED
    assert page.call_count == 1
    assert page.description == TEXT_CLEANED
    assert page.call_count == 2  # we want this to be 1


@pytest.mark.asyncio
async def test_description_explicit():
    # description is returned as is
    # descriptionHtml is produced by wrapping description
    class CustomProductPage(ProductPage):
        call_count = 0

        @field
        def description(self):
            self.call_count += 1
            return TEXT_CLEANED

    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=HTML))
    assert page.call_count == 0
    assert page.description == TEXT_CLEANED
    assert page.call_count == 1
    assert await page.descriptionHtml == DESCR_HTML_WRAPPED
    assert page.call_count == 1
    assert await page.descriptionHtml == DESCR_HTML_WRAPPED
    assert page.call_count == 1

    page = CustomProductPage(response=HttpResponse(url=url, body=HTML))
    assert page.call_count == 0
    assert await page.descriptionHtml == DESCR_HTML_WRAPPED
    assert page.call_count == 1
    assert page.description == TEXT_CLEANED
    assert page.call_count == 2  # we want this to be 1


@pytest.mark.asyncio
async def test_none():
    # when neither description nor descriptionHtml are user-defined,
    # both return None
    class CustomProductPage(ProductPage):
        pass

    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=HTML))
    assert await page.description is None
    assert await page.descriptionHtml is None


@pytest.mark.asyncio
async def test_job_posting_mixin():
    class CustomPage(JobPostingPage):
        @field
        def descriptionHtml(self):
            return self.css("article")

    url = "https://example.com"
    page = CustomPage(response=HttpResponse(url=url, body=HTML))
    assert page.descriptionHtml == DESCR_HTML_CLEANED
    assert await page.description == TEXT_CLEANED


@pytest.mark.parametrize(
    "page_class",
    (
        BusinessPlacePage,
        JobPostingPage,
        RealEstatePage,
    ),
)
def test_description_simple(page_class: type):
    class CustomPage(page_class):
        @field
        def description(self):
            return self.css("article")

    url = "https://example.com"
    page = CustomPage(response=HttpResponse(url=url, body=HTML))
    assert page.description == TEXT_CLEANED
