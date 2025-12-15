import re
import unittest

from processing import split_nodes_on, split_nodes_on_regex, text_to_nodes
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

  def test_split_nodes_on_with_empty_input(self):
    nodes = []
    new_nodes = split_nodes_on(nodes, "`", TextType.CODE)
    self.assertEqual(new_nodes, [])
  
  def test_split_nodes_on_regex_markdown_images_single(self):
    nodes = [TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.PLAIN)]
    new_nodes = split_nodes_on_regex(nodes, re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"), TextType.IMAGE)
    self.assertEqual(new_nodes, [TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")])

  def test_split_nodes_on_regex_markdown_images_multiple(self):
    nodes = [TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.PLAIN)]
    new_nodes = split_nodes_on_regex(nodes, re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"), TextType.IMAGE)
    self.assertEqual(new_nodes, [TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")])

  def test_split_nodes_on_regex_extract_markdown_images_none(self):
    nodes = [TextNode("this text doesn't have any images", TextType.PLAIN)]
    new_nodes = split_nodes_on_regex(nodes, re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"), TextType.IMAGE)
    self.assertEqual(new_nodes, nodes)
  
  def test_split_nodes_on_regex_extract_markdown_links_single(self):
    nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev)" , TextType.PLAIN)]
    new_nodes = split_nodes_on_regex(nodes, re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"), TextType.LINK)
    self.assertEqual(new_nodes, [TextNode("This is text with a link ", TextType.PLAIN), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")])
  
  def test_split_nodes_on_regex_markdown_links_multiple(self):
    nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)" , TextType.PLAIN)]
    new_nodes = split_nodes_on_regex(nodes, re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"), TextType.LINK)
    self.assertEqual(new_nodes, [TextNode("This is text with a link ", TextType.PLAIN), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode(" and ", TextType.PLAIN), TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")])
  
  def test_split_nodes_on_regex_markdown_links_none(self):
    nodes = [TextNode("this text doesn't have any links", TextType.PLAIN)]
    new_nodes = split_nodes_on_regex(nodes, re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"), TextType.LINK)
    self.assertEqual(new_nodes, nodes)

  def test_split_nodes_on_regex_markdown_links(self):
    nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)" , TextType.PLAIN)]
    new_nodes = split_nodes_on_regex(nodes, re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"), TextType.LINK)
    self.assertEqual(new_nodes, [TextNode("This is text with a link ", TextType.PLAIN), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode(" and ", TextType.PLAIN), TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")])

  def test_split_nodes_on_regex_markdown_images(self):
    nodes = [TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and trailing text", TextType.PLAIN)]
    new_nodes = split_nodes_on_regex(nodes, re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"), TextType.IMAGE)
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode(" and trailing text", TextType.PLAIN),
        ],
        new_nodes,
    )

  def test_split_nodes_on_regex_doesnt_alter_input_when_no_match(self):
    nodes = [TextNode("one ", TextType.PLAIN), TextNode("two", TextType.ITALIC), TextNode(" three", TextType.PLAIN)]
    new_nodes = split_nodes_on_regex(nodes, re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"), TextType.IMAGE)
    self.assertEqual(new_nodes, nodes)

  def test_text_to_nodes(self):
    nodes = text_to_nodes("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and trailing text")
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode(" and trailing text", TextType.PLAIN),
        ],
        nodes,
    )
  
  def test_text_to_nodes_all_types(self):
    nodes = text_to_nodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    self.assertListEqual(
        [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
        nodes,
    )