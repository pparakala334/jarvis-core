import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from brain import load_memory, save_memory, start_thread
from speak import generate_audio

# Load env vars
load_dotenv()
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Jarvis")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Parse ISO time for sorting
def parse_time(t):
    try:
        return datetime.fromisoformat(str(t))
    except Exception:
        return datetime.min

def get_latest_thread_id(memory):
    return max(memory["threads"], key=lambda k: memory["threads"][k]["last_active"])

def respond(messages):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )
    return response.choices[0].message.content

def handle_request(user_input, thread_id=None):
    memory = load_memory()

    # If provided thread_id is invalid or missing, default to latest or create new
    if thread_id not in memory["threads"]:
        if memory["threads"]:
            thread_id = get_latest_thread_id(memory)
        else:
            thread_id = start_thread()
            memory = load_memory()  # Refresh memory to include new thread

    thread = memory["threads"][thread_id]
    thread["messages"].append({"role": "user", "content": user_input})
    thread["last_active"] = datetime.now().isoformat()

    if "created_at" not in thread:
        thread["created_at"] = thread["last_active"]

    reply = respond(thread["messages"])
    thread["messages"].append({"role": "assistant", "content": reply})
    save_memory(memory)

    audio_path = generate_audio(reply)
    return reply, thread_id, audio_path
