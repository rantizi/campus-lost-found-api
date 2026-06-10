from flask import Blueprint, jsonify, request
from app.data import items

api = Blueprint("api", __name__)

def success_response(message, data=None, status_code=200):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status_code

def error_response(message, status_code=400):
    return jsonify({
        "success": False,
        "message": message,
        "data": None
    }), status_code

@api.route("/", methods=["GET"])
def home():
    return success_response("Campus Lost & Found API is running")

@api.route("/health", methods=["GET"])
def health_check():
    return success_response("API health check success", {
        "status": "healthy"
    })

@api.route("/api/items", methods=["GET"])
def get_all_items():
    return success_response("Items retrieved successfully", items)

@api.route("/api/items/<int:item_id>", methods=["GET"])
def get_item_by_id(item_id):
    item = next((item for item in items if item["id"] == item_id), None)

    if item is None:
        return error_response("Item not found", 404)

    return success_response("Item retrieved successfully", item)

@api.route("/api/items", methods=["POST"])
def create_item():
    data = request.get_json()

    if not data:
        return error_response("Request body must be JSON", 400)

    required_fields = ["name", "category", "status", "location", "contact"]

    for field in required_fields:
        if field not in data or not data[field]:
            return error_response(f"{field} is required", 400)

    allowed_status = ["lost", "found", "claimed"]

    if data["status"] not in allowed_status:
        return error_response("Status must be lost, found, or claimed", 400)

    new_id = items[-1]["id"] + 1 if items else 1

    new_item = {
        "id": new_id,
        "name": data["name"],
        "category": data["category"],
        "status": data["status"],
        "location": data["location"],
        "description": data.get("description", ""),
        "contact": data["contact"]
    }

    items.append(new_item)

    return success_response("Item created successfully", new_item, 201)

@api.route("/api/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()

    if not data:
        return error_response("Request body must be JSON", 400)

    item = next((item for item in items if item["id"] == item_id), None)

    if item is None:
        return error_response("Item not found", 404)

    allowed_status = ["lost", "found", "claimed"]

    if "status" in data and data["status"] not in allowed_status:
        return error_response("Status must be lost, found, or claimed", 400)

    item["name"] = data.get("name", item["name"])
    item["category"] = data.get("category", item["category"])
    item["status"] = data.get("status", item["status"])
    item["location"] = data.get("location", item["location"])
    item["description"] = data.get("description", item["description"])
    item["contact"] = data.get("contact", item["contact"])

    return success_response("Item updated successfully", item)

@api.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)

    if item is None:
        return error_response("Item not found", 404)

    items.remove(item)

    return success_response("Item deleted successfully", item)