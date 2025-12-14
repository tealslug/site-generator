import unittest

from processing import split_nodes_on, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestProcessing(unittest.TestCase):
  def test_split_nodes_on(self):
    nodes = [TextNode("one **two** three", TextType.PLAIN)]
    new_nodes = split_nodes_on(nodes, "**", TextType.BOLD)
    self.assertEqual(new_nodes, [TextNode("one ", TextType.PLAIN), TextNode("two", TextType.BOLD), TextNode(" three", TextType.PLAIN)])

  def test_split_nodes_on_italic(self):
    nodes = [TextNode("one _two_ three", TextType.PLAIN)]
    new_nodes = split_nodes_on(nodes, "_", TextType.ITALIC)
    self.assertEqual(new_nodes, [TextNode("one ", TextType.PLAIN), TextNode("two", TextType.ITALIC), TextNode(" three", TextType.PLAIN)])

  def test_split_nodes_on_with_empty_string(self):
    nodes = [TextNode("one __ three", TextType.PLAIN)]
    new_nodes = split_nodes_on(nodes, "_", TextType.ITALIC)
    self.assertEqual(new_nodes, [TextNode("one ", TextType.PLAIN), TextNode("", TextType.ITALIC), TextNode(" three", TextType.PLAIN)])

  def test_split_nodes_on_with_no_match(self):
    nodes = [TextNode("one two three", TextType.PLAIN)]
    new_nodes = split_nodes_on(nodes, "_", TextType.ITALIC)
    self.assertEqual(new_nodes, [TextNode("one two three", TextType.PLAIN)])

  def test_delim_bold_and_italic(self):
    node = TextNode("**bold** and _italic_", TextType.PLAIN)
    new_nodes = split_nodes_on([node], "**", TextType.BOLD)
    new_nodes = split_nodes_on(new_nodes, "_", TextType.ITALIC)
    self.assertEqual(
      [
        TextNode("bold", TextType.BOLD),
        TextNode(" and ", TextType.PLAIN),
        TextNode("italic", TextType.ITALIC),
      ],
      new_nodes,
    )

  def test_split_nodes_on_code(self):
    nodes = [TextNode("one `two` three", TextType.PLAIN)]
    new_nodes = split_nodes_on(nodes, "`", TextType.CODE)
    self.assertEqual(new_nodes, [TextNode("one ", TextType.PLAIN), TextNode("two", TextType.CODE), TextNode(" three", TextType.PLAIN)])

  def test_extract_markdown_images_single(self):
    text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)"
    self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

  def test_extract_markdown_images_multiple(self):
    text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

  def test_extract_markdown_images_none(self):
    text = "this text doesn't have any images"
    self.assertEqual(extract_markdown_images(text), [])
  
  def test_extract_markdown_links_single(self):
    text = "This is text with a link [to boot dev](https://www.boot.dev)"
    self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev")])
  
  def test_extract_markdown_links_multiple(self):
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
  
  def test_extract_markdown_links_none(self):
    text = "this text doesn't have any links"
    self.assertEqual(extract_markdown_links(text), [])