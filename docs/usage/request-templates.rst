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
specific parameters. For example:

.. code-block:: python

    from scrapy import Request, Spider
    from scrapy_poet import DummyResponse
    from zyte_common_items import SearchRequestTemplate


    class ExampleComSpider(Spider):
        name = "example_com"

        def start_requests(self):
            yield Request("https://example.com", callback=self.start_search)

        def start_search(
            self, response: DummyResponse, search_request_template: SearchRequestTemplate
        ):
            yield search_request_template.request(query="foo bar").to_scrapy(
                callback=self.parse_result
            )

        def parse_result(self, response): ...

``search_request_template.request(query="foo bar")`` builds a
:class:`~zyte_common_items.Request` object, e.g. with URL
``https://example.com/search?q=foo+bar``.


.. _custom-request-template-page:

Writing a request template page object
======================================

To enable building a request template for a given website, build a page object
for that website that returns the corresponding request template item class.
For example:

.. code-block:: python

    from web_poet import handle_urls
    from zyte_common_items import SearchRequestTemplatePage


    @handle_urls("example.com")
    class ExampleComSearchRequestTemplatePage(SearchRequestTemplatePage):
        @field
        def url(self):
            return "https://example.com/search?q={{ query|quote_plus }}"

Strings returned by request template page object fields are :doc:`Jinja
templates <jinja:templates>`, and may use the query arguments of the
``request`` method of the corresponding :ref:`request template item class
<request-template-api>`.

Often, you only need to build a URL template by figuring out where request
parameters go and using the right URL-encoding :ref:`filter <filters>`,
:func:`~jinja-filters.urlencode` or :func:`~urllib.parse.quote_plus`, depending
on how spaces are encoded:

=================================== ===================================================
Example search URL for “foo bar”    URL template
=================================== ===================================================
https://example.com/?q=foo%20bar    ``https://example.com/?q={{ query|urlencode }}``
https://example.com/?q=foo+bar      ``https://example.com/?q={{ query|quote_plus }}``
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
                    if query|length > 1
                    and query[0]|lower == 'p'
                    and query[1:]|int(-1) != -1
                -%}
                    https://example.com/p/{{ query|upper }}
                {%- else -%}
                    https://example.com/search
                {%- endif -%}
            """

        @field
        def method(self):
            return """
                {%-
                    if query|length > 1
                    and query[0]|lower == 'p'
                    and query[1:]|int(-1) != -1
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
                    if query|length > 1
                    and query[0]|lower == 'p'
                    and query[1:]|int(-1) != -1
                -%}
                {%- else -%}
                    {"query": {{ query|tojson }}}
                {%- endif -%}
            """

        @field
        def headers(self):
            return [
                Header(
                    name=(
                        """
                            {%-
                                if query|length > 1
                                and query[0]|lower == 'p'
                                and query[1:]|int(-1) != -1
                            -%}
                            {%- else -%}
                                Query
                            {%- endif -%}
                        """
                    ),
                    value="{{ query }}",
                ),
            ]
