import re

from src.model.enums import BlockType, TextType
from src.model.htmlnode import HTMLNode
from src.model.leafnode import LeafNode
from src.model.parentnode import ParentNode
from src.model.textnode import NonSupportedNodeError, TextNode


class InvalidMarkdownSyntax(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def text_node_to_html(text_node: TextNode) -> LeafNode:
    if text_node.text_type not in TextType:
        raise NonSupportedNodeError("Node type is not supported")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href" : f'"{text_node.url}"'})
        case TextType.IMAGE:
            return LeafNode("img", "", {
                "src": f'"{text_node.url}"',
                "alt": f'"{text_node.text}"'
            })

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    stack = []
    nodes_list = []

    for node in old_nodes:
        # Only try to split TEXT nodes, directly append all the other node types
        if node.text_type != TextType.TEXT:
            nodes_list.append(node)
            continue

        text = node.text

        while True:
            if not text:
                break

            tmp = text.split(delimiter, maxsplit=1)

            if not stack:
                # Searching for opening delimiter
                nodes_list.append(TextNode(tmp[0], TextType.TEXT))
                stack.append(delimiter)
            else:
                # Searching for closing delimiter
                if delimiter not in text:
                    raise InvalidMarkdownSyntax(f"Invalid markdown: the closing {delimiter} was not found")
                nodes_list.append(TextNode(tmp[0], text_type))
                stack.remove(delimiter)

            try:
                text = tmp[1]
            except IndexError:
                break

        stack = []

    return nodes_list

def extract_markdown_images(text) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes_list = []

    for node in old_nodes:
        # Only try to split TEXT nodes, directly append all the other node types
        if node.text_type != TextType.TEXT:
            nodes_list.append(node)
            continue

        text = node.text
        img_links = extract_markdown_images(text)

        if len(img_links) == 0:
            nodes_list.append(node)
            continue

        for img_alt, img_url in img_links:
            separator = f"![{img_alt}]({img_url})"

            tmp = text.split(separator, maxsplit=1)

            nodes_list.append(TextNode(tmp[0], TextType.TEXT))
            nodes_list.append(TextNode(img_alt, TextType.IMAGE, img_url))

            try:
                text = tmp[1]
            except IndexError:
                break

        # Append a node with any remainder text after the last link found
        if text:
            nodes_list.append(TextNode(text, TextType.TEXT))

    return nodes_list

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes_list = []

    for node in old_nodes:
        # Only try to split TEXT nodes, directly append all the other node types
        if node.text_type != TextType.TEXT:
            nodes_list.append(node)
            continue

        text = node.text
        img_links = extract_markdown_links(text)

        if len(img_links) == 0:
            nodes_list.append(node)
            continue

        for img_alt, img_url in img_links:
            separator = f"[{img_alt}]({img_url})"

            tmp = text.split(separator, maxsplit=1)

            nodes_list.append(TextNode(tmp[0], TextType.TEXT))
            nodes_list.append(TextNode(img_alt, TextType.LINK, img_url))

            try:
                text = tmp[1]
            except IndexError:
                break

        # Append a node with any remainder text after the last link found
        if text:
            nodes_list.append(TextNode(text, TextType.TEXT))

    return nodes_list

def text_to_textnodes(text: str) -> list[TextNode]:
    initial_text_node = TextNode(text, TextType.TEXT)
    nodes = []

    nodes = split_nodes_delimiter([initial_text_node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    block_list = []

    if not markdown:
        return block_list

    tmp = markdown.split("\n\n")

    for block in tmp:
        block = block.strip()
        if block != "":
            block_list.append(block)

    return block_list

def is_heading(block: str) -> bool:
    return (
        block.startswith(("#", "##", "###", "####", "#####", "######"))
        and len(block.split(maxsplit=1)) > 1
    )

def is_code(block: str) -> bool:
    return block.startswith("```\n") and block.endswith("```")

def is_quote(block: str) -> bool:
    return block.startswith(">") and len(block.split(" ", maxsplit=1)) > 1

def is_unordered_list(block: str) -> bool:
    result = False
    tmp_lines = block.split("\n")
    for line in tmp_lines:
        if not line.startswith("- "):
            return False
        result = True
    return result

def is_ordered_list(block: str) -> bool:
    result = False
    tmp_lines = block.split("\n")

    if not tmp_lines[0].startswith("1. "):
        return False

    for index, line in enumerate(tmp_lines):
        try:
            tmp_lines[index - 1]
        except IndexError:
            continue

        if not line.startswith(f"{index + 1}. "):
            return False
        result = True

    return result

def block_to_block_type(block: str) -> BlockType:
    if is_heading(block):
        return BlockType.HEADING
    elif is_code(block):
        return BlockType.CODE
    elif is_quote(block):
        return BlockType.QUOTE
    elif is_unordered_list(block):
        return BlockType.U_LIST
    elif is_ordered_list(block):
        return BlockType.O_LIST
    return BlockType.PARAGRAPH

def markdown_to_heading(block: str) -> LeafNode:
    # tag -> which h tag depending on the number of #
    # value -> the text after the space
    tmp = block.split(maxsplit=1)
    tag = f"h{tmp[0].count("#")}"
    value = tmp[1]
    return LeafNode(tag, value)

def markdown_to_code_block(block: str) -> ParentNode:
    parent_tag = "pre"
    children: list[HTMLNode] = []

    tmp_lines = block.split("\n")
    tmp_lines = tmp_lines[1:-1]
    code_str = ""

    for line in tmp_lines:
        code_str += f"{line.strip()}\n"

    code_node = TextNode(code_str, TextType.CODE)
    children.append(text_node_to_html(code_node))

    return ParentNode(parent_tag, children)

def markdown_to_paragraph(block: str) -> ParentNode:
    parent_tag = "p"
    clean_block = block.replace("\n"," ")
    inline_nodes = text_to_textnodes(clean_block)
    paragraph_nodes: list[HTMLNode] = [ text_node_to_html(node) for node in inline_nodes]
    return ParentNode(parent_tag, paragraph_nodes)

def markdown_to_quoteblock(block: str) -> ParentNode:
    parent_tag = "blockquote"
    quote_lines = block.split("\n")
    clean_quote_lines = [ line.replace(">","").strip() for line in quote_lines]
    inline_nodes = text_to_textnodes(" ".join(clean_quote_lines))
    blockquote_nodes: list[HTMLNode] = [ text_node_to_html(node) for node in inline_nodes]
    return ParentNode(parent_tag, blockquote_nodes)

def markdown_to_u_list(block: str) -> ParentNode:
    parent_tag = "ul"
    quote_lines = block.strip().split("\n")
    clean_quote_lines = [ line.replace("-","").strip() for line in quote_lines]
    children: list[HTMLNode] = []
    for line in clean_quote_lines:
        inline_nodes = text_to_textnodes(line)
        inline_html_nodes: list[HTMLNode] = [ text_node_to_html(node) for node in inline_nodes ]
        list_line = ParentNode("li", inline_html_nodes)
        children.append(list_line)
    return ParentNode(parent_tag, children)

def markdown_to_o_list(block: str) -> ParentNode:
    parent_tag = "ol"
    quote_lines = block.strip().split("\n")
    clean_quote_lines = [ re.sub(r"\d+\. ","",line,count=1) for line in quote_lines]
    children: list[HTMLNode] = []
    for line in clean_quote_lines:
        inline_nodes = text_to_textnodes(line)
        inline_html_nodes: list[HTMLNode] = [ text_node_to_html(node) for node in inline_nodes ]
        list_line = ParentNode("li", inline_html_nodes)
        children.append(list_line)
    return ParentNode(parent_tag, children)

def markdown_to_html_node(markdown) -> ParentNode:
    root_tag = "article"
    blocks = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.HEADING:
                node = markdown_to_heading(block)
                children.append(node)
            case BlockType.CODE:
                node = markdown_to_code_block(block)
                children.append(node)
            case BlockType.PARAGRAPH:
                node = markdown_to_paragraph(block)
                children.append(node)
            case BlockType.QUOTE:
                node = markdown_to_quoteblock(block)
                children.append(node)
            case BlockType.U_LIST:
                node = markdown_to_u_list(block)
                children.append(node)
            case BlockType.O_LIST:
                node = markdown_to_o_list(block)
                children.append(node)

    return ParentNode(root_tag, children)

def extract_title(markdown) -> str:
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        lines = block.split("\n")

        for line in lines:
            if line.startswith("# "):
                return line.replace("# ", "")

    raise InvalidMarkdownSyntax("Markdown must have a main header #")
