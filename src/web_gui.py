# gui_gradio.py
# pip install gradio
# pip install --user gradio // For windows
# main.py
import gradio as gr
from orchestrator import LLMOrchestrator

# Placeholder: Send commands to Isaac Sim
def send_to_isaac(command_dict):
    print(f"[SENDING TO ISAAC SIM] {command_dict}")
    # TODO: Implement communication bridge (ROS, HTTP, gRPC, etc.)
    pass

# Initialize orchestrator
orchestrator = LLMOrchestrator()

def execute_command(user_input, history):
    command_dict = orchestrator.get_robot_command(user_input)
    if command_dict["action"] == "error":
        return "Sorry, I didn't understand that command."
    elif command_dict["action"] == "chat":
        return command_dict["parameters"]["response"]

    params = command_dict["parameters"]
    try:
        # send_to_isaac(command_dict)
        bot_response = f"Success! Executing: {params['direction']} {params['distance']}m at speed {params['speed']}."
    except Exception as e:
        bot_response = f"Error sending command to simulator: {e}"

    return bot_response

def get_camera_stream():
    # Placeholder: replace with Isaac Sim camera stream
    return r"C:\Users\MAK\Videos\Captures\Characters_simulation_IsaacSim_Extension.mp4"

# -------------------------
# EXTRA FEATURES FOR HOSPITAL ROBOT
# -------------------------
# Shared state
task_data = [["Deliver medicine", "102", "High", "Pending"]]

# Shared system log
system_log_text = ""  # optional initial content

# -------------------------
# Functions
# -------------------------
def add_task(task, room, priority):
    global task_data
    if not task and not room:
        return task_data, "⚠️ Please enter both Task and Room number."
    elif not task:
        return task_data, "⚠️ Please enter a Task."
    elif not room:
        return task_data, "⚠️ Please enter a Room number."

    # Add task
    task_data.append([task, room, priority, "Pending"])
    return task_data, f"✅ Task added: {task} → Room {room} (Priority: {priority})"

def update_vitals():
    # Mock vitals
    hr, spo2, temp = 78, 96, 36.8
    return hr, spo2, temp

def emergency_stop():
    send_to_isaac({"action": "emergency_stop"})
    return "🚨 Emergency Stop Activated!"

def return_to_dock():
    send_to_isaac({"action": "return_to_dock"})
    return "🚧 Returning to charging dock!"

# -------------------------
# Build Interface
# -------------------------
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Isaac Sim Hospital Robot Commander")

    with gr.Row():
        # Left column → Chat + Vitals
        with gr.Column(scale=2):
            chat = gr.ChatInterface(fn=execute_command)

            with gr.Accordion("Vitals Dashboard", open=True):
                hr = gr.Slider(minimum=40, maximum=180, value=78, label="❤️ Heart Rate", interactive=False)
                spo2 = gr.Slider(minimum=70, maximum=100, value=96, label="🫁 SpO₂", interactive=False)
                temp = gr.Slider(minimum=30, maximum=42, value=36.8, label="🌡️ Temperature", interactive=False)
                refresh_btn = gr.Button("Refresh Vitals")
                refresh_btn.click(fn=update_vitals, outputs=[hr, spo2, temp])
            
            # Move system log here (under vitals)
            system_log = gr.Textbox(label="System Log", lines=6, interactive=False)

        # Right column → Video + Task Queue + Safety + Log
        with gr.Column(scale=2):
            video = gr.Video(value=get_camera_stream, label="Camera Stream", interactive=False)

            with gr.Accordion("Task Queue", open=False):
                task_box = gr.Dataframe(
                    headers=["Task", "Room", "Priority", "Status"],
                    value=task_data,
                    interactive=False
                )
                with gr.Row():
                    task_input = gr.Textbox(label="Task")
                    room_input = gr.Textbox(label="Room")
                    priority_input = gr.Dropdown(["Low", "Medium", "High"], label="Priority", value="Medium")
                    add_btn = gr.Button("📃 Add Task")

            with gr.Accordion("Safety Controls", open=False):
                e_btn = gr.Button("🚨 Emergency Stop", elem_classes="red-btn")
                d_btn = gr.Button("🚧 Return to Dock")

            # Shared system log
            # system_log = gr.Textbox(label="System Log", lines=6, interactive=False)

            # Connect buttons to system log
            add_btn.click(fn=add_task,
                          inputs=[task_input, room_input, priority_input],
                          outputs=[task_box, system_log])
            e_btn.click(fn=emergency_stop, outputs=system_log)
            d_btn.click(fn=return_to_dock, outputs=system_log)

# Launch app
demo.launch(
    server_name="192.168.0.109",
    allowed_paths=["C:/Users/MAK/Videos/Captures"]
)

# For public URL use share = true to connect on other devices from anywhere but it will expire after 1 week
# demo.launch(
#     server_name="192.168.0.109",
#     allowed_paths=["C:/Users/MAK/Videos/Captures"],
#     share=True
# )