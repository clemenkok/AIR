import os, anthropic, pathlib
output_path = pathlib.Path("AIR.txt")

client = anthropic.Anthropic(  # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)

def chunk_text(text, chunk_size=500):
    # Chunk the text into pieces that fit within the token limits
    return [text[i:i + chunk_size * 4] for i in range(0, len(text), chunk_size * 4)]

list_of_txt = []
directory = "newest_hash"
for fname in os.listdir(directory):
    if fname.lower().endswith('.txt'):
        file_path = os.path.join(directory, fname)
        with open(file_path, 'r') as file:
            file_content = file.read()
            chunks = chunk_text(file_content)
            list_of_txt.extend(chunks)

def chat_with_Claude(prompt, list_of_txt): #change to buttons guys
    if prompt.isdigit():
        idea_number = int(prompt)
        if idea_number <= 0 or idea_number > 5:
            return output_text == "ERROR, invalid idea number"
        else:
            prompt = f"From the list of research ideas generated just now, generate the python code based on the research idea number {idea_number}"
            system_message = []
    else:
        prompt = """Based on these papers, create a list of 5 new and original possible ideas for cryptographic hashes. Explain their viability and describe the methodology. Also, include references
            to where inspiration was derived from."""
        system_message = f"Here are the research papers:\n" + "\n".join([f"{i}. {txt}" for i, txt in enumerate(list_of_txt[:len(list_of_txt)])])

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8000,
        temperature=0,
        system=system_message,
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]
    )
    return response

while True: 
    user_input = input("Generate research ideas or generate code (input idea number)?")
    if user_input == "exit":
        output_text = "Exiting conversation"
        break
    
    response = chat_with_Claude(user_input, list_of_txt)
    output_text = response.content[0].text
    output_path.write_text(output_text)
    print("Done")






