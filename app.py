import os
import uuid
import json
import re
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from elevenlabs import VoiceSettings, Voice
from elevenlabs.client import ElevenLabs
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Load environment variables
load_dotenv()

# Set up API clients
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY environment variable not set")

openai_client = OpenAI(api_key=OPENAI_API_KEY)
eleven_labs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Ensure output directory exists
OUTPUT_DIR = "comedy_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load or create user preferences
PREFS_FILE = "comedian_preferences.json"
def load_preferences():
    default_prefs = {
        "voice_id": "default",
        "comedy_style": "observational",
        "output_format": "mp3_44100_128",
        "clean_script": True
    }
    if os.path.exists(PREFS_FILE):
        with open(PREFS_FILE, 'r') as f:
            saved_prefs = json.load(f)
        # Update default_prefs with saved preferences, keeping default values for any missing keys
        default_prefs.update(saved_prefs)
    return default_prefs

def save_preferences(prefs):
    with open(PREFS_FILE, 'w') as f:
        json.dump(prefs, f)

user_prefs = load_preferences()

def get_available_voices():
    voices = eleven_labs_client.voices.get_all()
    return {voice.name: voice.voice_id for voice in voices.voices}

AVAILABLE_VOICES = get_available_voices()

def generate_comedy_script(thoughts, style, clean=True):
    comedy_prompts = {
        "observational": "Create a hilarious observational comedy script based on these thoughts. Focus on everyday situations and make them funny.",
        "sarcastic": "Generate a sarcastic and witty comedy script using these thoughts. Don't hold back on the sass!",
        "absurdist": "Craft an absurdist comedy script that takes these thoughts to ridiculous and unexpected places. The weirder, the better!",
        "self-deprecating": "Write a self-deprecating comedy script that pokes fun at the person having these thoughts. Make it relatable and endearing.",
        "topical": "Develop a topical comedy script that relates these thoughts to current events or pop culture. Keep it fresh and relevant!"
    }
    style_prompt = comedy_prompts.get(style, comedy_prompts["observational"])
    
    clean_instruction = "Do not include any stage directions, audience reactions, or non-spoken elements (like 'laughter' or 'pauses'). Write the script as if it's being delivered directly to the audience." if clean else ""
    
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a brilliant comedy writer. {style_prompt} Make it engaging, funny, and suitable for a stand-up routine. {clean_instruction}"},
            {"role": "user", "content": f"Here are my random thoughts:\n\n{thoughts}\n\nTurn this into a hilarious comedy script as requested. Go wild with it!"}
        ]
    )
    return response.choices[0].message.content

def clean_script_content(script):  # Renamed from clean_script to clean_script_content
    # Remove common stage directions and audience reactions
    cleaned = re.sub(r'\([^)]*\)', '', script)
    cleaned = re.sub(r'\[[^]]*\]', '', cleaned)
    cleaned = re.sub(r'(laughter|applause|pause)', '', cleaned, flags=re.IGNORECASE)
    
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned

def create_output_folder(script):
    # Extract the first sentence or up to 50 characters as the folder name
    folder_name = re.sub(r'[^\w\-_\. ]', '_', script[:50].split('.')[0].strip())
    folder_path = os.path.join(OUTPUT_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def save_transcript(text: str, folder_path: str) -> str:
    save_file_path = os.path.join(folder_path, "comedy_script.txt")
    
    with open(save_file_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Transcript saved as: {save_file_path}")
    return save_file_path

def text_to_speech_file(text: str, voice_id: str, output_format: str, folder_path: str) -> str:
    response = eleven_labs_client.text_to_speech.convert(
        voice_id=voice_id,
        optimize_streaming_latency="0",
        output_format=output_format,
        text=text,
        model_id="eleven_turbo_v2",
        voice_settings=VoiceSettings(
            stability=0.3,
            similarity_boost=0.7,
            style=1.0,
            use_speaker_boost=True,
        ),
    )
    
    save_file_path = os.path.join(folder_path, "comedy_audio.mp3")
    
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)
    
    print(f"Comedy audio saved as: {save_file_path}")
    return save_file_path

class ComedyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Comedian's Thought to Script Generator")
        self.geometry("600x500")
        
        # Ensure user_prefs is updated with any new default values
        global user_prefs
        user_prefs = load_preferences()
        
        self.create_widgets()
    
    def create_widgets(self):
        # ... (previous widget creation code remains the same)
        
        # Clean script option
        self.clean_var = tk.BooleanVar(value=user_prefs.get("clean_script", True))
        self.clean_check = ttk.Checkbutton(self, text="Remove action words and details", variable=self.clean_var)
        self.clean_check.pack(pady=5)
        self.thoughts_text = tk.Text(self, height=10)
        self.thoughts_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Voice selection
        self.voice_label = ttk.Label(self, text="Select voice:")
        self.voice_label.pack(pady=5)
        self.voice_var = tk.StringVar(value=user_prefs["voice_id"])
        self.voice_menu = ttk.Combobox(self, textvariable=self.voice_var, values=list(AVAILABLE_VOICES.keys()))
        self.voice_menu.pack(pady=5)
        
        # Comedy style selection
        self.style_label = ttk.Label(self, text="Comedy style:")
        self.style_label.pack(pady=5)
        self.style_var = tk.StringVar(value=user_prefs["comedy_style"])
        self.style_menu = ttk.Combobox(self, textvariable=self.style_var, values=["observational", "sarcastic", "absurdist", "self-deprecating", "topical"])
        self.style_menu.pack(pady=5)
        
        # Clean script option
        self.clean_var = tk.BooleanVar(value=user_prefs.get("clean_script", True))
        self.clean_check = ttk.Checkbutton(self, text="Remove action words and details", variable=self.clean_var)
        self.clean_check.pack(pady=5)
        
        # Generate button
        self.generate_button = ttk.Button(self, text="Generate Comedy Script", command=self.generate_comedy)
        self.generate_button.pack(pady=10)
    
    def generate_comedy(self):
        thoughts = self.thoughts_text.get("1.0", tk.END).strip()
        if not thoughts:
            messagebox.showerror("Error", "Please enter your thoughts. Don't leave us hanging!")
            return
        
        voice_name = self.voice_var.get()
        voice_id = AVAILABLE_VOICES[voice_name]
        comedy_style = self.style_var.get()
        clean_script = self.clean_var.get()
        
        # Update preferences
        user_prefs["voice_id"] = voice_id
        user_prefs["comedy_style"] = comedy_style
        user_prefs["clean_script"] = clean_script
        save_preferences(user_prefs)
        
        # Generate comedy script
        script = generate_comedy_script(thoughts, comedy_style, clean_script)
        
        # Clean script if option is selected
        if clean_script:
            script = clean_script_content(script)  # Updated function name
        
        # Create output folder
        output_folder = create_output_folder(script)
        
        # Save transcript
        transcript_file = save_transcript(script, output_folder)
        
        # Convert to speech
        audio_file = text_to_speech_file(script, voice_id, user_prefs["output_format"], output_folder)
        
        messagebox.showinfo("Success", f"Comedy gold generated!\n\nOutput folder:\n{output_folder}\n\nAudio saved as:\n{audio_file}\n\nTranscript saved as:\n{transcript_file}\n\nHere's a preview of your script:\n\n{script[:200]}...")

if __name__ == "__main__":
    app = ComedyApp()
    app.mainloop()