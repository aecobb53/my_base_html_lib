from turtle import width
from phtml import Document, Div, Style, Header, Link, Image
from pydantic import BaseModel, model_validator
from typing import Dict, List, Optional


class NavigationContent(BaseModel):
    webpage_name: str
    navigation_content: Optional[List] = None
    style_name: Optional[str] = '.navigation_content'
    style_details: Optional[Dict[str, str]] = {}

    navigation_urls: Dict[str, str] = {}

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        # Style Details
        if 'style_details' not in fields:
            fields['style_details'] = {
                'background-color': '#1e1f22',
                'height': '50px',  # Overridable
                'color': '#949ba4',
                'padding': '0',
                'margin': '0',
                'position': 'relative',
            }

        # Navigation Urls
        navigation_urls = {
            'Home': '/',
        }
        if 'navigation_urls' in fields:
            navigation_urls.update(fields['navigation_urls'])
        navigation_urls['About'] = '/about'
        fields['navigation_urls'] = navigation_urls

        return fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.navigation_content = self.generate_default_navigation_content()

    def generate_default_navigation_content(self):
        # This method is for setting default behavior
        navigation_content = [
            # Link(href='favicon.png'),
            Header(level=1, internal=self.webpage_name).add_style(Style(style_details={
                'margin': '0',
                'padding': '5px 0 5px',
                'display': 'inline-block'})),
        ]
        link_style = Style(style_details={
            'margin': '15px',
            'padding': '0',
            'color': '#949ba4',
            'display': 'inline-block',
            'float': 'right'
        })
        for navigation_url_name in reversed(list(self.navigation_urls.keys())):
            navigation_url = self.navigation_urls[navigation_url_name]
            navigation_content.append(
                Link(href=navigation_url, internal=navigation_url_name).add_style(link_style))
        return navigation_content

    def return_style_object(self):
        obj = Style(name=self.style_name, style_details=self.style_details)
        return obj

    def return_html_object(self, height='50px'):
        style_object = self.return_style_object()
        style_object.styles['height'] = height
        obj = Div(
            internal=self.navigation_content).add_class(
                'navigation_content').add_style(
                    style_object)
        return obj


class SidebarContent(BaseModel):
    sidebar_content: Optional[List] = None
    style_name: Optional[str] = '.sidebar_content'
    style_details: Optional[Dict[str, str]] = {}

    sidebar_urls: Dict[str, str] = {}

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        # Style Details
        if 'style_details' not in fields:
            fields['style_details'] = {
                'background-color': '#2b2d31',
                # 'height': '100%',
                'top': '0',  # Overridable
                'width': '200px',  # Overridable
                'position': 'fixed',
                'z-index': '1',
                'left': '0',
                'overflow-x': 'hidden',
                'color': '#949ba4',
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
            internal=self.sidebar_content).add_class(
                'sidebar_content').add_style(
                    style_object)
        return obj


class BodyContent(BaseModel):
    body_content: Optional[List] = None
    style_name: Optional[str] = '.body_content'
    style_details: Optional[Dict[str, str]] = {}

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        # Style Details
        if 'style_details' not in fields:
            fields['style_details'] = {
                'position': 'relative',
                'color': '#c4cedb',
            }

        return fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body_content = self.generate_default_body_content()

    def generate_default_body_content(self):
        # This method is for setting default behavior
        body_content = self.body_content
        return body_content

    def return_style_object(self):
        obj = Style(name=self.style_name, style_details=self.style_details)
        return obj

    def return_html_object(self, left_offset=None):
        # if top_offset is not None:
        #     self.style_details['top'] = top_offset
        if left_offset is not None:
            self.style_details['left'] = left_offset
        style_object = self.return_style_object()
        obj = Div(
            internal=self.body_content).add_class(
                'body_content').add_style(
                    style_object)
        return obj


class FooterContent(BaseModel):
    footer_content: Optional[List] = None
    style_name: Optional[str] = '.footer_content'
    style_details: Optional[Dict[str, str]] = {}

    navigation_urls: Dict[str, str] = {}

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        # Style Details
        if 'style_details' not in fields:
            fields['style_details'] = {
                'background-color': '#1e1f22',
                'color': '#949ba4',
                'position': 'fixed',
                'bottom': '0',
                'width': '100%',
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

    def return_html_object(self, height='50px'):
        style_object = self.return_style_object()
        style_object.styles['height'] = height
        obj = Div(
            internal=self.footer_content).add_class(
                'footer_content').add_style(
                    style_object)
        return obj


class MyBaseDocument:
    def __init__(self,
        navigation_height='50px',
        footer_height='50px',
        sidebar_width='200px',
        navigation_content=None,
        sidebar_content=None,
        body_content=None,
        footer_content=None,):
        # Globals
        self.navigation_height = navigation_height
        self.footer_height = footer_height
        self.sidebar_width = sidebar_width
        self.body_content = body_content
        self.footer_content = footer_content

        # document
        self.document_style = Style(name='body', style_details={
            'background-color': '#313338',
            'padding': '0',
            'margin': '0',
            'position': 'relative',
        })

        # navigation_content
        self.navigation_content = navigation_content

        # sidebar_content
        self.sidebar_content = sidebar_content

        # body_content
        self.body_content = body_content

        # footer_content
        self.footer_content = footer_content

    @property
    def return_document(self):
        document = Document()
        document.add_style(self.document_style)

        # navigation_content
        if self.navigation_content:
            # self.navigation_content.style_details['height'] = self.navigation_height
            # self.navigation_content_style.styles['height'] = self.navigation_height
            # navigation_content = Div(
            #     internal=self.navigation_content).add_class('navigation_content').add_style(
            #         self.navigation_content_style
            #     )
            # document.add_body_element(navigation_content)
            height = self.navigation_height
            document.add_body_element(self.navigation_content.return_html_object(height=height))

        # sidebar_content
        if self.sidebar_content:
            # if self.navigation_content:
            #     self.sidebar_content_style.styles['top'] = self.navigation_height
            if self.navigation_content is not None:
                top_offset = self.navigation_height
            else:
                top_offset = '0'
            if self.footer_content is not None:
                footer_offset = self.footer_height
            else:
                footer_offset = '0'
            document.add_body_element(self.sidebar_content.return_html_object(
                top_offset=top_offset, bottom_offset=footer_offset, width=self.sidebar_width))
            # sidebar_content = Div(
            #     internal=self.sidebar_content).add_class('sidebar_content').add_style(
            #         self.sidebar_content_style
            #     )
            # document.add_body_element(sidebar_content)

        # body_content
        if self.body_content:
            if self.sidebar_content is not None:
                left_offset = self.sidebar_width
            else:
                left_offset = '0'
            document.add_body_element(self.body_content.return_html_object(
                left_offset=left_offset
            ))
            # if self.navigation_content:
            #     self.body_content_style.styles['top'] = self.navigation_height
            # if self.sidebar_content:
            #     self.body_content_style.styles['left'] = self.sidebar_width
            # body_content = Div(
            #     internal=self.body_content).add_class('body_content').add_style(
            #         self.body_content_style
            #     )
            # document.add_body_element(body_content)

        # footer_content
        if self.footer_content:
            document.add_body_element(self.footer_content.return_html_object(
                height=self.footer_height))
            # if self.navigation_content:
            #     self.footer_content_style.styles['top'] = self.navigation_height
            # if self.sidebar_content:
            #     self.footer_content_style.styles['left'] = self.sidebar_width
            # footer_content = Div(
            #     internal=self.footer_content).add_class('footer_content').add_style(
            #         self.footer_content_style
            #     )
            # document.add_body_element(footer_content)
        return document.return_document
