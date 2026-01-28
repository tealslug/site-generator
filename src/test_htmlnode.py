import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "hello world")
        self.assertRaises(NotImplementedError, node.to_html)

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

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "Hello world", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

