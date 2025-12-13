import unittest

from processing import split_nodes_on
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

  def test_split_nodes_on_code(self):
    nodes = [TextNode("one `two` three", TextType.PLAIN)]
    new_nodes = split_nodes_on(nodes, "`", TextType.CODE)
    self.assertEqual(new_nodes, [TextNode("one ", TextType.PLAIN), TextNode("two", TextType.CODE), TextNode(" three", TextType.PLAIN)])
