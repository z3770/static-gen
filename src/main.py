import os
import sys
import shutil
from blocks import markdown_to_html_node


def copy_static(src, dst):
    # On the first call, wipe the destination clean
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for entry in os.listdir(src):
        src_path = os.path.join(src, entry)
        dst_path = os.path.join(dst, entry)
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"Entering directory: {src_path}")
            copy_static(src_path, dst_path)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found in markdown")


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    # Rewrite absolute root-relative paths to use the basepath
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(html)


def generate_pages_recursive(content_dir, template_path, dest_dir, basepath="/"):
    for entry in os.listdir(content_dir):
        src_path = os.path.join(content_dir, entry)
        dst_path = os.path.join(dest_dir, entry)
        if os.path.isfile(src_path) and entry.endswith(".md"):
            html_path = dst_path[:-3] + ".html"  # replace .md with .html
            generate_page(src_path, template_path, html_path, basepath)
        elif os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dst_path, basepath)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_src = os.path.join(project_root, "static")
    docs_dst = os.path.join(project_root, "docs")
    copy_static(static_src, docs_dst)

    generate_pages_recursive(
        os.path.join(project_root, "content"),
        os.path.join(project_root, "template.html"),
        docs_dst,
        basepath,
    )


main()
