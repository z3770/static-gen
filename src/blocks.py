from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


def block_to_paragraph_node(block):
    # Replace newlines with spaces so multi-line paragraphs become one line
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def block_to_heading_node(block):
    level = 0
    for ch in block:
        if ch == "#":
            level += 1
        else:
            break
    text = block[level + 1:]  # skip "### "
    return ParentNode(f"h{level}", text_to_children(text))


def block_to_code_node(block):
    lines = block.split("\n")
    # Strip the opening ``` and closing ``` fence lines
    inner = "\n".join(lines[1:-1]) + "\n"
    code_node = LeafNode("code", inner)
    return ParentNode("pre", [code_node])


def block_to_quote_node(block):
    lines = block.split("\n")
    stripped = []
    for line in lines:
        if line.startswith("> "):
            stripped.append(line[2:])
        elif line.startswith(">"):
            stripped.append(line[1:])
        else:
            stripped.append(line)
    text = " ".join(stripped)
    return ParentNode("blockquote", text_to_children(text))


def block_to_ulist_node(block):
    items = []
    for line in block.split("\n"):
        text = line[2:]  # strip "- "
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)


def block_to_olist_node(block):
    items = []
    for i, line in enumerate(block.split("\n"), start=1):
        text = line[len(f"{i}. "):]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(block_to_paragraph_node(block))
        elif block_type == BlockType.HEADING:
            children.append(block_to_heading_node(block))
        elif block_type == BlockType.CODE:
            children.append(block_to_code_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(block_to_quote_node(block))
        elif block_type == BlockType.ULIST:
            children.append(block_to_ulist_node(block))
        elif block_type == BlockType.OLIST:
            children.append(block_to_olist_node(block))
    return ParentNode("div", children)
