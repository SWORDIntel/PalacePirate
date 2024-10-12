import os
import sys
import subprocess

# Activate virtual environment if not already active
if not os.getenv('VIRTUAL_ENV'):
    venv_path = os.path.join(os.path.dirname(__file__), 'venv')
    activate_script = os.path.join(venv_path, 'bin', 'activate_this.py')
    if os.path.exists(activate_script):
        with open(activate_script) as f:
            exec(f.read(), {'__file__': activate_script})

# Install required Python packages
subprocess.run([sys.executable, '-m', 'pip', 'install', 'openai'])

import requests
import json
import pickle
from setuptools import setup
import openai

# Reminder to the user
print("You can invoke this script using either 'palacepirate' or 'pprat' commands.")
print("This script is attributed to SWORD Intelligence.")

# Display ASCII sword with the Earth behind it for 8 seconds
import time
print(r"""
       />_________________________________
[########[]_________________________________>
       \>
""")
time.sleep(8)

# Special thanks
print("Special thanks to tgpt, porchpirate, and tg-archive.")

# File to store API keys
SESSION_FILE = "/usr/local/bin/api_keys_session.pkl"

# Function to load API keys from session file
def load_api_keys():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

# Function to save API keys to session file
def save_api_keys(api_keys):
    with open(SESSION_FILE, 'wb') as f:
        pickle.dump(api_keys, f)

# Set or load API keys
def set_or_load_api_keys():
    api_keys = load_api_keys()
    if api_keys:
        print("Stored API keys found.")
        choice = input("Do you want to use existing API keys or set new ones? (use/set/clear): ")
        if choice.lower() == 'use':
            return api_keys
        elif choice.lower() == 'clear':
            api_keys = {}
            save_api_keys(api_keys)
            print("Cleared stored API keys.")
    
    # Set new API keys
    api_keys['dehashed'] = input("Enter Dehashed API key (leave blank to skip): ")
    api_keys['intelx'] = input("Enter intelX API key (leave blank to skip): ")
    api_keys['openai'] = input("Enter OpenAI API key: ")
    save_api_keys(api_keys)
    return api_keys

# Load or set API keys at the start
API_KEYS = set_or_load_api_keys()
API_KEY_DEHASHED = API_KEYS.get('dehashed', '')
API_KEY_INTELX = API_KEYS.get('intelx', '')
API_KEY_OPENAI = API_KEYS.get('openai', '')

# Configure OpenAI API key
openai.api_key = API_KEY_OPENAI

# Install to /usr/local/bin as PalacePirate
def install_as_palacepirate():
    choice = input("Do you want to install this script to /usr/local/bin as PalacePirate? (yes/no): ")
    if choice.lower() == 'yes':
        target_path = '/usr/local/bin/PalacePirate'
        subprocess.run(['sudo', 'cp', os.path.abspath(__file__), target_path])
        subprocess.run(['sudo', 'chmod', '+x', target_path])
        print(f"Installed as PalacePirate at {target_path}")

# Run installation prompt at start
install_as_palacepirate()

