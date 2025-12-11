from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode tag cannot be None")
        if self.children is None:
            raise ValueError("ParentNode children cannot be None")
        return f"<{self.tag}{self.props_to_html()}>{self.children_to_html()}</{self.tag}>"
        
    def children_to_html(self) -> str:
        return "".join([child.to_html() for child in self.children])
    
    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ParentNode):
            return False
        return self.tag == other.tag and self.children == other.children and self.props == other.props
    
    def __ne__(self, other: object) -> bool:
        return not self == other