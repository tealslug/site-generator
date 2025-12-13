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