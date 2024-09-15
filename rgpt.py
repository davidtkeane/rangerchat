#!/usr/bin/env python3

# Created by Ranger (rgpt)
# RangerChat-ChatGPT script for Linux and MacOS

# Version 1: Created 15-09-2024.

# Usage: 
# python rgpt.py "query" : Replace "query" with your question or prompt. 
# Example 1: python rgpt.py What is the capital of France
# Example 2: rgpt What is the capital of Ireland

# Modules to import
import openai
import os
import sys
import logging
from dotenv import load_dotenv
from datetime import datetime

# Set up directory and log file
rgpt_dir = os.path.join(os.path.expanduser("~"), "rangerchat")
log_file = os.path.join(rgpt_dir, "rgpt.log")
history_file = os.path.join(rgpt_dir, "rgpt.txt")

# Ensure the ~/rgpt/ directory exists
if not os.path.exists(rgpt_dir):
    os.makedirs(rgpt_dir)

# Set up logging
logging.basicConfig(filename=log_file, level=logging.INFO)

# Default model and temperature settings
current_model = "gpt-4"
current_temperature = 0.8

def save_conversation(prompt, response_content):
    """Save the conversation (prompt and response) to a text file with timestamps."""
    with open(history_file, "a") as file:
        start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Log start of conversation
        file.write("=== ChatGPT-4 started at {} ===\n".format(start_time))

        # Log user input
        file.write("[{}] User 💀 : {}\n".format(start_time, prompt))

        # Log model response
        end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        file.write("[{}] RangerChat 🤖 : {}\n".format(end_time, response_content))

        # Log end of conversation
        file.write("=== ChatGPT-4 ended at {} ===".format(end_time) + "\n\n")

def chat_gpt4(prompt):
    """Function to interact with OpenAI's GPT-4 model."""
    try:
        # Load environment variables from ~/rgpt/.env
        env_path = os.path.join(rgpt_dir, ".env")
        load_dotenv(env_path)

        openai.api_key = os.getenv('OPENAI_API_KEY')

        # Check if the API key is present
        if openai.api_key is None:
            print("\033[91mAPI key not found. Please make sure it's set in the .env file.\033[0m")
            return

        print("\n\033[93mPlease wait for your answer 💀\033[0m\n")
        
        # Call the OpenAI API (ChatCompletion) for GPT-4 or GPT-3.5-turbo
        response = openai.ChatCompletion.create(
            model=current_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=current_temperature,
            max_tokens=100
        )

        # Get the response content
        response_content = response['choices'][0]['message']['content'].strip()
        logging.info(f"Model: {current_model}, Temperature: {current_temperature}, Prompt: {prompt}, Response: {response_content}")
        print(response_content)

        # Save the conversation to rgpt.txt with timestamps
        save_conversation(prompt, response_content)

    except openai.error.AuthenticationError:
        print("\033[91mInvalid API key. Please check your key.\033[0m")
        logging.error("Authentication error: Invalid API key.")
    except Exception as e:
        logging.error(f"Error during API call: {e}")
        print("\033[91mAn error occurred while processing your request.\033[0m")

def display_options():
    """Display the interactive options menu."""
    global current_model, current_temperature

    while True:
        print("\n\033[96mOptions:\033[0m")
        print("")
        print("1. Enter a prompt or ask a question")
        print(f"2. Change model (current: {current_model})")
        print(f"3. Change temperature (current: {current_temperature})")
        print("4. Help")
        print("")
        print("\033[96m5. Exit\033[0m")
        print("")

        option = input("\033[94mChoose an option: \033[0m").strip()

        if option == "1":
            query = input("Enter your prompt: ")
            chat_gpt4(query)
            # After the query is handled, display the options again
        elif option == "2":
            current_model = input("Enter new model name (e.g., gpt-4, gpt-4o): ").strip()
            print(f"Model changed to: {current_model}")
            # After changing the model, display the options again
        elif option == "3":
            try:
                current_temperature = float(input("Enter new temperature (0.0 to 1.0): "))
                if 0.0 <= current_temperature <= 1.0:
                    print(f"Temperature changed to: {current_temperature}")
                else:
                    print("Temperature must be between 0.0 and 1.0.")
            except ValueError:
                print("Invalid input. Please enter a number between 0.0 and 1.0.")
            # After changing the temperature, display the options again
        elif option == "4":
            print_help()
            # After displaying the help, show the options again
        elif option == "5":
            print("\033[93mThank you for using RangerChat 💀\033[0m")
            break
        else:
            print("Invalid option. Please try again.")

        # Display the options again after every action

def print_help():
    """Print help information."""
    print("\n\033[96mRangerChat Help Page:\033[0m")
    print("")
    print("1. You can interact with the model by entering a prompt.")
    print("2. You can change the model by choosing option 2.")
    print("3. Temperature (0.0 is more deterministic, 1.0 is more creative).")
    print("4. Check logs in '~/rangerchat/rgpt.log'.")
    print("5. Conversation history is saved in '~/rangerchat/rgpt.txt'.")
    print("\n\033[94m6. For help, run: rgpt --help 💀\033[0m\n")

def main():
    """Main function to handle command-line arguments and options."""
    # Print welcome message
    print("\n\033[93mWelcome to RangerChat 💀\033[0m\n")

    if "--help" in sys.argv:
        print_help()
        sys.exit(0)

    if "--options" in sys.argv:
        display_options()
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Usage: rgpt <query> or rgpt --options")
        sys.exit(1)

    query = ' '.join(sys.argv[1:])
    chat_gpt4(query)

    # Check if the user wants to ask another question
    while True:
        print("")
        another_question = input("\033[93mDo you want to ask another question? (yes/no): \033[0m")
        if another_question.lower() in ["yes", "y"]:
            query = input("Enter your question: ")
            chat_gpt4(query)
        elif another_question.lower() in ["no", "n"]:
            print("")
            print("\033[93mThank you for using RangerChat 💀\033[0m")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()
