import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from listen import capture_input
from speak import play_response
from brain import load_memory, save_memory, start_thread

# Load environment variables
load_dotenv()

# Constants
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Jarvis")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Helper to parse ISO time
def parse_time(t):
    try:
        return datetime.fromisoformat(str(t))
    except Exception:
        return datetime.min  # push invalid/missing timestamps to the bottom

def get_latest_thread_id(threads):
    valid_threads = {
        t_id: t_data
        for t_id, t_data in threads.items()
        if "last_active" in t_data
    }

    if not valid_threads:
        return start_thread()

    return max(valid_threads, key=lambda t: parse_time(valid_threads[t]["last_active"]))

# Get response from OpenAI
def respond_with_voice(messages):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )
    return response.choices[0].message.content

# Handle input, update memory, and return assistant response
def handle_request(user_input, thread_id=None):
    memory = load_memory()

    if not thread_id or thread_id not in memory.get("threads", {}):
        thread_id = start_thread()
        memory = load_memory()  # Reload to get new thread


    thread = memory["threads"][thread_id]
    thread["messages"].append({"role": "user", "content": user_input})
    thread["last_active"] = datetime.now().isoformat()
    if "created_at" not in thread:
        thread["created_at"] = thread["last_active"]

    reply = respond_with_voice(thread["messages"])
    thread["messages"].append({"role": "assistant", "content": reply})
    save_memory(memory)

    # Generate audio
    audio_path = play_response(reply)

    return reply, thread_id, audio_path

# CLI Mode
if __name__ == "__main__":
    print(f"{ASSISTANT_NAME} is online. Speak or type below.")
    memory = load_memory()
    thread_id = get_latest_thread_id(memory["threads"])

    while True:
        try:
            user_input = capture_input()
            if user_input.strip().lower() in ["exit", "quit"]:
                print("Shutting down.")
                break

            print(f"You: {user_input}")
            reply, thread_id = handle_request(user_input, thread_id)
            print(f"{ASSISTANT_NAME}: {reply}")
            play_response(reply)

        except KeyboardInterrupt:
            print("\nGoodbye.")
            break

__all__ = ["handle_request", "get_latest_thread_id"]