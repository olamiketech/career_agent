"""
Railway deployment entry point for Gradio app
This file is used by Railway to start the application
"""
from app import create_ui
import os

if __name__ == "__main__":
    # Create the UI
    demo = create_ui()
    
    # Railway provides PORT as an environment variable
    # Default to 7860 for local development
    port = int(os.getenv("PORT", 7860))
    
    # Launch the app
    # Railway needs 0.0.0.0 to accept external connections
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False  # Don't create public link (Railway provides URL)
    )

