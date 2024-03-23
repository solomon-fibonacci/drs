from datetime import datetime
import json

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that converts datetime objects to ISO format strings."""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

def check_and_conditions(condition, doc):
    return all(condition[key](key, doc) for key in condition)

def check_or_conditions(condition, doc):
    return any(condition[key](key, doc) for key in condition)


def check_query_matches(doc, query_data):
    and_conditions = query_data.get("conditions", {}).get("$$", [])
    if and_conditions:
        for condition in and_conditions:
            if not check_and_conditions(condition, doc):
                return False

    or_conditions = query_data.get("conditions", {}).get("||", [])
    if or_conditions:
        if not check_or_conditions(or_conditions, doc):
            return False

    return True