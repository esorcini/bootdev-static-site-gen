import os
import shutil
import sys

from src.textnodehelpers import extract_title, markdown_to_html_node


def copy_files_r(src: str, dst: str) -> None:
    for file in os.listdir(src):
        src_file = os.path.join(src, file)
        if os.path.isdir(src_file):
            dst_dir = os.path.join(dst,file)
            print(f"Creating directory: {file} inside {dst}...")
            os.mkdir(dst_dir)
            copy_files_r(src_file,dst_dir)
        else:
            print(f"Copying file: {src_file} to {dst}...")
            shutil.copy(src_file,dst)

def copy_files(source: str, target: str):
    if not os.path.exists(source):
        raise FileNotFoundError(f"Could not find source path: {source}")

    try:
        shutil.rmtree(target, ignore_errors=True)
        os.mkdir(target)
    except FileNotFoundError as fnf:
        raise FileNotFoundError(f"Missing parent folder in target path: {target}") from fnf
    except OSError:
        raise

    copy_files_r(source, target)

def generate_page(basepath: str, from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown: str | None = None
    template: str | None = None

    with open(from_path) as markdown_file:
        markdown = markdown_file.read()

    with open(template_path) as template_file:
        template = template_file.read()

    html_string = markdown_to_html_node(markdown).to_html()
    html_title = extract_title(markdown)

    html_page = template.replace("{{ Title }}", html_title)
    html_page = html_page.replace("{{ Content }}", html_string)

    if basepath:
        html_page = html_page.replace('href="/', f'href="{basepath}')
        html_page = html_page.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w") as html_file:
        html_file.write(html_page)

def generate_pages_recursive(basepath: str, dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    if not os.path.exists(dir_path_content):
        raise OSError(f"Content folder '{dir_path_content}' was not found")
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for entry in os.listdir(dir_path_content):
        entry_content_path = dir_path_content + f"/{entry}"
        entry_html_write_path = dest_dir_path + f"/{entry.replace(".md",".html")}"

        if os.path.isdir(entry_content_path):
            generate_pages_recursive(basepath, entry_content_path, template_path, entry_html_write_path)
        elif os.path.isfile(entry_content_path):
            generate_page(basepath, entry_content_path, template_path, entry_html_write_path)
        else:
            raise OSError(f"The entry '{entry_content_path}' is not a file nor a directory")

def main():
    try:
        basepath = sys.argv[1]
    except IndexError:
        basepath = ""

    # copy_files("./static", "./public")
    copy_files("./static", "./docs")
    generate_pages_recursive(basepath, "content", "template.html", "docs")

main()
