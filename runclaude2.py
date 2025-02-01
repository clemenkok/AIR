import os, anthropic, pathlib
output_path = pathlib.Path("AIR" + ".txt")

client = anthropic.Anthropic(  # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)

# def chunk_text(text, chunk_size=1000):
#     # Chunk the text into pieces that fit within the token limits
#     return [text[i:i + chunk_size * 4] for i in range(0, len(text), chunk_size * 4)]

list_of_txt = []
directory = "concurrency"
for fname in os.listdir(directory):
    if fname.lower().endswith('.txt'):
        file_path = os.path.join(directory, fname)
        with open(file_path, 'r') as file:
            file_content = file.read()
            list_of_txt.extend(file_content)

system_message = f"Here are the research papers:\n" + "\n".join([f"{i}. {txt}" for i, txt in enumerate(list_of_txt[:len(list_of_txt)])])

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=8000,
    temperature=0,
    system=system_message,
    messages=[
        {
            "role": "user",
            "content": [{"type": "text", "text": "Based on these papers, create a list of 5 possible research ideas sorted in descending order based on research impact. Explain their rationales and describe the methodology. Also, include references to where inspiration was derived from."}]
        }
    ]
)
output_text = message.content[0].text
# Process message.content into clean multiline text


# Join with proper line breaks


# Write the content as Python code to a .py file
output_path.write_text(output_text)