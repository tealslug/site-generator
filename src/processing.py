import re
from textnode import TextNode, TextType

IMAGE_RE = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
LINK_RE = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

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