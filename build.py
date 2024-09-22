import markdown
import os
import shutil
from bs4 import BeautifulSoup

# additional function incase the directories  need to be reset
def rebuild_directories():
    if os.path.isdir('pages'):
        shutil.rmtree('pages')
    if os.path.isdir('poems'):
        shutil.rmtree('poems')
    if os.path.exists('index.html'):
        os.remove('index.html')
    
    os.makedirs('poems')
    os.makedirs('pages')

# inserts lower_soup into upper_soup at tag with id_name
def insert_to_tag(id_name, upper_soup, lower_soup):
    tag_poem = upper_soup.find(id=id_name) 
    tag_poem.insert(0, lower_soup)

# returns wrapper_soup after creation from template and attaching page_soup to it
# sets title of Webpage
def attach_page_soup(page_soup, name):
    with open('source/templates/wrapper.html') as f_wrap:
        wrapper_soup = BeautifulSoup(f_wrap, 'html.parser')
    
    insert_to_tag("main_body", wrapper_soup, page_soup)

    title = wrapper_soup.title
    title.string = title.string.replace("SETTITLE", name.title().replace('_', ' '))

    return wrapper_soup

# sets current page to active in nav_bar in wrapper
def set_active(nav_name, wrapper):
    tag_nav = wrapper.find(id="nav_" + nav_name)
    tag_nav['class'] = 'active'

# writes wrapper_soup to output html file at path
def write_output(path, wrapper_soup):
    with open(path, "w") as f_out:
        f_out.write(str(wrapper_soup))

# builds index.html to root
def build_index():
    page_name = 'home'
    file_path = 'index.html'

    with open('source/' + file_path) as f_index:
        page_soup = BeautifulSoup(f_index, 'html.parser')

    wrapper = attach_page_soup(page_soup, page_name)
    set_active(page_name, wrapper)
    write_output(file_path, wrapper)

# builds poems to poems/ from .md files in source/poems
def build_poems():
    directory = os.fsencode('source/poems/') 

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        page_name = filename.split('.')[0]

        poem_html = ""
        page_soup = ""
        with open('source/poems/' + filename, 'r') as fin:
            for line in fin:
                line = line.replace('\n', '<br/>')
                html_string = markdown.markdown(line)
                html_string = html_string.replace('<p>', '')
                html_string = html_string.replace('</p>', '')
                poem_html += html_string + '\n'
        poem_soup = BeautifulSoup(poem_html, 'html.parser')

        with open('source/templates/poem_wrapper.html') as f_poem:
            page_soup = BeautifulSoup(f_poem, 'html.parser')

        header = page_soup.find(id="poem_title") 
        header.string = page_name.replace('_', ' ')

        img = page_soup.find(id="poem_img")
        img['src'] = '../images/' + page_name + '.jpeg'

        insert_to_tag('main_poetry', page_soup, poem_soup)

        wrapper = attach_page_soup(page_soup, page_name)
        set_active('poetry', wrapper)
        write_output('poems/' + page_name + '.html', wrapper)

# builds Poetry and About pages from source/pages/ HTML file to pages/
def build_pages():
    directory = os.fsencode('source/pages/') 

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        page_name = filename.split('.')[0]

        with open('source/pages/' + filename) as f_index:
            page_soup = BeautifulSoup(f_index, 'html.parser')

        wrapper = attach_page_soup(page_soup, page_name)
        if (page_name == 'about'):
            set_active('about', wrapper)
        else:
            set_active('poetry', wrapper)
            tag_main = wrapper.find(id="main_body")
            tag_main['id'] = ''
            tag_main['class'] = 'main'
        write_output('pages/' + filename, wrapper)

def build_html():
    #rebuild_directories()

    build_index()
    build_poems()
    build_pages()

    print("Build successful!")

build_html()