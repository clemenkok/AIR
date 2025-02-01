import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=[
        {
            "type": "computer_20241022",
            "name": "computer",
            "display_width_px": 1024,
            "display_heigh_px": 768,
            "display_number": 1,
        },
        {
            "type": "bash_20241022",
            "name": "bash"
        }
    ],
    messages=[{"role": "user", "content": "Run the jupyter notebook"}],
    betas=["computer-use-2024-10-22"],
)
print(response)