# pip install --user openai
# pip install --user python-dotenv

import openai
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import numpy as np
# We will set up the Isaac Sim connection later

load_dotenv()

class LLMOrchestrator:
    def __init__(self):
        # self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
            # api_key="<OPENROUTER_API_KEY>",
            )
        self.system_prompt = """
        You are an expert robotics command translator. Convert natural language commands into JSON.
        
        ABSOLUTE RULES (never break these):

        1. If the user says a greeting (examples: "hello", "hi", "hey", "good morning", "good afternoon", "good evening", "how are you", "what's up") or asks a general/non-robotics question, you MUST respond EXACTLY in this format:
        {
            "action": "chat",
            "parameters": {
                "response": "<your natural, friendly response to the user's greeting or question>. How can I help you control the robot today?"
            }
        }

        2. If the user gives a robot movement command, you MUST respond EXACTLY in this format:
        {
            "action": "move",
            "parameters": {
                "direction": "forward", // Allowed: "forward", "backward", "left", "right"
                "distance": 1.0,        // For forward/backward: meters. For left/right: angle in degrees.
                "speed": 0.5            // Range: 0.1 (very slow) to 1.0 (very fast). Default = 0.5 if not specified.
            }
        }

        3. If the command is unclear or cannot be understood, you MUST respond EXACTLY in this format:
        {
            "action": "error",
            "parameters": {
                "reason": "Unable to understand the command."
            }
        }
        """



    
    def get_robot_command(self, user_input):
        try:
            completion = self.client.chat.completions.create(
                
                # Free versions
                model="gpt-3.5-turbo",
                # model="gpt-4o-mini",
                # model="meta-llama/llama-3.1-8b-instruct",
                
                #paid versions
                # model="gpt-4-turbo-preview",
                # model = "openai/gpt-5",

                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ],
                response_format={"type": "json_object"} # This forces the model to respond with JSON
            )
            llm_response = completion.choices[0].message.content
            command_dict = json.loads(llm_response)
            return command_dict
        except Exception as e:
            print(f"Error communicating with LLM: {e}")
            return {"action": "error", "parameters": {}}

# Test the LLM part without Isaac Sim
if __name__ == "__main__":
    orchestrator = LLMOrchestrator()
    test_command = "Move forward half a meter at full speed"
    result = orchestrator.get_robot_command(test_command)
    print("LLM Response:", result)