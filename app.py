# app.py

import streamlit as st
from streamlit_tags import st_tags
from pydantic import BaseModel, Field, create_model, ValidationError
from typing import Dict, List
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from pydub import AudioSegment
from dotenv import load_dotenv
from openai import OpenAI 

# Load environment variables
load_dotenv(override=True, dotenv_path=".env")

voice_mapping = {


}

default_voice = 'Alloy'  # Replace with a valid default voice if necessary


# Initialize OpenAI API key
openai_api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API key is not set. Please set it in the Streamlit secrets file in .streamlit/secrets.toml.")
    st.stop()


client = OpenAI(api_key=openai_api_key)

# Function to create dynamic Characters model
def create_charactors_model(speakers: Dict[str, str]) -> BaseModel:
    fields = {
        speaker: (str, Field(..., description=desc if desc else f"The character '{speaker}' in the podcast conversation simulation"))
        for speaker, desc in speakers.items()
    }
    return create_model('Charactors', **fields)

# Function to create Conversation model
def create_conversation_model(charactors_model: BaseModel) -> BaseModel:
    class Conversation(BaseModel):
        conversation: List[charactors_model] = Field(
            ..., 
            description="A list of conversation turns with dynamic speakers."
        )
    return Conversation

# Function to generate conversation
def get_conversation(topic, docs, minutes, words, Conversation, model="gpt-4o-mini"):
    # characters_list = ", ".join(characters)
    system_prompt_content = f"""
    You are a script writer. Write a conversation between the following characters. The topic is given by the user.

    Important information:
    
    - Podcast length: Produce a script or dialogue for a podcast of about {minutes} minutes which equates to about {words} total words.
    Note that depending on the number of characters, the total words per character may vary to acheive the desired podcast length.

    - As this is a podcast, the conversation style should be consistent with the following attributes:
        - It should be engaging and informative but also funny and playful, depicting familiarity and friendship with one another as well as love foor throughtful conversation.
        - Each character should have a distinct personality and style of speaking.
        - The characters should refer to other characters by name in conversation.
        - Characters can argure, agree, or disagree with each other. 
        - They should occasionally interrupt each other and finish each other's sentences.
        - Each character should have a unique speaking tone.
        - Characters may use slang and colloquial language.
        - The characters don't have to completely agree with one another and should often have differing opinions on the topic.
        - The conversation should be natural and not forced. This means that each character should only speak for one or two sentences at a time to allow the other character to respond.
    """

    messages = [
        {
            "role": "system",
            "content": system_prompt_content
        },
        {
            "role": "user",
            "content": f"""Please create a podcast script. The topic of the conversation is {topic}.
            {docs}
            """
        }
    ]

    try:
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            response_format=Conversation
        )

        conversation_data = completion.choices[0].message.parsed
        return conversation_data

    except ValidationError as ve:
        st.error(f"Validation Error: {ve}")
        st.stop()
    except Exception as e:
        st.error(f"Error generating conversation: {e}")
        st.stop()


# Function to create audio using TTS
def create_audio(input_text, output_filename, voice):
    try:
        # Replace the following lines with your actual TTS service API calls
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=input_text
        )
        response.stream_to_file(output_filename)
    except Exception as e:
        st.error(f"Error generating audio for voice '{voice}': {e}")
        st.stop()

# Function to combine audio files
def combine_audio(audio_files):
    combined = AudioSegment.empty()
    for file in audio_files:
        try:
            segment = AudioSegment.from_file(file)
            combined += segment
        except Exception as e:
            st.warning(f"Could not process {file}: {e}")
    return combined

