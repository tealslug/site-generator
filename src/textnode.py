from leafnode import LeafNode
from enum import Enum

class TextType(Enum):
    PLAIN = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6
    
class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def to_html_node(self) -> LeafNode:
        if self.text_type == TextType.PLAIN:
            return LeafNode(None, self.text)
        elif self.text_type == TextType.BOLD:
            return LeafNode("b", self.text)
        elif self.text_type == TextType.ITALIC:
            return LeafNode("i", self.text)
        elif self.text_type == TextType.CODE:
            return LeafNode("code", self.text)
        elif self.text_type == TextType.LINK:
            return LeafNode("a", self.text, {"href": self.url})
        elif self.text_type == TextType.IMAGE:
            return LeafNode("img", "", {"src": self.url})
        raise ValueError(f"Invalid text type: {self.text_type}")