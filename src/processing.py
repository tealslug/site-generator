from src.htmlnode import HTMLNode
from src.parentnode import ParentNode
import re
from textnode import TextNode, TextType
from enum import Enum

IMAGE_RE = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
LINK_RE = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
HEADING_RE = r"^#{1,6} "
UNORDERED_LIST_RE = r"^[\*\-\+] "

def split_nodes_on(nodes: list[TextNode], split_on: str, text_type: TextType) -> list[TextNode]:
  new_nodes = []
  for node in nodes:
    if node.text_type != TextType.PLAIN:
      new_nodes.append(node)
      continue
    if split_on not in node.text:
      new_nodes.append(node)
      continue

    parts = node.text.split(split_on)
    if len(parts[0]) > 0:
      new_nodes.append(TextNode(parts[0], TextType.PLAIN))
    new_nodes.append(TextNode(parts[1], text_type))
    if len(parts[2]) > 0:
      new_nodes.append(TextNode(parts[2], TextType.PLAIN))

  return new_nodes

# Splits all regex pairs from a string.  By pairs we mean that the pattern
# should have two groups, with the first representing the text content of
# a node, and the second representing the url content of the node.  We then
# return a list of these split out nodes, along with any in-between text as 
# nodes of type PLAIN.  The text_type parameter is the type of the node to
# create for the matched pairs.
def split_nodes_on_regex(nodes: list[TextNode], regex: re.Pattern, text_type: TextType) -> list[TextNode]:
  new_nodes = []
  for node in nodes:
    found = []
    text = node.text

    while True:
      match = regex.search(text)
      if match is None:
        break
      # Add the text before the match
      if match.start() > 0:
        found.append(TextNode(text[:match.start()], TextType.PLAIN))
      found.append(TextNode(match.group(1), text_type, match.group(2)))
      text = text[match.end():]

    if found:
      if len(text) > 0:
        found.append(TextNode(text, TextType.PLAIN))
      new_nodes.extend(found)
    else:
      new_nodes.append(node)
    
  return new_nodes

def text_to_nodes(text: str) -> list[TextNode]:
  new_nodes = [TextNode(text, TextType.PLAIN)]
  new_nodes = split_nodes_on(new_nodes, "**", TextType.BOLD)
  new_nodes = split_nodes_on(new_nodes, "_", TextType.ITALIC)
  new_nodes = split_nodes_on(new_nodes, "`", TextType.CODE)
  new_nodes = split_nodes_on_regex(new_nodes, re.compile(IMAGE_RE), TextType.IMAGE)
  new_nodes = split_nodes_on_regex(new_nodes, re.compile(LINK_RE), TextType.LINK)
  return new_nodes

def markdown_to_blocks(markdown: str) -> list[str]:
  blocks = markdown.split("\n\n")
  result = []
  for block in blocks:
    val = block.strip()
    if val != "":
      result.append(val)
  return result

class BlockType(Enum):
  PARAGRAPH = 1
  HEADING = 2
  CODE = 3
  QUOTE = 4
  UNORDERED_LIST = 5
  ORDERED_LIST = 6
  
def block_to_block_type(block: str) -> BlockType:
  lines = block.split("\n")

  if re.match(HEADING_RE, block):
    return BlockType.HEADING

  if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
    return BlockType.CODE

  is_quote = True
  for line in lines:
    if not line.startswith(">"):
      is_quote = False
      break
  if is_quote:
    return BlockType.QUOTE

  is_unordered_list = True
  for line in lines:
    line = line.strip()
    if line == "":
      continue
    if not re.match(UNORDERED_LIST_RE, line):
      is_unordered_list = False
      break
  if is_unordered_list:
    return BlockType.UNORDERED_LIST

  is_ordered_list = True
  expected_num = 1
  for line in lines:
    line = line.strip()
    if line == "":
      continue
    if not line.startswith(f"{expected_num}. "):
      is_ordered_list = False
      break
    expected_num += 1
  if is_ordered_list:
    return BlockType.ORDERED_LIST

  return BlockType.PARAGRAPH

def text_to_html_nodes(text: str) -> list[HTMLNode]:
  text_nodes = text_to_nodes(text)
  children = []
  for text_node in text_nodes:
    html_node = text_node.to_html_node()
    children.append(html_node)
  return children

def paragraph_to_html_node(block: str) -> HTMLNode:
  lines = block.split("\n")
  paragraph = " ".join(lines)
  children = text_to_html_nodes(paragraph)
  return ParentNode("p", children)

def heading_to_html_node(block: str) -> HTMLNode:
  level = 0
  for char in block:
    if char != "#":
      break
    level += 1
  if level + 1 >= len(block):
    raise ValueError(f"Invalid heading level: {level}")
  text = block[level + 1 :]
  children = text_to_html_nodes(text)
  return ParentNode(f"h{level}", children)

def code_to_html_node(block: str) -> HTMLNode:
  if not block.startswith("```") or not block.endswith("```"):
    raise ValueError("invalid code block")

  text = block[4:-3]
  raw_text_node = TextNode(text, TextType.PLAIN)
  child = raw_text_node.to_html_node()
  code = ParentNode("code", [child])
  return ParentNode("pre", [code])

def ordered_list_to_html_node(block: str) -> HTMLNode:
  lines = block.split("\n")
  children = []
  for line in lines:
    parts = line.split(". ", 1)
    text = parts[1]
    nodes = text_to_html_nodes(text)
    children.append(ParentNode("li", nodes))
  return ParentNode("ol", children)

def unordered_list_to_html_node(block: str) -> HTMLNode:
  lines = block.split("\n")
  children = []
  for line in lines:
    text = line[2:]
    nodes = text_to_html_nodes(text)
    children.append(ParentNode("li", nodes))
  return ParentNode("ul", children)

def quote_to_html_node(block: str) -> HTMLNode:
  lines = block.split("\n")
  new_lines = []
  for line in lines:
    if not line.startswith(">"):
      raise ValueError("invalid quote block")
    new_lines.append(line.lstrip(">").strip())
  content = " ".join(new_lines)
  children = text_to_html_nodes(content)
  return ParentNode("blockquote", children)

def block_to_html_node(block: str) -> HTMLNode:
  block_type = block_to_block_type(block)
  if block_type == BlockType.PARAGRAPH:
    return paragraph_to_html_node(block)
  elif block_type == BlockType.HEADING:
    return heading_to_html_node(block)
  elif block_type == BlockType.CODE:
    return code_to_html_node(block)
  elif block_type == BlockType.QUOTE:
    return quote_to_html_node(block)
  elif block_type == BlockType.ORDERED_LIST:
    return ordered_list_to_html_node(block)
  elif block_type == BlockType.UNORDERED_LIST:
    return unordered_list_to_html_node(block)
  else:
    raise ValueError(f"Unknown block type: {block_type}")

def markdown_to_html_node(markdown: str) -> HTMLNode:
  blocks = markdown_to_blocks(markdown)
  children = []
  for block in blocks:
    html_node = block_to_html_node(block)
    children.append(html_node)
  return ParentNode("div", children, None)