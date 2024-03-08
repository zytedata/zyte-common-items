.. _request-templates:

=================
Request templates
=================

:ref:`Request templates <request-template-api>` are :ref:`items <items>` that
allow writing reusable code that creates :class:`~zyte_common_items.Request`
objects from parameters.

Using request templates
=======================

After you :ref:`write a request template page object
<custom-request-template-page>` for a website, you can get a request template
item for that website and call its ``request`` method to build a request with
specific parameters.

For example, after implementing the page object :ref:`below
<custom-request-template-page>`, you can get a
:class:`~zyte_common_items.SearchRequestTemplate` object for
https://quotes.toscrape.com/, and build a search request for a specific
keyword. Using :doc:`scrapy-poet <scrapy-poet:index>`:

.. code-block:: python

    from scrapy import Request, Spider
    from scrapy_poet import DummyResponse
    from zyte_common_items import SearchRequestTemplate


    class QuotesToScrapeComSpider(Spider):
        name = "quotes_toscrape_com"

        def start_requests(self):
            yield Request("https://quotes.toscrape.com", callback=self.start_search)

        def start_search(
            self, response: DummyResponse, search_request_template: SearchRequestTemplate
        ):
            yield search_request_template.render(keyword="Unhappy Marriage").to_scrapy(
                callback=self.parse_quotes
            )

        def parse_quotes(self, response):
            ...

``search_request_template.render(keyword="Unhappy Marriage")`` builds a
:class:`~zyte_common_items.Request` object with URL
``https://quotes.toscrape.com/tag/unhappy-marriage/``.


.. _custom-request-template-page:

Writing a request template page object
======================================

To enable building a request template for a given website, build a page object
for that website that returns the corresponding request template item class.

For example, to build a search request template to search for quotes in
https://quotes.toscrape.com/ by tag, create the following page object class:

.. code-block:: python

    from web_poet import handle_urls
    from zyte_common_items import SearchRequestTemplatePage


    @handle_urls("quotes.toscrape.com")
    class QuotesToScrapeComSearchRequestTemplatePage(SearchRequestTemplatePage):
        @field
        def url(self):
            return "https://quotes.toscrape.com/tag/{{ keyword|lower|replace(' ', '-')|urlencode }}/"

Strings returned by request template page object fields are :doc:`Jinja
templates <jinja:templates>`, and may use the keyword arguments of the
``request`` method of the corresponding :ref:`request template item class
<request-template-api>`.

Often, you only need to build a URL template by figuring out where request
parameters go and using the right URL-encoding :ref:`filters <filters>`,
:func:`~jinja-filters.urlencode` or :func:`~urllib.parse.quote_plus`, depending
on how spaces are encoded:

=================================== ===================================================
Example search URL for “foo bar”    URL template
=================================== ===================================================
https://example.com/?q=foo%20bar    ``https://example.com/?q={{ keyword|urlencode }}``
https://example.com/?q=foo+bar      ``https://example.com/?q={{ keyword|quote_plus }}``
=================================== ===================================================

You can use any of :ref:`Jinja’s built-in filters <builtin-filters>`, plus
:func:`~urllib.parse.quote_plus`, and all other Jinja features. Jinja enables
very complex scenarios:

.. code-block:: python

    class ComplexSearchRequestTemplatePage(SearchRequestTemplatePage):
        @field
        def url(self):
            return """
                {%-
                    if keyword|length > 1
                    and keyword[0]|lower == 'p'
                    and keyword[1:]|int(-1) != -1
                -%}
                    https://example.com/p/{{ keyword|upper }}
                {%- else -%}
                    https://example.com/search
                {%- endif -%}
            """

        @field
        def method(self):
            return """
                {%-
                    if keyword|length > 1
                    and keyword[0]|lower == 'p'
                    and keyword[1:]|int(-1) != -1
                -%}
                    GET
                {%- else -%}
                    POST
                {%- endif -%}
            """

        @field
        def body(self):
            return """
                {%-
                    if keyword|length > 1
                    and keyword[0]|lower == 'p'
                    and keyword[1:]|int(-1) != -1
                -%}
                {%- else -%}
                    {"query": {{ keyword|tojson }}}
                {%- endif -%}
            """

        @field
        def headers(self):
            return [
                Header(
                    name=(
                        """
                            {%-
                                if keyword|length > 1
                                and keyword[0]|lower == 'p'
                                and keyword[1:]|int(-1) != -1
                            -%}
                            {%- else -%}
                                Query
                            {%- endif -%}
                        """
                    ),
                    value="{{ keyword }}",
                ),
            ]
