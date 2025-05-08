from main import generate_image
import yaml
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio 

# todo: we need async throttler for rate limiting

class GenerationConfig(BaseModel):
    words: list[str]
    styles: list[str]

    output_dir: str = "collection"
    # api_key = os.getenv("OPENAI_API_KEY")

async def generate_collection(config: GenerationConfig):
    tasks = []
    for word in config.words:
        for style in config.styles:
            output_path = f"{config.output_dir}/{style}/{word}.png"
            if not Path(output_path).exists():
                tasks.append(generate_image(word, output_path, style))
    await asyncio.gather(*tasks)


async def main():
    with open("config.yaml", "r") as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    
    config = GenerationConfig(**config_dict)
    await generate_collection(config)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
