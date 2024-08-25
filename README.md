# Comedy Script Generator

## Overview

The Comedy Script Generator is a desktop application that uses AI to transform your random thoughts into hilarious stand-up comedy routines. With customizable comedy styles and text-to-speech capabilities, this app brings your comedic ideas to life.

## Features

- **AI-Powered Script Generation**: Utilizes OpenAI's GPT-4 to create comedy scripts based on user input.
- **Multiple Comedy Styles**: Choose from observational, sarcastic, absurdist, self-deprecating, or topical humor.
- **Text-to-Speech**: Converts generated scripts into audio using ElevenLabs' advanced voice synthesis.
- **Customizable Voices**: Select from a variety of available voices for your comedy routine.
- **Script Cleaning**: Option to remove stage directions and non-spoken elements for cleaner output.
- **Output Management**: Automatically saves both text scripts and audio files in organized folders.

## Prerequisites

- Python 3.7 or higher
- OpenAI API key
- ElevenLabs API key

## Installation

1. Clone the repository or download the source code. 
2. Git Clone https://github.com/lalomorales22/Jokes-GPT-Elevenlabs.git
3. Navigate to the project directory:
   ```
   cd path/to/Jokes-GPT_Elevenlabs
   ```

4. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

6. Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. In the app interface:
   - Enter your random thoughts in the text area.
   - Select a voice from the dropdown menu.
   - Choose a comedy style.
   - Optionally, check the "Remove action words and details" box for cleaner output.
   - Click "Generate Comedy Script" to create your routine.

3. The app will generate the script, convert it to audio, and save both in a new folder within the `comedy_output` directory.

## Configuration

- User preferences are automatically saved in `comedian_preferences.json`.
- Output files are saved in the `comedy_output` directory, with each generation in its own subfolder.

## Troubleshooting

- If you encounter API errors, ensure your API keys are correctly set in the `.env` file.
- For voice-related issues, check your internet connection and ElevenLabs API status.

## License

[Specify your license here, e.g., MIT License]

## Acknowledgments

- This app uses OpenAI's GPT-4 for text generation.
- Text-to-speech functionality is powered by ElevenLabs.

## Support

For issues, questions, or contributions, please [open an issue](link-to-your-issue-tracker) on the project repository.
