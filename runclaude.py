import os, anthropic, pathlib
output_path = pathlib.Path("AIR" + ".py")

client = anthropic.Anthropic(  # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)

def chunk_text(text, chunk_size=1000):
    # Chunk the text into pieces that fit within the token limits
    return [text[i:i + chunk_size * 4] for i in range(0, len(text), chunk_size * 4)]

list_of_txt = []
directory = "concurrency"
for fname in os.listdir(directory):
    if fname.lower().endswith('.txt'):
        file_path = os.path.join(directory, fname)
        with open(file_path, 'r') as file:
            file_content = file.read()
            chunks = chunk_text(file_content)
            list_of_txt.extend(chunks)  # Add chunks to the list

system_message = f"Here are the research papers:\n" + "\n".join([f"{i+1}. {txt}" for i, txt in enumerate(list_of_txt[:3])])

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    temperature=0,
    system=system_message,
    messages=[
        {
            "role": "user",
            "content": [{"type": "text", "text": "Based on these papers, generate a research idea as a comment in a Python file and generate the Python code that conducts the experiment on this."}]
        }
    ]
)
# print(message.content)

# Process message.content into clean multiline text
output_lines = []
for block in message.content:
    if isinstance(block, dict) and block.get("type") == "text":
        output_lines.append(block.get("text", "").strip())

# Join with proper line breaks
formatted_output = "\n\n".join(output_lines)

# Write the content as Python code to a .py file
output_text = "# Generated Research Idea and Experiment Code\n\n" + formatted_output.strip() + "\n"
print(output_text)
output_path.write_text(output_text)






