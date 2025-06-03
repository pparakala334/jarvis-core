import os
import json
import uuid
from datetime import datetime

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"threads": {}}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def start_thread():
    thread_id = str(uuid.uuid4())
    memory = load_memory()
    memory["threads"][thread_id] = {
        "id": thread_id,
        "messages": [],
        "created_at": datetime.now().isoformat(),
        "last_active": datetime.now().isoformat()
    }
    save_memory(memory)
    return thread_id
