# gui_gradio.py
# pip install gradio
# pip install --user gradio // For windows

import gradio as gr

# This function will be called when the user submits a command
def execute_command(user_input, history):
    # history is the chat history, we'll ignore it for now but it's useful for context
    # This is where we will call our main orchestrator function
    # For now, just echo and simulate a response.
    bot_response = f"Received command: '{user_input}'. I will move the robot now."
    return bot_response

# Create a simple chat interface
demo = gr.ChatInterface(
    fn=execute_command,
    title="LLM Robot Commander",
    description="Give a natural language command to the robot in Isaac Sim.",
)

if __name__ == "__main__":
    
    # For local URL - only enables to connect on local device
    # demo.launch()
    
    # After checking the local IP using "ipconfig in windows" in your PC set that IP here
    # It allows to connect other devices to the network as well
    demo.launch(server_name="192.168.1.103")

    # For public URL use share = true to connect on other devices from anywhere but it will expire after 1 week
    # demo.launch(share=True)