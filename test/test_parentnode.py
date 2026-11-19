import unittest

from src.model.leafnode import LeafNode
from src.model.parentnode import ParentNode


class testParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        expected_html = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        node = ParentNode("p",[LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])
        parent_html = node.to_html()
        self.assertEqual(expected_html, parent_html)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
