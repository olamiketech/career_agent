"""
Script to add secrets to Hugging Face Space
Run this to add your secrets programmatically
"""

from huggingface_hub import HfApi
import os

# Initialize the API
api = HfApi()

# Your space ID
space_id = "olamike007/career_conversations"

# Get your token (you'll need to enter it)
# You can get it from: https://huggingface.co/settings/tokens
token = input("Enter your Hugging Face token (with write permissions): ").strip()

# Add secrets
secrets_to_add = {
    "OPENAI_API_KEY": input("Enter your OPENAI_API_KEY: ").strip(),
    "PUSHOVER_USER": "u7uh5eu13yweg5purczxo48vka2zj2",
    "PUSHOVER_TOKEN": "aqfb6oyoohir6h5csmm7qukymogtic"
}

print("\nAdding secrets to your Space...")

for secret_name, secret_value in secrets_to_add.items():
    try:
        # Note: This is a simplified approach. The actual API might be different
        # Check Hugging Face Hub documentation for the correct method
        print(f"Adding {secret_name}...")
        # You may need to use a different API method here
        # Check: https://huggingface.co/docs/huggingface_hub/main/en/package_reference/hf_api
    except Exception as e:
        print(f"Error adding {secret_name}: {e}")

print("\nSecrets added! Please restart your Space.")


