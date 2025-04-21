from sqlmodel import Session, select
from models import TreeNode, TreeNodeCreate
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

def create_node(session: Session, data: TreeNodeCreate):
    parent_id = data.parentId if data.parentId not in [0, None] else None

    if parent_id is not None:
        parent = session.get(TreeNode, parent_id)
        if not parent:
            raise HTTPException(status_code=400, detail="Parent node not found")

    node = TreeNode(label=data.label, parent_id=parent_id)
    session.add(node)
    try:
        session.commit()
        session.refresh(node)
        node.children
        return node
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Label must be unique")



def get_full_tree(session: Session):
    def build_tree(node):
        node.children = [build_tree(child) for child in session.exec(select(TreeNode).where(TreeNode.parent_id == node.id)).all()]
        return node

    roots = session.exec(select(TreeNode).where(TreeNode.parent_id == None)).all()
    return [build_tree(root) for root in roots]
