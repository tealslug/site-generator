import re
from textnode import TextNode, TextType

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
    new_nodes.append(TextNode(parts[0], TextType.PLAIN))
    new_nodes.append(TextNode(parts[1], text_type))
    new_nodes.append(TextNode(parts[2], TextType.PLAIN))

  return new_nodes

# Extracts all regex pairs from a string.  By pairs we mean that the pattern
# should have two groups, and we return a list of those groups.
def extract_regex_pairs(text: str, regex: re.Pattern) -> list[(str, str)]:
  found = []
  while True:
    match = regex.search(text)
    if match is None:
      break
    found.append(match.groups())
    text = text[match.end():]

  return found

def extract_markdown_images(text: str) -> list[(str, str)]:
  return extract_regex_pairs(text, re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"))

def extract_markdown_links(text: str) -> list[(str, str)]:
  return extract_regex_pairs(text, re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"))
