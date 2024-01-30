from msgspec import Struct
from typing import List, Optional, Union
class Header(Struct):
    level: int
    rich_text: List[RichText]

class ListItem(Struct):
    rich_text: List[RichText]
    children: Optional[List[BlockContent]] = None  # For nested lists

class ListBlock(Struct):
    items: List[ListItem]

class Quote(Struct):
    rich_text: List[RichText]

class Callout(Struct):
    rich_text: List[RichText]
    icon_url: Optional[str] = None

class CodeBlock(Struct):
    text: str
    language: str

class User(Struct):
    id: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None

class Text(Struct):
    content: str
    link: Optional[str] = None

class Annotations(Struct):
    bold: bool
    italic: bool
    strikethrough: bool
    underline: bool
    code: bool
    color: str

class RichText(Struct):
    type: str
    text: Text
    annotations: Annotations
    plain_text: str
    href: Optional[str] = None

class Paragraph(Struct):
    rich_text: List[RichText]
    color: str

class ToDo(Struct):
    rich_text: List[RichText]
    checked: bool

class Image(Struct):
    type: str
    image_url: str

BlockContent = Union[Paragraph, ToDo, Image, Header, ListBlock, Quote, Callout, CodeBlock]

class Block(Struct):
    object: str
    id: str
    created_time: str
    last_edited_time: str
    created_by: User
    last_edited_by: User
    has_children: bool
    archived: bool
    type: str
    content: Optional[BlockContent] = None

def extract_info(block: Block) -> dict:
    # Extend this function to handle new block types
    title = ""
    if isinstance(block.content, (Paragraph, Header, Quote, Callout)):
        title = " ".join([text.plain_text for text in block.content.rich_text])
    elif isinstance(block.content, ToDo):
        title = "ToDo: " + " ".join([text.plain_text for text in block.content.rich_text])
    elif isinstance(block.content, ListBlock):
        title = "List: " + "; ".join([" ".join([text.plain_text for text in item.rich_text]) for item in block.content.items])
    elif isinstance(block.content, CodeBlock):
        title = "Code: " + block.content.text[:30] + "..."  # Example: First 30 chars    if isinstance(block.content, Paragraph):
        title = " ".join([text.plain_text for text in block.content.rich_text])
    
    info = {
        "Title": title,
        "Block Type": block.type,
        "UUID": block.id
    }
    return info

def serialize_block(block: Block) -> dict:
    return block.asdict()

def deserialize_block(data: dict) -> Block:
    return Block(**data)
