from pydoc import doc
import re
from phtml import Document, Div, Style, StyleTag, Header, Link, Image, Base
from pydantic import BaseModel, model_validator, ConfigDict
from typing import Dict, List, Optional, Any


primary_background = '#393B41'
secondary_background = '#1e1f22'
accent_background = '#000000'
primary_text = '#949ba4'


NAVIGATION_BACKGROUND_COLOR = secondary_background
NAVIGATION_ACCENT_COLOR = accent_background
NAVIGATION_TEXT_COLOR = primary_text

BODY_BACKGROUND_COLOR = secondary_background
BODY_TEXT_COLOR = primary_text


navigation_background_color = ''
navigation_text_color = ''

body_background_color = ''
body_background_accent_color = ''


class NavigationContent(BaseModel):
    webpage_name: str | Base
    navigation_links: Dict = {}
    style_items: Dict = {}

    background_color: str = None
    text_color: str = None

    webpage_name_link: str | None = None  # None will not link

    navigation_div: Any = None
    navigation_styles: Any = []

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if not isinstance(fields, dict):
            fields = fields.model_dump()
        if not fields.get('navigation_links'):
            fields['navigation_links'] = {
                'About': '/about',
                'Home': '/home',
            }

        webpage_name = fields['webpage_name']
        if fields.get('webpage_name_link'):
            webpage_name = Link(
                href=fields['webpage_name_link'], internal=webpage_name).add_class('webpage-name-link')

        navigation_div = Div().add_class('navigation-bar-div')
        for link_name, link_url in fields['navigation_links'].items():
            navigation_div.add_element(
                Link(href=link_url, internal=link_name).add_class('navigation-bar-link'))
        navigation_div.add_element(Header(level=2, internal=webpage_name))

        background_color = fields.get('background_color', NAVIGATION_BACKGROUND_COLOR)
        text_color = fields.get('text_color', NAVIGATION_TEXT_COLOR)

        navigation_styles = [
            StyleTag(name='.navigation-bar-div', internal=f"""
                background-color: {background_color};
                width: 100%;
                height: 150px;
                color: {text_color};
                padding: 0;
                margin: 0;
            """),
            StyleTag(name='.webpage-name-link', internal=f"""
                color: {text_color};
                text-decoration: none;
                font-size: 2.5em;
            """),
            StyleTag(name='.navigation-bar-div h2', internal=f"""
                color: {text_color};
                display: inline-block;
                height: 100%;
                padding: 70px 30px;
                margin: 0;
            """),
            StyleTag(name='.navigation-bar-link', internal=f"""
                color: {text_color};
                background-color: {NAVIGATION_ACCENT_COLOR};
                padding: 13px;
                margin: 16px 8px;
                display: inline-block;
                float: right;
                border: 3px solid {NAVIGATION_ACCENT_COLOR};
                border-radius: 15px;
                -moz-border-radius: 15px;
                font-size: 1.5em;
            """),
        ]

        fields['navigation_div'] = navigation_div
        fields['navigation_styles'] = navigation_styles
        return fields

    @property
    def bar_height(self):
        for line in self.navigation_styles[0].internal[0].split('\n'):
            re_match = re.search(r'height: (\d+)', line.strip())
            if re_match:
                return int(re_match.group(1))

    def add_navigation_link(self, link_name: str, link_url: str):
        self.navigation_div.add_element(
            Link(href=link_url, internal=link_name).add_class('navigation-bar-link'))

    def add_navigation_styles(self, style_item: StyleTag):
        self.navigation_styles.append(style_item)


class SidebarContent(BaseModel):
    sidebar_content: Optional[List] = None
    style_name: Optional[str] = '.sidebar_content'
    style_details: Optional[Dict[str, str]] = {}
    id: Optional[str] = 'sidebar_content'

    sidebar_urls: Dict[str, str] = {}

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        # Style Details
        if 'style_details' not in fields:
            fields['style_details'] = {
                'background-color': '#2b2d31',
                'height': '100%',
                'top': '0',  # Overridable
                'width': '200px',  # Overridable
                'position': 'fixed',
                'z-index': '1',
                'left': '0',
                'overflow-x': 'hidden',
                'color': '#949ba4',
                'z-index': '40',
            }

        # # Sidebar Urls
        # sidebar_urls = {}
        # if 'sidebar_urls' in fields:
        #     sidebar_urls.update(fields['sidebar_urls'])
        # fields['sidebar_urls'] = sidebar_urls

        return fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sidebar_content = self.generate_default_sidebar_content()

    def generate_default_sidebar_content(self):
        # This method is for setting default behavior
        sidebar_content = self.sidebar_content
        # for sidebar_url_name in reversed(list(self.sidebar_urls.keys())):
        #     sidebar_url = self.sidebar_urls[sidebar_url_name]
        #     sidebar_content.append(
        #         Link(href=sidebar_url, internal=sidebar_url_name).add_style(
        #             Style(style_details={'margin': '15px', 'padding': '0', 'color': '#949ba4'})))
        return sidebar_content

    def return_style_object(self):
        obj = Style(name=self.style_name, style_details=self.style_details)
        return obj

    def return_html_object(self, top_offset, bottom_offset, width='200px'):
        style_object = self.return_style_object()
        style_object.styles['top'] = top_offset
        style_object.styles['bottom'] = bottom_offset
        style_object.styles['width'] = width
        obj = Div(
            internal=self.sidebar_content,
            id=self.id).add_class(
                'sidebar_content').add_style(
                    style_object)
        return obj


