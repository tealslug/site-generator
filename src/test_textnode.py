import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, 2, None)")

    def test_link_node(self):
        node = TextNode("Click me!", TextType.LINK, "https://example.com")
        node2 = TextNode("Click me!", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)
        self.assertEqual(repr(node), "TextNode(Click me!, 5, https://example.com)")

    def test_link_node_no_url(self):
        node = TextNode("Click me!", TextType.LINK)
        self.assertEqual(repr(node), "TextNode(Click me!, 5, None)")


if __name__ == "__main__":
    unittest.main()