# 🎙️ Dynamic Podcast Conversation Simulator

An AI-powered tool to generate simulated podcast conversations between custom characters on any topic, inspired by Google's Notebook LM.

## Introduction

The Dynamic Podcast Conversation Simulator is a Streamlit application that allows users to create simulated podcast conversations between multiple characters. Users can define custom characters, assign them distinct personalities, and generate engaging dialogues on any chosen topic. The app leverages OpenAI's language models to produce natural and dynamic conversations and uses Text-to-Speech (TTS) services to convert the dialogue into audio.

## Features

- **Custom Character Creation**: Add and define multiple speakers with unique descriptions and personalities.
- **Dynamic Conversation Generation**: Generate conversations on any topic, guided by detailed prompts and optional context.
- **Podcast Length Control**: Specify the desired duration of the podcast to adjust the length of the conversation.
- **Voice Assignment**: Assign different voices to each character for audio output.
- **Audio Generation**: Convert the generated conversation into an audio file using TTS.
- **Playback and Download**: Play the audio directly in the app and download the final MP3 file.
- **Interactive Interface**: User-friendly interface built with Streamlit for ease of use.

## Inspiration

This project was inspired by Google's Notebook LM, an AI-powered notebook that allows users to interact with their notes and research materials in dynamic ways. Notebook LM introduced innovative features like AI-assisted note-taking, contextual information retrieval, and collaborative research.

Similarly, the Dynamic Podcast Conversation Simulator aims to enhance how users create and interact with content by:

- Allowing personalized content generation based on user-defined inputs.
- Providing an AI-driven platform to simulate natural conversations.
- Offering a way to organize and produce engaging multimedia content.

While Notebook LM focuses on research and note-taking, this project extends the concept to creative content generation, specifically in the context of podcast simulations.

## UI

![PodcasterAI](https://github.com/user-attachments/assets/2737d990-c43b-4722-8d25-e447d117cd85)


## Installation

### Prerequisites

- **Python 3.7 or higher**
- **pip** package manager

### Clone the Repository

```
git clone https://github.com/yourusername/dynamic-podcast-conversation-simulator.git
cd dynamic-podcast-conversation-simulator

```

### Create a Virtual Environment (Optional but Recommended)

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

```

### Install Dependencies

```
pip install -r requirements.txt

```

### Set Up API Keys

The app requires access to the OpenAI API and a Text-to-Speech (TTS) service API.

By default this app utilises the OpenAI API for Speech-to-Text (STT), Chat Completions text response and Text-to-Speech (TTS).

1. **OpenAI API Key**:
    - Sign up at [OpenAI](https://openai.com/) and obtain an API key.
    - Ensure you have access to the necessary models (e.g., GPT-4).
2. **Option: -- Text-to-Speech Service API Key**:
    - Choose a TTS service provider (e.g., Google Cloud TTS, Amazon Polly, Azure TTS).
    - Obtain an API key and set up authentication as per the provider's instructions.

### Configure Environment Variables

Create a `.env` file in the project root directory and add your API keys:

```
OPENAI_API_KEY=your_openai_api_key_here

```

*Note: Ensure that the `.env` file is included in your `.gitignore` to prevent committing sensitive information.*

## Usage

### Run the App

```
streamlit run app.py

```

### App Workflow

1. **Select Characters**:
    - Add speakers by typing names and pressing Enter.
    - You can add as many characters as you like.
2. **Enter Speaker Descriptions**:
    - Provide a description for each character to define their personality and speaking style.
3. **Enter Topic and Context**:
    - Input the main topic for the conversation.
    - Optionally, provide additional context to guide the AI.
4. **Select Podcast Length**:
    - Use the slider to choose the desired length of the podcast in minutes.
5. **Assign Voices**:
    - Select a voice for each character from the available options.
6. **Generate Conversation**:
    - Click the "Click to Generate" button to start the conversation generation process.
    - The app will generate the conversation script and convert it into audio.
7. **Play and Download Audio**:
    - Listen to the generated podcast directly in the app.
    - Download the MP3 file for offline use.


## Acknowledgments

- **Google's Notebook LM**: For inspiring the concept of AI-assisted content creation and interaction.
- **OpenAI**: For providing powerful language models that enable natural language generation.
- **Streamlit**: For offering an easy-to-use framework for building interactive web applications.
- **Pydantic**: For simplifying data validation and management.
- **Pydub**: For audio manipulation capabilities.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
