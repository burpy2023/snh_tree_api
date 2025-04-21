from typing import Optional, List, ForwardRef
from sqlmodel import Field, SQLModel, Relationship
from pydantic import Field as PydanticField 
class TreeNode(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    label: str = Field(unique=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="treenode.id")
    children: List["TreeNode"] = Relationship(back_populates="parent")
    parent: Optional["TreeNode"] = Relationship(back_populates="children", sa_relationship_kwargs={"remote_side": "TreeNode.id"})
    
class TreeNodeCreate(SQLModel):
    label: str
    parentId: Optional[int] = None



class TreeNodeRead(SQLModel):
    id: int
    label: str
    parent_id: Optional[int] = None  # 👈 Add this
    children: List["TreeNodeRead"] = PydanticField(default_factory=list)
