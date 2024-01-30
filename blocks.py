from msgspec import Struct
from typing import List, Optional, Union
class Annotations(Struct):
    bold: bool
    italic: bool
    strikethrough: bool
    underline: bool
    code: bool
    color: str
class User(Struct):
    id: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None

class Text(Struct):
    content: str
    link: Optional[str] = None
class RichText(Struct):
    type: str
    text: Text
    annotations: Annotations
    plain_text: str
    href: Optional[str] = None
class Header(Struct):
    level: int
    rich_text: List[RichText]
class Image(Struct):
    type: str
    image_url: str
class CodeBlock(Struct):
    text: str
    language: str
class Quote(Struct):
    rich_text: List[RichText]
class Callout(Struct):
    rich_text: List[RichText]
    icon_url: Optional[str] = None
class Paragraph(Struct):
    rich_text: List[RichText]
    color: str
class ToDo(Struct):
    rich_text: List[RichText]
    checked: bool

BlockContent = Union[Paragraph, ToDo, Image, Header, Quote, Callout, CodeBlock]

class ListItem(Struct):
    rich_text: List[RichText]
    children: Optional[List[BlockContent]] = None # For nested lists

class ListBlock(Struct):
    items: List[ListItem]






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
    title_extractors = {
        Paragraph: lambda b: " ".join([text.plain_text for text in b.content.rich_text]),
        Header: lambda b: " ".join([text.plain_text for text in b.content.rich_text]),
        ToDo: lambda b: "ToDo: " + " ".join([text.plain_text for text in b.content.rich_text]),
        ListBlock: lambda b: "List: " + "; ".join([" ".join([text.plain_text for text in item.rich_text]) for item in b.content.items]),
        CodeBlock: lambda b: "Code: " + b.content.text[:30] + "...",
        # Add other block types here...
    }
    title = title_extractors.get(type(block.content), lambda b: "Unknown Block Type")(block)
    
    return {
        "Title": title,
        "Block Type": block.type,
        "UUID": block.id
    }


def serialize_block(block: Block) -> dict:
    return block.__dict__

def deserialize_block(data: dict) -> Block:
    return Block(**data)
