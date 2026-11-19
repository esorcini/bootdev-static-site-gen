import unittest

from src.model.htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {"color":"red", "font-size":"16px"}
        node = HTMLNode("h1", "Hello World", None, props)
        formatted_props = ' color="red" font-size="16px"'
        printed_props = node.props_to_html()
        self.assertEqual(formatted_props, printed_props)

    def test_faulty_props_to_html(self):
        props = {"color":"red", "font-size":"16px"}
        node = HTMLNode("h1", "Hello World", None, props)
        formatted_props = ' color="blue" font-size="16px"'
        printed_props = node.props_to_html()
        self.assertNotEqual(formatted_props, printed_props)

    def test_repr(self):
        node = HTMLNode("h1", "Hello World", None, None)
        self.assertIn("tag", node.__repr__())

    def test_faulty_repr(self):
        node = HTMLNode("h1", "Hello World", None, None)
        self.assertNotIn("someText", node.__repr__())

if __name__ == "__main__":
    unittest.main()
