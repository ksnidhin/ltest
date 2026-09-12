import logging
from groq import AsyncGroq
from config import GROQ_API_KEY

# Initialize the Groq client
client = AsyncGroq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are a friendly, welcoming, and informative AI assistant.
Your goal is to answer the user's questions simply and directly.
DO NOT provide complex, lengthy explanations unless absolutely necessary.
Keep your tone polite and helpful."""

async def generate_response(user_text: str) -> str:
    """
    Sends the user's text to Groq and returns a simple, friendly response.
    """
    try:
        completion = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            model="llama3-8b-8192",  # Standard, highly available model
            temperature=0.7,
            max_tokens=300
        )
        
        answer = completion.choices[0].message.content
        return answer.strip()
    except Exception as e:
        logging.error(f"[GROQ] Error generating response: {e}")
        return "I'm sorry, I ran into a bit of trouble thinking of an answer. Please try again!"
