from typing import Optional

from api.utils.model_utils import get_large_model, get_llm_client
from api.utils.variable_length_models import (
    get_presentation_markdown_model_with_n_slides,
)
from ppt_config_generator.models import PresentationMarkdownModel


def get_prompt_template(prompt: str, n_slides: int, language: str, content: str):
    return [
        {
            "role": "system",
            "content": """
                Create a presentation based on the provided prompt, number of slides, output language, and additional informational details.
                Format the output in the specified JSON schema with structured markdown content.
    
                # Steps

                1. Identify key points from the provided prompt, including the topic, number of slides, output language, and additional content directions.
                2. Create a concise and descriptive title reflecting the main topic, adhering to the specified language.
                3. Generate a clear title for each slide.
                4. Develop comprehensive content using markdown structure:
                    * Use bullet points (- or *) for lists.
                    * Use **bold** for emphasis, *italic* for secondary emphasis, and `code` for technical terms.
                5. Provide important points from prompt as notes.
                
                # Notes
                - Content must be generated for every slide.
                - Images or Icons information provided in **Input** must be included in the **notes**.
                - Notes should cleary define if it is for specific slide or for the presentation.
                - Slide **body** should not contain slide **title**.
                - Slide **title** should not contain "Slide 1", "Slide 2", etc.
                - Slide **title** should not be in markdown format.
                - There must be exact **Number of Slides** as specified.
                """,
        },
        {
            "role": "user",
            "content": f"""
                **Input:**
                - Prompt: {prompt}
                - Output Language: {language}
                - Number of Slides: {n_slides}
                - Additional Information: {content}
            """,
        },
    ]


async def generate_ppt_content(
    prompt: Optional[str],
    n_slides: int,
    language: Optional[str] = None,
    content: Optional[str] = None,
) -> PresentationMarkdownModel:
    client = get_llm_client()
    model = get_large_model()
    response_model = get_presentation_markdown_model_with_n_slides(n_slides)

    response = await client.beta.chat.completions.parse(
        model=model,
        temperature=0.2,
        messages=get_prompt_template(prompt, n_slides, language, content),
        response_format=response_model,
    )
    return response.choices[0].message.parsed
