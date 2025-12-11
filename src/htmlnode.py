class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
            and self.children == other.children
        )

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return " " + " ".join([f"{key}={value}" for key, value in self.props.items()])
