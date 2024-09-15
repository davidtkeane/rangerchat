#!/usr/bin/env python3
# 

# Import necessary modules
import os
import sys
import subprocess
from setuptools import setup, find_packages

MIN_PYTHON_VERSION = (3, 5)  # Minimum version of Python 3.5+
REQUIRED_PACKAGES = ['openai', 'python-dotenv']  # Add required packages

def check_python_version():
    """Check if Python is installed and meets the minimum version requirement."""
    if sys.version_info < MIN_PYTHON_VERSION:
        print(f"\033[91mError: Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]} or higher is required.\033[0m")
        sys.exit(1)
    else:
        print(f"\033[92mPython {sys.version.split()[0]} is installed and meets the requirement.\033[0m")

def check_pip_installed():
    """Check if pip is installed, otherwise exit."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'])
        print("\033[92mPip is installed.\033[0m")
    except subprocess.CalledProcessError:
        print("\033[91mError: Pip is not installed. Please install pip before running the setup.\033[0m")
        sys.exit(1)

def install_requirements():
    """Install packages from requirements.txt."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("\033[92mAll packages from requirements.txt installed successfully.\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError: Failed to install the required packages. {str(e)}\033[0m")
        sys.exit(1)

def check_installed_packages():
    """Ensure all required packages are installed."""
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
            print(f"\033[92mPackage '{package}' is installed.\033[0m")
        except ImportError:
            print(f"\033[91mPackage '{package}' is not installed. Installing now...\033[0m")
            install_requirements()
# Define functions
def print_help():
    """Print help information and exit."""
    print("\nUsage:")
    print("  python setup.py")
    print("  python setup.py --help")
    print("\nThis script sets up RangerChat, including prompting for the OpenAI API key, setting aliases, and testing the API.")
    print("\nAfter installation, use the 'rgpt' command to interact with the GPT model via the terminal.")
    print("  Example: rgpt 'What is the capital of France?'")
    exit(0)

def banner_start():
    print("\n\033[95mHello There!\033[0m\n")

def banner_end():
    print("\n\033[92mMade by Ranger 💀\033[0m\n")

# Prompt the user for their OpenAI API key
def prompt_api_key():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("")
        print("\033[93mDo you have an OpenAI API key?\033[0m")
        print("")
        has_key = input("Enter 'yes' if you have the key, or 'no' if you don't: ").lower()

        if has_key == 'no':
            print("")
            print("You can find your API key at https://platform.openai.com/account/api-keys")
            open_url = input("Would you like to open this link in your browser? (yes/no): ").lower()
            if open_url == 'yes':
                os.system("open https://platform.openai.com/account/api-keys")
        print("")
        api_key = input("\033[92mPlease enter your OpenAI API key: \033[0m")
    return api_key

# Write the API key to a .env file in ~/rgpt/
def create_env_file(api_key, rgpt_dir):
    import time
    env_path = os.path.join(rgpt_dir, ".env")
    with open(env_path, "w") as f:
        f.write(f"OPENAI_API_KEY={api_key}\n")
    print("")
    print(f"\033[92mAPI key saved in {env_path}\033[0m")
    print("")
    sleep = 5
    print(f"\033[92mConnecting to OpenAI to check API key validity can take {sleep} second(s)...\033[0m")
    print("")
    print(f"\033[93mConnecting, please wait...\033[0m")
    

# Test the API key with a simple OpenAI request
def test_api_key(rgpt_dir):
    import openai
    from dotenv import load_dotenv
    import logging
    

    # Setup logging in ~/rgpt/rgpt_setup.log
    log_file = os.path.join(rgpt_dir, "rgpt_setup.log")
    logging.basicConfig(filename=log_file, level=logging.INFO)

    # Load the .env file
    env_path = os.path.join(rgpt_dir, ".env")
    load_dotenv(env_path)

    openai.api_key = os.getenv('OPENAI_API_KEY')

    if not openai.api_key:
        print("\033[91mAPI key is missing or invalid. Please check the .env file.\033[0m")
        logging.error("API key is missing or invalid.")
        return

    try:
        # Test the API key by sending a request to OpenAI's chat endpoint using gpt-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Explain the programming language Python?"}
            ],
            max_tokens=500
        )
        print("")
        print(f"\033[93mConnection successful!!\033[0m")
        print("")    
        print(f"\033[92mTesting API Response: {response.choices[0].message['content'].strip()}\033[0m")        
        logging.info(f"API key test successful: {response.choices[0].message['content'].strip()}")
        print("")
        print(f"\033[93mAPI key test successful!\033[0m")
        print("")

    except openai.error.AuthenticationError:
        print("")
        print("\033[91mInvalid API key. Please double-check and enter a valid key.\033[0m")
        logging.error("API key authentication failed.")
        new_api_key = prompt_api_key()
        create_env_file(new_api_key, rgpt_dir)
        test_api_key(rgpt_dir)

    except openai.error.APIConnectionError:
        print("\033[91mNetwork error: Failed to connect to OpenAI's API. Please check your internet connection.\033[0m")
        logging.error("Network error: Failed to connect to OpenAI's API.")
    except openai.error.InvalidRequestError as e:
        print(f"\033[91mInvalid request error: {e}\033[0m")
        logging.error(f"Invalid request error: {e}")
    except Exception as e:
        logging.error(f"Error during API test: {e}")
        print(f"\033[91mAn unexpected error occurred during the API test: {e}.\033[0m")

# Main setup routine
if "--help" in sys.argv:
    print_help()

banner_start()
print("")
print("\033[93mSetting up RangerChat...\033[0m")
print("")

# Check Python version and pip installation
check_python_version()
check_pip_installed()

# Create the ~/rgpt/ directory for all files
rgpt_dir = os.path.join(os.path.expanduser("~"), "rgpt")
if not os.path.exists(rgpt_dir):
    os.makedirs(rgpt_dir)

# Check and install required pip packages
check_installed_packages()

api_key = prompt_api_key()
create_env_file(api_key, rgpt_dir)

# Test the API connection
test_api_key(rgpt_dir)

# Set up shell alias
shell_config = input("Lets create the alias. Do you use zsh or bash? (Enter 'zsh' or 'bash'): ").lower()
alias_command = "alias rgpt='python ~/rgpt/rgpt.py'"
home_dir = os.path.expanduser("~")

if shell_config == 'zsh':
    config_path = os.path.join(home_dir, ".zshrc")
else:
    config_path = os.path.join(home_dir, ".bashrc")

with open(config_path, "a") as f:
    f.write(f"\n{alias_command}\n")

print("")
print(f"\033[92mAlias added to {config_path}.\033[0m")
print("")
print(f"\033[92mYou can now use 'rgpt' from the terminal.\033[0m")
print("")
print(f"\033[92mrgpt --help\033[0m for more information.\033[0m")
print("")
print(f"\033[92mTo run 'rgpt How to check my internet connection?'.\033[0m")
print("")

banner_end()

# Call setup() only if valid commands are passed (e.g., install, sdist)
if len(sys.argv) > 1 and sys.argv[1] in ["install", "sdist"]:
    setup(
        name="rgpt",
        version="0.1.0",
        description="A CLI tool to interact with OpenAI's GPT models",
        author="Ranger Smyth",
        author_email="rangersmyth.74@gmail.com",
        packages=find_packages(),
        install_requires=[
            'openai',
            'python-dotenv',
        ],
        entry_points={
            'console_scripts': [
                'rgpt=rgpt:main',  # Assuming your rgpt.py has a main function
            ],
        },
    )