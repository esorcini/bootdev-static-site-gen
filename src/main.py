import os
import shutil

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

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown: str | None = None
    template: str | None = None

    with open(from_path) as markdown_file:
        markdown = markdown_file.read()

    with open(template_path) as template_file:
        template = template_file.read()

    target_dir = os.path.dirname(dest_path)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    html_string = markdown_to_html_node(markdown).to_html()
    html_title = extract_title(markdown)

    html_page = template.replace("{{ Title }}", html_title)
    html_page = html_page.replace("{{ Content }}", html_string)

    with open(dest_path, "w") as html_file:
        html_file.write(html_page)

def main():
    copy_files("./static","./public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()
