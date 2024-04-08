import sys
sys.path.append('/home/acobb/git/my_base_html_lib')

from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent
from phtml import *

base_object = MyBaseDocument()

navigation_content = NavigationContent(
    webpage_name='Test Webpage',
)
base_object.navigation_content = navigation_content

sidebar_content = SidebarContent(
    sidebar_content=[Header(level=1, internal='Sidebar').add_style(Style(style_details={'margin': '0', 'padding': '0 5px'}))],
)
base_object.sidebar_content = sidebar_content


body_big_content_string = []
with open('/home/acobb/git/my_base_html_lib/tests/resources/big_data_file.html', 'r') as f:
    for line in f.readlines():
        body_big_content_string.append(line[:-1])
body_big_content_string = ''.join(body_big_content_string)

body_content = BodyContent(
    body_content=[
        Header(level=1, internal='Body Stuff').add_style(Style(style_details={'margin': '0', 'padding': '0 5px'})),
        body_big_content_string,
    ],
)
base_object.body_content = body_content

footer_content = FooterContent(
    footer_content=[Header(level=1, internal='Footer Details').add_style(Style(style_details={'margin': '0', 'padding': '0'}))],
)
base_object.footer_content = footer_content

result = base_object.return_document
print(result)
with open('tests/test_output/test_file.html', 'w') as file:
    file.write(result)
