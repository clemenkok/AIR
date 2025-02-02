import anthropic 
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

app = FastAPI()
origins = [
    "http://localhost:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = anthropic.Anthropic(  # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)

def stream_claude_client(prompt: str):
    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8000,
        temperature=1,
        system=prompt,
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ],
    ) as stream:
        for event in stream:
            if event.type == "content_block_delta":
                yield event.delta.text

class Outline(BaseModel):
    title: str
    abstract: str

class Outlines(BaseModel):
    data: list[Outline]

@app.post("/generate_outline")
async def generate_outline(outline: Outlines):
    # Extract the data from the request
    data = outline.data
    formatted_data = ""

    for item in data:
        formatted_data += f"""
            {item.title}: {item.abstract}
        """

    prompt = f"""
        Generate an experimental outline for the following research paper.
        
        Involve the following ideas, including their titles and abstracts to form a basis:
        {formatted_data}
    """

    return StreamingResponse(
        stream_claude_client(prompt),
        media_type="text/event-stream"
    )

class CodeRequest(BaseModel):
    plan: str

@app.post("/generate_code")
async def generate_code(req: CodeRequest):
    prompt = f"""
        Generate a code experiment based on the following plan, only generate the code, no other commentary:
        Avoid generating execessive computation and CUDA.
        Please make a simple and TRIVIAL experiment, nothing too complex. Avoid scikit learn and CUDA libraries.
        Format the code using
        ```python
        ```


        This is the experiment plan:
        {req.plan}

        If any plots or images are generated, save them into the image folder such as:
            ```
            IMAGES_FOLDER = "generated_images"
            ...
            plt.savefig(os.path.join(IMAGES_FOLDER, 'graph1.png'))
            ```
    """

    return StreamingResponse(
        stream_claude_client(prompt),
        media_type="text/event-stream"
    )


