import re
import unittest

from processing import split_nodes_on, split_nodes_on_regex, text_to_nodes, markdown_to_blocks, block_to_block_type, BlockType
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

  def test_markdown_to_blocks_empty(self):
    md = ""
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, [])

  def test_markdown_to_blocks_single(self):
    md = "This is a single block"
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, ["This is a single block"])

  def test_markdown_to_blocks_trailing_newline(self):
    md = "This is a single block\n"
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, ["This is a single block"])

  def test_markdown_to_blocks_leading_newline(self):
    md = "\nThis is a single block"
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, ["This is a single block"])

  def test_markdown_to_blocks_leading_and_trailing_newline(self):
    md = "\nThis is a single block\n"
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, ["This is a single block"])

  def test_markdown_to_blocks_single_multiline(self):
    md = """
This is a single block
with multiple lines
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, ["This is a single block\nwith multiple lines"])

  def test_markdown_to_blocks_typical(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

  def test_markdown_to_blocks_with_multiple_blank_lines(self):
    md = """
This is a single block



"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, ["This is a single block"])
  
  def test_block_to_block_type(self):
    self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("```"), BlockType.CODE)
    self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
    self.assertEqual(block_to_block_type("- List"), BlockType.UNORDERED_LIST)
    self.assertEqual(block_to_block_type("1. List"), BlockType.ORDERED_LIST)
    self.assertEqual(block_to_block_type("Paragraph"), BlockType.PARAGRAPH)
    self.assertEqual(block_to_block_type("Paragraph\nwith multiple lines"), BlockType.PARAGRAPH)
    self.assertEqual(block_to_block_type("```\nCode block\n```"), BlockType.CODE)

  def test_block_to_block_type_with_multiple_lines(self):
    self.assertEqual(block_to_block_type("# Heading\nwith multiple lines"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("```\nCode block\nwith multiple lines\n```"), BlockType.CODE)
    self.assertEqual(block_to_block_type("> Quote\n> with multiple lines\n> and another line"), BlockType.QUOTE)
    self.assertEqual(block_to_block_type("- List\n- with multiple lines\n- and another line"), BlockType.UNORDERED_LIST)
    self.assertEqual(block_to_block_type("1. List\n2. with multiple lines\n3. and another line"), BlockType.ORDERED_LIST)
    
  def test_block_to_block_type_complex_cases(self):
    self.assertEqual(block_to_block_type(" # Not a heading"), BlockType.PARAGRAPH)
    self.assertEqual(block_to_block_type("  > Not a quote"), BlockType.PARAGRAPH)
    self.assertEqual(block_to_block_type("```\njust a line\n```"), BlockType.CODE)
    self.assertEqual(block_to_block_type("```\n    indented code\n```"), BlockType.CODE)
    self.assertEqual(block_to_block_type("Paragraph with\n  multiple lines\nand some trailing spaces "), BlockType.PARAGRAPH)
    self.assertEqual(block_to_block_type("# Heading with extra space"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("```\n\n```"), BlockType.CODE) # Empty code block
    self.assertEqual(block_to_block_type("> Single line quote"), BlockType.QUOTE)
    self.assertEqual(block_to_block_type("    Just some indented text, not code block"), BlockType.PARAGRAPH)
  
  def test_block_to_block_type_unordered_list(self):
    self.assertEqual(block_to_block_type("- list item\n- another item\n"), BlockType.UNORDERED_LIST)
  
  def test_block_to_block_type_ordered_list(self):
    self.assertEqual(block_to_block_type("1. list item\n2. another item\n"), BlockType.ORDERED_LIST)

  def test_split_nodes_on_unmatched_delimiter(self):
    nodes = [TextNode("one **two three", TextType.PLAIN)]
    with self.assertRaises(Exception):
      split_nodes_on(nodes, "**", TextType.BOLD)

  def test_split_nodes_on_unmatched_delimiter_with_multiple_nodes(self):
    nodes = [TextNode("one **two three", TextType.PLAIN), TextNode("four", TextType.PLAIN)]
    with self.assertRaises(Exception):
      split_nodes_on(nodes, "**", TextType.BOLD)

  def test_block_to_block_type_heading_levels(self):
    self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)
