import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "This is a text node", [HTMLNode("p", "This is a paragraph")], {"class": "test"})
        node2 = HTMLNode("div", "This is a text node", [HTMLNode("p", "This is a paragraph")], {"class": "test"})
        self.assertEqual(node, node2)

    def test_ne(self):
        node = HTMLNode("div", "This is a text node", [HTMLNode("p", "This is a paragraph")], {"class": "test"})
        node2 = HTMLNode("div", "This is a text node", [HTMLNode("p", "This is a paragraph")], {"class": "test2"})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("div", "This is a text node", [HTMLNode("p", "This is a paragraph")], {"class": "test"})
        self.assertEqual(repr(node), "HTMLNode(div, This is a text node, [HTMLNode(p, This is a paragraph, None, None)], {'class': 'test'})")