# Welcome message and usage instructions
def show_help():
    print("Welcome to the Porch Pirate Interactive CLI!")
    print("Usage: porch_pirate_cli [option]")
    print("\nOptions:")
    print("  -h, --help                Display this help message")
    print("  -s, --simple-search       Perform a simple search")
    print("                            More info: Searches for a term using Porch Pirate to find relevant public entities.")
    print("  -w, --get-workspace       Get information on a specific workspace")
    print("                            More info: Retrieves detailed information about a specific workspace using its ID.")
    print("  -d, --dump-workspace      Dump workspace information")
    print("                            More info: Dumps all available data about a workspace for deeper analysis.")
    print("  -g, --get-globals         Extract workspace globals")
    print("                            More info: Extracts global variables from a specified workspace based on the search term.")
    print("  -u, --extract-urls        Extract URLs from workspace")
    print("                            More info: Extracts all URLs from the collections within a workspace.")
    print("  -c, --show-collections    Show collections in workspace")
    print("                            More info: Displays all collections that are part of the specified workspace.")
    print("  -r, --show-requests       Show workspace requests")
    print("                            More info: Lists all requests associated with a particular workspace.")
    if API_KEY_DEHASHED:
        print("  --dehashed-search         Search using Dehashed API")
        print("                            More info: Uses Dehashed API to search for data breaches or compromised information.")
    if API_KEY_INTELX:
        print("  --intelx-search           Search using intelX API")
        print("                            More info: Uses intelX API for comprehensive intelligence search on the given term.")
    print("  --openai-chat             Interact with OpenAI's GPT model")
    print("                            More info: Use OpenAI's GPT model to generate responses for specific prompts.")
    print("                            Models available: 'gpt-3.5-turbo', 'gpt-4', 'davinci' (choose one)")
    print("  --openai-complete         Generate text completion using OpenAI API")
    print("                            More info: Generate a completion for a given prompt using OpenAI's language model.")
    print("                            Models available: 'gpt-3.5-turbo', 'gpt-4', 'davinci' (choose one)")
    print("  --openai-extrapolate      Extrapolate data using OpenAI API")
    print("                            More info: Use OpenAI's GPT model to analyze and extrapolate data from previous function results.")
    print("                            Models available: 'gpt-3.5-turbo', 'gpt-4', 'davinci' (choose one)")
    print("  --explain-functions       Explain the available functions and their integration")
    print("                            More info: Provides an explanation of each function and how they can integrate with each other.")
    print("  -f, --output-format       Output results into various file formats (json, csv, txt, maltego)")
    print("                            More info: Saves search results to the specified file format for further use.")
    print("  --create-shortcut         Create a shortcut for this script in the taskbar")
    print("                            More info: Adds a shortcut to the taskbar for easy access to Porch Pirate CLI.")
    print("  --tg-archive              Archive Telegram chats using tg-archive")
    print("                            More info: Archives Telegram chats using tg-archive based on the provided configuration.")

# Porch Pirate Client Functions
def simple_search(term):
    print(f"Performing simple search for: {term}...")
    subprocess.run(["/usr/local/bin/porch-pirate", "-s", term])


def get_workspace(workspace_id):
    print(f"Getting workspace information for: {workspace_id}...")
    subprocess.run(["/usr/local/bin/python3", "/usr/local/bin/get_workspace.py", workspace_id])


def dump_workspace(workspace_id):
    print(f"Dumping workspace information for: {workspace_id}...")
    subprocess.run(["/usr/local/bin/porch-pirate", "-w", workspace_id, "--dump"])


def get_globals(term):
    print(f"Extracting globals for: {term}...")
    subprocess.run(["/usr/local/bin/porch-pirate", "-s", term, "--globals"])


def extract_urls(workspace_id):
    print(f"Extracting URLs from workspace: {workspace_id}...")
    subprocess.run(["/usr/local/bin/porch-pirate", "-w", workspace_id, "--urls"])


def show_collections(workspace_id):
    print(f"Showing collections in workspace: {workspace_id}...")
    subprocess.run(["/usr/local/bin/python3", "/usr/local/bin/get_collections.py", workspace_id])


def show_requests(workspace_id):
    print(f"Showing requests in workspace: {workspace_id}...")
    subprocess.run(["/usr/local/bin/python3", "/usr/local/bin/get_request.py", workspace_id])

# Dehashed and intelX API Functions
if API_KEY_DEHASHED:
    def dehashed_search(term):
        print(f"Performing Dehashed search for: {term}...")
        response = requests.get(f"https://api.dehashed.com/search?query={term}", auth=(API_KEY_DEHASHED, ""))
        print(response.text)

if API_KEY_INTELX:
    def intelx_search(term):
        print(f"Performing intelX search for: {term}...")
        headers = {"x-key": API_KEY_INTELX}
        response = requests.get(f"https://2.intelx.io/intelligent/search?term={term}", headers=headers)
        print(response.text)

# OpenAI API Functions
def openai_chat(prompt):
    model = input("Choose model ('gpt-3.5-turbo', 'gpt-4', 'davinci'): ")
    print(f"Interacting with OpenAI's {model} model for prompt: {prompt}...")
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    print(response.choices[0].message['content'])


def openai_complete(prompt):
    model = input("Choose model ('gpt-3.5-turbo', 'gpt-4', 'davinci'): ")
    print(f"Generating text completion for prompt: {prompt} using {model} model...")
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=150
    )
    print(response.choices[0].text.strip())


def openai_extrapolate(data):
    model = input("Choose model ('gpt-3.5-turbo', 'gpt-4', 'davinci'): ")
    print(f"Using OpenAI's {model} model to extrapolate data: {data}...")
    response = openai.Completion.create(
        engine=model,
        prompt=f"Analyze and extrapolate the following: {data}",
        max_tokens=150
    )
    print(response.choices[0].text.strip())
