import unittest

from src.model.enums import BlockType, TextType
from src.model.textnode import TextNode
from src.textnodehelpers import *


class TestNodeHelpers(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected_list)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected_list)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with an _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_list = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected_list)

    def test_split_nodes_delimiter_multiple_bolds(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        node2 = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        expected_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected_list)

    def test_split_nodes_delimiter_TEXT_text(self):
        node = TextNode("Just TEXT text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_list = [
            TextNode("Just TEXT text", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected_list)

    def test_split_nodes_delimiter_bad_syntax(self):
        node = TextNode("This is text with an _italic block` word", TextType.TEXT)
        with self.assertRaises(InvalidMarkdownSyntax):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        result = extract_markdown_images(text)
        # print(f"expected: {expected_result}")
        # print(f"actual: {result}")
        self.assertListEqual(result, expected_result)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        result = extract_markdown_links(text)
        # print(f"expected: {expected_result}")
        # print(f"actual: {result}")
        self.assertListEqual(result, expected_result)

    def test_extract_markdown_link_on_normal_text(self):
        text = "This is text with normal text and no links"
        expected_result = []
        result = extract_markdown_links(text)
        # print(f"expected: {expected_result}")
        # print(f"actual: {result}")
        self.assertListEqual(result, expected_result)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # print(f"actual: {new_nodes}")
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("This is a normal text with no image links", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        # print(f"actual: {new_nodes}")
        self.assertListEqual(
            [TextNode("This is a normal text with no image links", TextType.TEXT)],
            new_nodes
        )

    def test_split_images_no_remaining_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # print(f"actual: {new_nodes}")
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

    def test_split_images_with_remaining_text_only(self):
        node = TextNode(
            "This is text with an image ![image](https://i.imgur.com/zjjcJKZ.png) and another text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # print(f"actual: {new_nodes}")
        self.assertListEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_with_remaining_text_only(self):
        node = TextNode(
            "This is text with a link [link text](https://i.imgur.com/zjjcJKZ.png) and another text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # print(f"actual: {new_nodes}")
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_nodes(self):
        input_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        nodes = text_to_textnodes(input_text)
        self.assertListEqual(nodes, expected_nodes)

    def test_text_to_nodes_inverted(self):
        input_text = " and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) This is **text** with an _italic_ word and a `code block`"
        expected_nodes = [
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
        ]
        nodes = text_to_textnodes(input_text)
        self.assertListEqual(nodes, expected_nodes)

    def test_text_to_nodes_mixed(self):
        input_text = "This is **text** with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and an _italic_ word and a `code block` and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        nodes = text_to_textnodes(input_text)
        self.assertListEqual(nodes, expected_nodes)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_double_lines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_heading_trailing_lines(self):
        md = """

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blocktype_heading_min(self):
        md = "# This is a heading"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_blocktype_heading_max(self):
        md = "###### This is a heading"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_blocktype_not_heading(self):
        md = "This is not a markdown heading"
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_to_blocktype_not_heading_syntax(self):
        md = "## "
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_to_blocktype_code(self):
        md = "```\na line of code```"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_blocktype_code_wrong_syntax_1(self):
        md = "```a line of code```"
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.CODE)

    def test_block_to_blocktype_code_wrong_syntax_2(self):
        md = "``` a line of code```"
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.CODE)

    def test_block_to_blocktype_quote_1(self):
        md = ">This is a quote line"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_blocktype_quote_2(self):
        md = "> This is a quote line"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_blocktype_quote_wrong_syntax_1(self):
        md = "This is not a quote line"
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.QUOTE)

    def test_block_to_blocktype_quote_wrong_syntax_2(self):
        md = ">"
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.QUOTE)

    def test_block_to_blocktype_u_list_min(self):
        md = "- line"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.U_LIST)

    def test_block_to_blocktype_u_list_max(self):
        md = "- line\n- line 2\n- line 3"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.U_LIST)

    def test_block_to_blocktype_u_list_wrong_syntax_1(self):
        md = "-line\n- line 2\n- line 3"
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.U_LIST)

    def test_block_to_blocktype_u_list_wrong_syntax_2(self):
        md = "- line\n-line 2\n- line 3"
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.U_LIST)

    def test_block_to_blocktype_u_list_wrong_syntax_3(self):
        md = "-line -line 2 - line 3"
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.U_LIST)

    def test_block_to_blocktype_o_list_min(self):
        md = "1. line"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.O_LIST)

    def test_block_to_blocktype_o_list_max(self):
        md = "1. line\n2. line2\n3. line3"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.O_LIST)

    def test_block_to_blocktype_o_list_wrong_syntax_1(self):
        md = "1. line\n3. line2\n4. line 3"
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.U_LIST)

    def test_block_to_blocktype_o_list_wrong_syntax_2(self):
        md = "1.line\n2. line2\n3. line 3"
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.U_LIST)

    def test_block_to_blocktype_o_list_wrong_syntax_3(self):
        md = "1. line\n3. line2\n4.line 3"
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.U_LIST)

    def test_block_to_blocktype_o_list_wrong_syntax_4(self):
        md = "1. line\n2. line2\n6. line 3"
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.U_LIST)

    def test_block_to_blocktype_normal_text(self):
        md = "This is a normal text line"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_markdown_to_html_heading_1(self):
        md = "# Title 1"
        expected_node = "<article><h1>Title 1</h1></article>"
        parent_node = markdown_to_html_node(md).to_html()
        self.assertEqual(parent_node, expected_node)

    def test_markdown_to_html_heading_6(self):
        md = "###### Title"
        expected_node = "<article><h6>Title</h6></article>"
        parent_node = markdown_to_html_node(md).to_html()
        self.assertEqual(parent_node, expected_node)

    def test_markdown_to_html_heading_faulty(self):
        md = "Title without bangs"
        expected_node = "<article><h1>Title 1</h1></article>"
        parent_node = markdown_to_html_node(md).to_html()
        self.assertNotEqual(parent_node, expected_node)

    def test_markdown_to_html_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        expected_node = "<article><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></article>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,expected_node)

    def test_markdown_to_html_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        expected_node = "<article><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></article>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,expected_node)



    def test_markdown_to_html_blockquotes(self):
        md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""
        expected_node = '<article><blockquote>"I am in fact a Hobbit in all but size."  -- J.R.R. Tolkien</blockquote></article>'

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,expected_node)

    def test_markdown_to_html_u_list(self):
        md = """
- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy
"""
        expected_node = "<ul><li>You can spend years studying the legendarium and still not understand its depths</li><li>It can be enjoyed by children and adults alike</li><li>Disney <i>didn't ruin it</i> (okay, but Amazon might have)</li><li>It created an entirely new genre of fantasy</li></ul>"
        node = markdown_to_u_list(md)
        html = node.to_html()
        self.assertEqual(html,expected_node)

    def test_markdown_to_html_o_list(self):
        md = """
1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn
    """
        expected_node = "<ol><li>Gandalf</li><li>Bilbo</li><li>Sam</li><li>Glorfindel</li><li>Galadriel</li><li>Elrond</li><li>Thorin</li><li>Sauron</li><li>Aragorn</li></ol>"
        node = markdown_to_o_list(md)
        html = node.to_html()
        self.assertEqual(html,expected_node)

    def test_extract_title(self):
        md = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
        """

        expected = "Tolkien Fan Club"
        title = extract_title(md)
        self.assertEqual(title, expected)

    def test_extract_title_faulty(self):
        md = """
![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
    """

        with self.assertRaises(InvalidMarkdownSyntax):
            title = extract_title(md)
