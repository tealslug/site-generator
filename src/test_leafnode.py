import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("div", "This is a text node", {"class": "test"})
        node2 = LeafNode("div", "This is a text node", {"class": "test"})
        self.assertEqual(node, node2)

    def test_ne(self):
        node = LeafNode("div", "This is a text node", {"class": "test"})
        node2 = LeafNode("div", "This is a text node", {"class": "test2"})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = LeafNode("div", "This is a text node", {"class": "test"})
        self.assertEqual(repr(node), "LeafNode(div, This is a text node, {'class': 'test'})")

    def test_to_html(self):
        node = LeafNode("div", "This is a text node", {"class": "test"})
        self.assertEqual(node.to_html(), "<div class=\"test\">This is a text node</div>")
        