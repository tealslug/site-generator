import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode("div", [ParentNode("div", [ParentNode("div", [])])], {"class": "test"})
        node2 = ParentNode("div", [ParentNode("div", [ParentNode("div", [])])], {"class": "test"})
        self.assertEqual(node, node2)

    def test_ne(self):
        node = ParentNode("div", [ParentNode("div", [ParentNode("div", [])])], {"class": "test"})
        node2 = ParentNode("div", [ParentNode("div", [ParentNode("div", [])])], {"class": "test2"})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = ParentNode("div", [ParentNode("div", [])], {"class": "test"})
        self.assertEqual(repr(node), "ParentNode(div, [ParentNode(div, [], None)], {'class': 'test'})")

    def test_to_html(self):
        node = ParentNode("div", [ParentNode("div", [ParentNode("div", [])])], {"class": "test"})
        self.assertEqual(node.to_html(), "<div class=\"test\"><div><div></div></div></div>")
        
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


if __name__ == "__main__":
    unittest.main()
