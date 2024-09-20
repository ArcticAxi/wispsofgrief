import markdown
import os
import shutil

def open_fout(file):
    global fout
    fout = open(file, 'a')
    fout.truncate(0)

def close_fout():
    fout.close()

def markdown_to_html(path):
    with open(path, 'r') as fin:
        markdown_string = fin.read()
        html_string = markdown.markdown(markdown_string)
        fout.write(html_string)

def format_poem(name):
    file_location = 'source/poems/' + name + '.md'
    with open(file_location, 'r') as fin:
        for line in fin:
            line = line.replace('\n', '<br/>')

            html_string = markdown.markdown(line)
            html_string = html_string.replace('<p>', '')
            html_string = html_string.replace('</p>', '')

            fout.write(html_string)

def replace_underscore(path, name):
    with open(path, 'r') as fin:
        for line in fin:
            line = line.replace('SETTITLE', name.replace('_', ' '))
            html_string = markdown.markdown(line)
            fout.write(html_string)

def write_poem_body(name):
    replace_underscore('source/templates/poetry_start.md', name)    
    format_poem(name)
    with open('source/templates/poetry_end.md', 'r') as fin:
        for line in fin:
            line = line.replace('SETIMAGE', '../images/' + name.lower() + '.JPG')
            html_string = markdown.markdown(line)
            fout.write(html_string)

def write_head(name):
    replace_underscore('source/templates/head.md', name)
    with open('source/templates/header.md', 'r') as fin:
        for line in fin:
            if (name.lower() == 'home'):
                line = line.replace('href="../index.html"', 'href="index.html"')
            html_string = markdown.markdown(line)
            fout.write(html_string)

    with open('source/templates/navbar.md', 'r') as fin:
        for line in fin:
            # set class="active" for current page
            if (name == 'Home'):
                line = line.replace('href="index.html"', 'href="index.html" class="active"')
            elif (name == 'About'):
                line = line.replace('href="index.html"', 'href="../index.html"')
                line = line.replace('href="/pages/about.html"', 'href="/pages/about.html" class="active"')
            else:
                line = line.replace('href="index.html"', 'href="../index.html"')
                line = line.replace('href="/pages/poetry.html"', 'href="/pages/poetry.html" class="active"')
            html_string = markdown.markdown(line)
            fout.write(html_string)

def builds(dir_str, dir_out):
    if (dir_out == ''):
        open_fout('index.html')
        write_head('Home')
        markdown_to_html('source/index.md') # index.md
        markdown_to_html('source/templates/footer.md')
        close_fout()
    else:    
        page_name = ''

        directory = os.fsencode(dir_str)
        os.makedirs(dir_out)

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            page_name = filename.split('.')[0]

            # do functions below for each poem
            open_fout(dir_out + '/' + page_name + '.html')
            write_head(page_name.title())
            # if statement for different number
            if (page_name == 'poetry'):
                markdown_to_html('source/pages/poetry.md') # poetry.md
            elif (page_name == 'about'):
                markdown_to_html('source/pages/about.md') # about.md
            else:
                write_poem_body(page_name.title())
            markdown_to_html('source/templates/footer.md')
            close_fout()

def build_html():
# removes directory and folders within
    if os.path.isdir('pages'):
        shutil.rmtree('pages')
    if os.path.isdir('poems'):
        shutil.rmtree('poems')
    if os.path.exists('index.html'):
        os.remove('index.html')

    builds('source/poems', 'poems')
    builds('source/pages', 'pages')
    builds('source', '')

build_html()