import unittest

from src.model.enums import TextType
from src.model.textnode import TextNode
from src.textnodehelpers import text_node_to_html


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_links(self):
        node = TextNode("This is a link node", TextType.LINK, "www.somelink.com")
        node2 = TextNode("This is a link node", TextType.LINK, "www.somelink.com")
        self.assertEqual(node, node2)

    def test_neq_links(self):
        node = TextNode("This is a link node", TextType.LINK, "www.somelink.com")
        node2 = TextNode("This is a link node", TextType.LINK, "www.adifferentlink.com")
        self.assertNotEqual(node, node2)

    def test_neq_nodes(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.someurl.com")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertIn("www.someurl.com", html_node.props["href"])

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "www.imageurl.com")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "img")
        self.assertIn("This is an image node", html_node.props["alt"])
        self.assertIn("www.imageurl.com", html_node.props["src"])

if __name__ == "__main__":
    unittest.main()
