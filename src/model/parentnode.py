from src.model.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Parent nodes must have a tag")
        if self.children is None:
            raise ValueError("Parent nodes must have children")

        children_html = ""
        try:
            for children in self.children:
                children_html += children.to_html()
        except ValueError as ve:
            if str(ve) == "Parent nodes must have children":
                return ""

        return f'<{self.tag}{super().props_to_html()}>{children_html}</{self.tag}>'
