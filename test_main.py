from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from main import app
from database import engine
from models import TreeNode

client = TestClient(app)

# Ensure the database is fresh for testing
def setup_module(module):
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def test_create_root_node():
    response = client.post("/api/tree", json={"label": "root"})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "root"
    assert data["children"] == []

def test_create_child_node():
    # Add root
    client.post("/api/tree", json={"label": "root2"})
    # Add child to root with id 2
    response = client.post("/api/tree", json={"label": "child", "parentId": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "child"
    assert data["parent_id"] == 2 or data["parentId"] == 2

def test_get_tree_structure():
    response = client.get("/api/tree")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(node["label"] == "root2" for node in data)

def test_create_with_invalid_parent():
    response = client.post("/api/tree", json={"label": "orphan", "parentId": 999})
    assert response.status_code == 400
    assert response.json()["detail"] == "Parent node not found"

def test_get_empty_tree():
    setup_module(None)  # Reset DB
    response = client.get("/api/tree")
    assert response.status_code == 200
    assert response.json() == []


def test_multiple_children_under_parent():
    client.post("/api/tree", json={"label": "multi-root"})
    client.post("/api/tree", json={"label": "child1", "parentId": 1})
    client.post("/api/tree", json={"label": "child2", "parentId": 1})

    response = client.get("/api/tree")
    assert response.status_code == 200
    data = response.json()
    children = data[0]["children"]
    labels = [c["label"] for c in children]
    assert "child1" in labels and "child2" in labels


def test_duplicate_labels_disallowed():
    client.post("/api/tree", json={"label": "unique"})
    response = client.post("/api/tree", json={"label": "unique"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Label must be unique"

def test_ml_suggestions_work():
    # Insert frog node
    create_response = client.post("/api/tree", json={"label": "frog"})
    assert create_response.status_code == 200
    frog_id = create_response.json()["id"]

    # Get suggestions for 'frog'
    response = client.get("/api/tree/smart-suggestions", params={"parentId": frog_id})
    assert response.status_code == 200
    suggestions = response.json()
    print("Suggestions returned:", suggestions)

    # Validate
    assert set(suggestions).intersection({"tadpole", "hop", "pond"})
