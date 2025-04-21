# snh_tree_api
 Simple SNH project

# Running the code
python -m venv venv
uvicorn main:app --reload

# this launches the app on local server port 8000. You can use your browser to hit the endpoints from 

127.0.0.1:8000/docs

# press the try it out button on the get and post api to send custom requests

# running the unit tests

pytest test_main.py


# test coverage
test_create_root_node                  -> Tests creating a node without a parent
test_create_child_node                 -> Tests creating a child node under an existing parent
test_get_tree_structure                -> Ensures full tree is returned in nested structure format
test_create_with_invalid_parent       -> Ensures creating a node with a non-existent parentId is rejected
test_get_empty_tree                    -> Verifies that the server returns an empty list when no tree exists
test_multiple_children_under_parent   -> Tests that a parent can have multiple children
test_duplicate_labels_disallowed      -> Ensures that labels are unique and duplicate labels are rejected gracefully
