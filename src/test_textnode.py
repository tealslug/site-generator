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

    def test_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html_node_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html_node_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html_node_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html_node_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_to_html_node_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://example.com")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com"})


if __name__ == "__main__":
    unittest.main()