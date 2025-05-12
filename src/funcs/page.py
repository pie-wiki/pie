from flask import Blueprint, abort
import os
import sys
import markdown
from flask_themes2 import render_theme_template, get_theme

from flask import Blueprint, request, redirect, url_for, abort
import os
import markdown
from flask_login import login_required
from flask_themes2 import render_theme_template, get_theme

page_bp = Blueprint('page', __name__)

def get_current_theme():
    return get_theme('default')  # Replace with dynamic selection if needed

@page_bp.route('/<space>/<page>')
def render_markdown(space, page):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    md_path = os.path.join(base_dir, '..', 'pages', space, f'{page}.md')
    print(f"Looking for Markdown file at: {md_path}")  # Debugging output
    print('This is standard output', file=sys.stdout)
    if not os.path.exists(md_path):
        abort(404)
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    html_content = markdown.markdown(content)
    return render_theme_template(get_current_theme(), 'page.html', content=html_content, space=space, page=page)

@page_bp.route('/<space>/<page>/edit', methods=['GET', 'POST'])
@login_required
def edit_page(space, page):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    page_dir = os.path.join(base_dir, '..', 'pages', space)
    md_path = os.path.join(page_dir, f'{page}.md')
    if request.method == 'POST':
        content = request.form.get('content', '')
        os.makedirs(page_dir, exist_ok=True)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return redirect(url_for('page.render_markdown', space=space, page=page))
    else:
        if os.path.exists(md_path):
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = ''
        return render_theme_template(get_current_theme(), 'edit_page.html', content=content, space=space, page=page)

@page_bp.route('/<space>/new', methods=['GET', 'POST'])
@login_required
def create_page(space):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    page_dir = os.path.join(base_dir, '..', 'pages', space)
    if request.method == 'POST':
        page_name = request.form.get('page_name', '').strip()
        content = request.form.get('content', '')
        if not page_name:
            return render_theme_template(get_current_theme(), 'create_page.html', error='Page name is required.', space=space)
        md_path = os.path.join(page_dir, f'{page_name}.md')
        if os.path.exists(md_path):
            return render_theme_template(get_current_theme(), 'create_page.html', error='Page already exists.', space=space)
        os.makedirs(page_dir, exist_ok=True)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return redirect(url_for('page.render_markdown', space=space, page=page_name))
    else:
        return render_theme_template(get_current_theme(), 'create_page.html', space=space)