class BodyContent(BaseModel):
    body_content: List = []
    style_items: Dict = {}

    body_div: Any = None
    body_styles: Any = []

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if not isinstance(fields, dict):
            fields = fields.model_dump()

        body_div = Div().add_class('body-content-div')
        for item in fields.get('body_content', []):
            body_div.add_element(item)

        if not fields.get('body_styles'):
            fields['body_styles'] = [
                StyleTag(name='.body-content-div', internal=f"""
                    color: {BODY_TEXT_COLOR};
                    padding: 0;
                    margin: 0;
                """),
            ]

        fields['body_div'] = body_div
        # fields['body_styles'] = body_styles
        return fields

    def add_body_link(self, link_name: str, link_url: str):
        self.body_div.add_element(
            Link(href=link_url, internal=link_name).add_class('body-bar-link'))

    def add_body_styles(self, style_item: StyleTag):
        self.body_styles.append(style_item)

class FooterContent(BaseModel):
    footer_content: Optional[List] = None
    style_name: Optional[str] = '.footer_content'
    style_details: Optional[Dict[str, str]] = {}
    id: Optional[str] = 'footer_content'

    navigation_urls: Dict[str, str] = {}

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        # Style Details
        if 'style_details' not in fields:
            fields['style_details'] = {
                'background-color': '#1e1f22',
                'color': '#949ba4',
                'position': 'absolute',
                # 'position': 'fixed',
                # 'position': 'sticky',
                # 'bottom': '0',
                # 'left': '0',
                'height': '50px',  # Overridable
                'width': '100%',
                'z-index': '45',
            }

        return fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.footer_content = self.generate_default_footer_content()

    def generate_default_footer_content(self):
        # This method is for setting default behavior
        footer_content = self.footer_content

        link_style = Style(style_details={
            'margin': '15px',
            'padding': '0',
            'color': '#949ba4',
            'display': 'inline-block',
            'float': 'right',
        })
        for navigation_url_name in reversed(list(self.navigation_urls.keys())):
            navigation_url = self.navigation_urls[navigation_url_name]
            footer_content.append(
                Link(href=navigation_url, internal=navigation_url_name).add_style(link_style))
        return footer_content

    def return_style_object(self):
        obj = Style(name=self.style_name, style_details=self.style_details)
        return obj

    def return_html_object(self, height='50px', left_offset=None):
        style_object = self.return_style_object()
        style_object.styles['height'] = height
        if left_offset is not None:
            style_object.styles['left'] = left_offset
        obj = Div(
            internal=self.footer_content,
            id=self.id).add_class(
                'footer_content').add_style(
                    style_object)
        return obj


class MyBaseDocument:
    def __init__(self,
        navigation_content=None,
        sidebar_content=None,
        body_content=None,
        footer_content=None,
        document_style=None,
        style_items=None,
        primary_background_color=BODY_BACKGROUND_COLOR,
        onload_function=None,
        favicon=None
    ):
        self.navigation_content = navigation_content
        self.sidebar_content = sidebar_content
        self.body_content = body_content
        self.footer_content = footer_content
        self.onload_function = onload_function
        self.favicon = favicon

        doc_styles = []

        if document_style:
            doc_styles.extend(document_style)
        if style_items:
            doc_styles.extend(style_items)
        self.doc_styles = doc_styles

    @property
    def return_phtml(self):
        doc = Document()
        if self.favicon:
            doc.add_favicon(self.favicon)

        if self.onload_function:
            body = doc.html.internal[1]
            body.attributes['onload'] = self.onload_function
        doc_styles = self.doc_styles

        # Navigation Bar Content
        if self.navigation_content is not None:
            doc.add_body_element(self.navigation_content.navigation_div)
            doc_styles.extend(self.navigation_content.navigation_styles)

        # Body
        if self.body_content is not None:
            doc.add_body_element(self.body_content.body_div)
            doc_styles.extend(self.body_content.body_styles)

        # Style Items
        for style in doc_styles:
            doc.add_head_element(style)

        return doc

    @property
    def return_document(self):
        doc = self.return_phtml
        return doc.return_document


"""
https://stackoverflow.com/questions/609517/why-em-instead-of-px
"""
