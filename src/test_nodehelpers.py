import unittest

from src.enums import BlockType
from src.textnode import TextNode, TextType
from src.textnodehelpers import InvalidMarkdownSyntax, block_to_block_type, extract_markdown_images, extract_markdown_links, markdown_to_blocks, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


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
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

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
