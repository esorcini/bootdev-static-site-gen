from __future__ import annotations


class HTMLNode:
    def __init__(
            self, tag: str|None = None,
            value: str|None = None,
            children: list[HTMLNode]|None = None,
            props: dict[str,str]|None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        formatted_props = ""
        for key, value in self.props.items():
            formatted_props += f' {key}="{value}"'

        return formatted_props

    def __repr__(self) -> str:
        html_node = f"tag: {self.tag}" if self.tag else ""
        html_node += f"value: {self.value}" if self.tag else ""

        if self.children:
            for children in self.children:
                html_node += f"child: {children.__repr__()}"

        html_node += f"props: {self.props_to_html()}" if self.tag else ""

        return html_node
