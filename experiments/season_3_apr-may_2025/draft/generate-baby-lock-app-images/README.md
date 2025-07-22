# Alphabet Project Image Generator

A simple Python script that generates images for simple words like "arm" and "house" using OpenAI's DALL-E model.

## Features

- Generates images in multiple artistic styles:
  - Simple, clean drawings with minimal style
  - Doodle style (casual, hand-drawn sketches)
  - Pencil sketch style (detailed with shading and texture)
  - Crayon drawing style (colorful with visible strokes)
- Uses DALL-E 3 for high-quality image generation
- Saves images to a local directory with timestamps
- Simple command-line interface
- Supports batch processing from a file
- Allows customizing the output directory
- Loads API key from environment variables or .env file

## Requirements

- Python 3.6+
- OpenAI API key
- `openai` Python package
- `python-dotenv` package (for loading API key from .env file)

## Installation

1. Clone this repository or download the script
2. Install the required packages:
   ```
   pip install openai python-dotenv
   ```
3. Set your OpenAI API key using one of these methods:

   a. As an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key'
   ```

   On Windows:
   ```
   set OPENAI_API_KEY=your-api-key
   ```

   b. Or create a `.env` file in the same directory as the script with the following content:
   ```
   OPENAI_API_KEY=your-api-key
   ```

## Usage

### Basic Usage

Run the script with one or more words as arguments:

```
python main.py word1 word2 word3
```

Example:
```
python main.py arm house dog cat
```

### Advanced Options

The script supports several command-line options:

- `-f FILE, --file FILE`: Read words from a file (one word per line)
- `-o DIR, --output DIR`: Specify a custom output directory (default: generated_images)

#### Examples:

Process words from a file:
```
python main.py -f words.txt
```

Specify a custom output directory:
```
python main.py -o my_images arm house dog
```

Combine options:
```
python main.py -f words.txt -o alphabet_images
```

The script will:
1. Generate a simple, clean drawing for each word
2. Save the images to the specified output directory (or `generated_images` by default)
3. Print the path to each saved image

## Example Output

```
🖼️ Generating images for: arm, house, dog
✅ Generated image for 'arm' saved to generated_images/arm_1683456789.png
✅ Generated image for 'house' saved to generated_images/house_1683456791.png
✅ Generated image for 'dog' saved to generated_images/dog_1683456793.png
✨ Done!
```

## Notes

- The script uses DALL-E 3, which produces high-quality images but may incur higher API costs
- Each image generation counts toward your OpenAI API usage
- The prompt is designed to create simple, clean drawings with no text or letters
