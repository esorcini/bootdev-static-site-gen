import unittest

from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        props = {"color":"red", "font-size":"16px"}
        expected_leaf_node = '<h1 color="red" font-size="16px">Hello World</h1>'
        node = LeafNode("h1", "Hello World", props)
        html_leaf = node.to_html()
        self.assertEqual(expected_leaf_node, html_leaf)

    def test_faulty_leaf_to_html(self):
            props = {"color":"red", "font-size":"16px"}
            node = LeafNode("h1", "Hello World", props)
            faulty_leaf = '<h1 color="blue" font-size="16px">Hello World</h1>'
            html_leaf = node.props_to_html()
            self.assertNotEqual(html_leaf, faulty_leaf)

    def test_repr(self):
        node = LeafNode("h1", "Hello World", None)
        self.assertIn("tag", node.__repr__())

    def test_repr_w_props(self):
        node = LeafNode("h1", "Hello World", {"color":"red", "font-size":"16px"})
        result_text = node.__repr__()
        self.assertIn("tag", result_text)
        self.assertIn("props", result_text)

    def test_empty_leaf_error(self):
        node = LeafNode("h1", "Hello World")
        node.value = None
        with self.assertRaises(ValueError) as cm:
            node.to_html()
            self.assertIs(type(cm.exception), ValueError)

    def test_empty_leaf_msg(self):
        node = LeafNode("h1", "Hello World")
        node.value = None
        with self.assertRaises(ValueError) as cm:
            node.to_html()
            self.assertEqual(cm.msg, "All leaf nodes must have a value")

if __name__ == "__main__":
    unittest.main()
