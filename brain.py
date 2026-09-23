from ollama import chat


conversation = [
    {
        "role": "system",
        "content": (
            "You are NOVA, a futuristic personal AI assistant. "
            "You are intelligent, calm, helpful and professional. "
            "Speak naturally like a JARVIS-style assistant. "
            "Keep normal answers concise unless the user asks for detail. "
            "Remember information from the current conversation. "
            "You may call the user sir occasionally, but do not overuse it."
        )
    }
]


def nova_brain(command):

    try:

        # Add user's message
        conversation.append({
            "role": "user",
            "content": command
        })

        response = chat(
            model="llama3.2:3b",
            messages=conversation
        )

        answer = response.message.content

        # Save NOVA's answer to memory
        conversation.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    except Exception as e:

        return f"Sorry sir, I encountered a problem: {e}"