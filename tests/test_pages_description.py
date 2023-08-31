import pytest
from web_poet import HttpResponse, field

from zyte_common_items import ProductPage

HTML = b"""
<!DOCTYPE html>
<html>
    <body>
        <article><div>text</div><p style="color:blue">text2</p></article>
    </body>
</html>
"""

DESCR_HTML_CLEANED = """<article>

<p>text</p>

<p>text2</p>

</article>"""


TEXT_CLEANED = "text\n\ntext2"


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

    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=HTML))
    assert page.call_count == 0
    assert (
        page.descriptionHtml
        == '<article><div>text</div><p style="color:blue">text2</p></article>'
    )
    assert page.call_count == 1
    assert await page.description == TEXT_CLEANED
    assert page.call_count == 2  # we want this to be 1
    assert await page.description == TEXT_CLEANED
    assert page.call_count == 2  # we want this to be 1

    page = CustomProductPage(response=HttpResponse(url=url, body=HTML))
    assert page.call_count == 0
    assert await page.description == TEXT_CLEANED
    assert page.call_count == 1
    assert (
        page.descriptionHtml
        == '<article><div>text</div><p style="color:blue">text2</p></article>'
    )
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
    assert await page.descriptionHtml == DESCR_HTML_CLEANED
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
async def test_none():
    # when neither description nor descriptionHtml are user-defined,
    # both return None
    class CustomProductPage(ProductPage):
        pass

    url = "https://example.com"
    page = CustomProductPage(response=HttpResponse(url=url, body=HTML))
    assert await page.description is None
    assert await page.descriptionHtml is None
