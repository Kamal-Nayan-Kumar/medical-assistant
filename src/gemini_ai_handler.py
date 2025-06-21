import google.generativeai as genai

def generate_gemini_answer(api_key, query, context):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
You are a medical AI assistant. Answer the user's query using only the provided context from trusted sources. Cite sources using [number].

User Query: "{query}"

Context:
{context}

Answer:
"""
    response = model.generate_content(prompt)
    return response.text
