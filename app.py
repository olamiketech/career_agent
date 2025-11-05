from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr

# Load environment variables from .env file if it exists (for local development)
# Don't override existing environment variables (important for Hugging Face Spaces)
load_dotenv(override=False)

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class Me:

    def __init__(self):
        # Check if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found! Please set it as an environment variable or in your .env file.\n"
                "On Hugging Face Spaces, add it as a secret in Settings → Secrets."
            )
        
        self.openai = OpenAI(api_key=api_key)
        self.name = "Michael Salami"
        reader = PdfReader("me/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    

def create_ui():
    """Create an enhanced chat interface with better UI/UX"""
    me = Me()
    
    # Custom theme with modern colors
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    )
    
    # Custom CSS for additional styling
    custom_css = """
    :root {
        color-scheme: light;
    }
    body {
        margin: 0;
        padding: 0;
        background: transparent !important;
    }
    .gradio-container {
        font-family: 'Inter', ui-sans-serif, system-ui, sans-serif;
        width: 100%;
        max-width: 720px;
        margin: 0 auto;
        padding: clamp(0.75rem, 2vw + 0.5rem, 1.5rem) !important;
        box-sizing: border-box;
    }
    .gradio-container .gradio-block {
        width: 100%;
    }
    .header-text,
    .suggestions {
        text-align: center;
    }
    .gradio-chatbot {
        border-radius: 0.75rem !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        min-height: clamp(340px, 55vh, 620px);
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    }
    .gradio-chatbot .message,
    .gradio-chatbot .message.user,
    .gradio-chatbot .message.bot {
        border-radius: 1rem;
        padding: 0.75rem 1rem;
        margin: 0.4rem 0;
        font-size: 0.95rem;
        line-height: 1.55;
        word-break: break-word;
        white-space: pre-wrap;
        max-width: min(100%, 90ch);
        box-shadow: none;
    }
    .gradio-chatbot .message.user {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: #ffffff;
        margin-left: auto;
    }
    .gradio-chatbot .message.bot {
        background: #f1f5f9;
        color: #0f172a;
        margin-right: auto;
    }
    .gradio-chatbot .message-content p {
        margin: 0;
    }
    .gradio-chatbot .message > .avatar {
        display: none;
    }
    .gradio-button {
        border-radius: 0.5rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    .gradio-button.primary {
        background: linear-gradient(90deg, #3b82f6, #2563eb) !important;
        color: white !important;
    }
    .gradio-button.primary:hover {
        background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    .gradio-button.secondary:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    }
    .gradio-textbox textarea {
        border-radius: 0.5rem !important;
        border: 2px solid #cbd5e1 !important;
    }
    .gradio-textbox textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    .message-input textarea {
        min-height: clamp(120px, 22vh, 200px) !important;
        resize: vertical;
    }
    #input-row {
        gap: 0.75rem;
        align-items: flex-start;
        flex-wrap: wrap;
    }
    #input-row .gradio-textbox {
        flex: 1 1 240px;
        min-width: 0;
    }
    #button-column {
        display: flex;
        flex: 0 0 auto;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    #button-column .gradio-button {
        flex: 1 1 120px;
        min-width: 110px;
    }
    .action-button button {
        width: 100%;
        padding: 0.65rem 1rem !important;
        font-size: 0.95rem !important;
    }
    @media (max-width: 768px) {
        .gradio-container {
            padding: clamp(0.75rem, 4vw, 1.25rem) !important;
        }
        .gradio-chatbot {
            min-height: clamp(280px, 60vh, 520px);
        }
    }
    @media (max-width: 640px) {
        #input-row {
            flex-direction: column;
        }
        #button-column {
            width: 100%;
        }
        #button-column .gradio-button {
            width: 100%;
        }
        .message-input textarea {
            min-height: clamp(140px, 28vh, 220px) !important;
        }
        .header-text h1 {
            font-size: 1.5rem;
        }
        .header-text h3 {
            font-size: 1rem;
        }
    }
    """
    
    # Create a header component
    with gr.Blocks(theme=theme, css=custom_css, title=f"{me.name} - AI Assistant") as demo:
        # Header section
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown(
                    f"""
                    ## Chat with {me.name}
                    Ask about work, experience, or ways to collaborate.
                    """,
                    elem_classes=["header-text"]
                )
        
        gr.Markdown("---")
        
        # Chat interface with initial welcome message
        chatbot = gr.Chatbot(
            label="Chat",
            show_copy_button=True,
            avatar_images=(None, "https://i.pravatar.cc/150?img=12"),  # User avatar, bot avatar
            show_label=False,
            type="messages",  # Use new messages format instead of deprecated tuples
            value=[],
            elem_classes=["chatbot-panel"],
        )

        with gr.Row(elem_id="input-row", equal_height=True):
            msg = gr.Textbox(
                label="",
                placeholder="Type a question or say hello to start the conversation.",
                show_label=False,
                scale=9,
                container=False,
                autofocus=True,
                lines=4,
                max_lines=8,
                elem_classes=["message-input"],
            )
            with gr.Column(scale=3, min_width=220, elem_id="button-column"):
                submit_btn = gr.Button(
                    "Send",
                    variant="primary",
                    size="lg",
                    min_width=100,
                    elem_classes=["action-button"],
                )
                clear_btn = gr.Button(
                    "Clear",
                    variant="secondary",
                    size="lg",
                    min_width=100,
                    elem_classes=["action-button"],
                )
        
        # Footer with helpful suggestions
        gr.Markdown(
            """
            **Try asking about:** recent projects · key skills · collaboration ideas · how to connect
            """,
            elem_classes=["suggestions"]
        )
        
        # Event handlers
        def respond(message, chat_history):
            """Handle user message and return response"""
            # Convert from Gradio messages format to API format
            # Skip system/assistant-only messages (welcome messages)
            api_history = []
            for msg in chat_history:
                if msg.get("role") == "user":
                    api_history.append({"role": "user", "content": msg["content"]})
                elif msg.get("role") == "assistant" and api_history:  # Only add if there's a prior user message
                    api_history.append({"role": "assistant", "content": msg["content"]})
            
            # Get bot response
            bot_message = me.chat(message, api_history)
            
            # Append to Gradio messages format
            chat_history.append({"role": "user", "content": message})
            chat_history.append({"role": "assistant", "content": bot_message})
            return "", chat_history
        
        def clear_chat():
            """Clear the chat history and restore welcome message"""
            return [], ""
        
        # Connect events
        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        submit_btn.click(respond, [msg, chatbot], [msg, chatbot])
        clear_btn.click(clear_chat, outputs=[chatbot, msg])
    
    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",  # Allow access from network
        server_port=7860,
        share=False,  # Set to True if you want a public link
        show_error=True,
        favicon_path=None,  # You can add a favicon path here if you have one
    )
    