def main():
    st.set_page_config(page_title="Dynamic Podcast Conversation Simulator", layout="wide")
    st.title("🎙️ Dynamic Podcast Conversation Simulator")

    # Sidebar for selecting and adding speakers
    st.subheader("1. Select Characters")

    # Initialize session state for speakers_info
    if 'speakers_info' not in st.session_state:
        st.session_state['speakers_info'] = {}
        

    # Input for speaker names using st_tags
    selected_characters = st_tags(
        label='Add Speakers:',
        text='Press enter to add a speaker',
        value=[],  # Default speakers
        suggestions=['Andy', 'Dee', 'Rose', 'Sam'],  # Predefined suggestions (optional)
        maxtags=-1,  # Unlimited tags
        key='tags_input'
    )

    st.markdown("---")

    st.subheader("2. Enter Speaker Descriptions")

    # Loop through each selected speaker to get their description
    for speaker in selected_characters:
        if speaker not in st.session_state['speakers_info']:
            st.session_state['speakers_info'][speaker] = ""
        
        description = st.text_input(
            f"Description for {speaker}:",
            value=st.session_state['speakers_info'][speaker],
            key=f"description_{speaker}"
        )
        st.session_state['speakers_info'][speaker] = description
    
    # Create the dynamic models **after** initializing session state
    speakers_info = st.session_state['speakers_info']
    Charactors = create_charactors_model(speakers_info)
    Conversation = create_conversation_model(Charactors)

    st.markdown("---")

    st.subheader("3. Enter Topic and Context")
    # Input: Conversation Topic
    topic = st.text_input("Enter the conversation topic:", "The benefits of using Agile project managment for your company.", key="topic")
    context = st.text_area("Enter the additional context (Optional):", "")
    docs = f"""The following is some additional context to help inform your response about the topic: 

    {context}""" if context else None
    
    st.markdown("---")

    st.subheader("4. Select Podcast Length")
    minutes = st.slider('Slide me', min_value=2, max_value=10)
    words = minutes * 150
    
    st.markdown("---")
    
        # Assign Voices to Characters
    st.subheader("5. Assign Voices")
    available_voices = ['onyx', 'alloy', 'nova', 'amber', 'echo', 'fable']  # Add more voices as needed
    voice_mapping_user = {}
    for character in selected_characters:
        voice = st.selectbox(f"Select voice for {character}:", available_voices, index=available_voices.index('default_voice') if 'default_voice' in available_voices else 0, key=character)
        voice_mapping_user[character] = voice
    
    st.markdown("---")
    
    # Generate Conversation Button
    st.subheader("6. Generate Conversation")
    if st.button("Click to Generate"):
        if not topic:
            st.error("Please enter a conversation topic.")
            st.stop()

        if not selected_characters:
            st.error("Please select at least one character.")
            st.stop()

        # Generate conversation
        with st.spinner("Generating conversation..."):
            conversation_data = get_conversation(topic, docs, minutes, words, Conversation, model="gpt-4o-mini")

        st.success("Conversation generated successfully!")

        # Display the conversation transcript
        st.subheader("Conversation Transcript")
        for idx, turn in enumerate(conversation_data.conversation, 1):
            st.markdown(f"**Turn {idx}:**")
            for speaker, text in turn.dict().items():
                st.write(f"**{speaker}:** {text}")
            st.markdown("---")

        # Generate and Combine Audio
        with st.spinner("Converting conversation to audio..."):
            audio_files = []
            with TemporaryDirectory() as temp_dir:
                temp_audio_path = Path(temp_dir)
                for idx, turn in enumerate(conversation_data.conversation, 1):
                    for speaker in selected_characters:
                        line_text = turn.dict().get(speaker)
                        if line_text:
                            voice = voice_mapping_user.get(speaker, default_voice)
                            output_filename = temp_audio_path / f"line_{idx}_{speaker}.mp3"
                            create_audio(line_text, output_filename, voice)
                            audio_files.append(output_filename)

                # Combine all audio files
                combined_audio = combine_audio(audio_files)

                # Save the combined audio to a file in the current directory
                output_file = Path("conversation.mp3")
                try:
                    combined_audio.export(output_file, format="mp3")
                except Exception as e:
                    st.error(f"Error exporting combined audio: {e}")
                    st.stop()

        st.success("Audio generated successfully!")

        # Play the audio
        st.subheader("Play Audio")
        try:
            with open(output_file, 'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
        except Exception as e:
            st.error(f"Error playing audio: {e}")

        # Download the audio
        st.subheader("Download Audio")
        try:
            with open(output_file, 'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.download_button(
                    label="Download Conversation Audio",
                    data=audio_bytes,
                    file_name='conversation.mp3',
                    mime='audio/mp3'
                )
        except Exception as e:
            st.error(f"Error preparing download: {e}")

    st.markdown("---")

    st.sidebar.markdown("""
    **Note**:
    - Ensure that your st.secrets or .env file contains the necessary API keys.
    - To add new characters, add their fields to the `Charactors` class in the `app.py` file.
    - The TTS function currently uses OpenAI's hypothetical TTS service. Replace the `create_audio` function with your actual TTS API implementation.
    """)

if __name__ == "__main__":
    main()
