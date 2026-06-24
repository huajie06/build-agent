import json
from ai.provider import DeepSeekProvider
from tools.fs import write_file, WRITE_FILE_SCHEMA

class AgentRuntime:
    def __init__(self):
        self.provider = DeepSeekProvider()
        
        # Connect the functional maps
        self.tool_registry = {
            "write_file": write_file
        }
        self.tools_schema = [WRITE_FILE_SCHEMA]

    def execute(self, user_prompt: str):
        messages = [
            {"role": "system", "content": "You are a modular learning assistant."},
            {"role": "user", "content": user_prompt}
        ]
        
        while True:
            print("\n🤖 [Core Runtime] Querying LLM...")
            response = self.provider.query(messages, self.tools_schema)
            
            response_message = response.choices[0].message
            messages.append(response_message)
            
            if response_message.content:
                print(f"\n💡 Agent: {response_message.content}")
                
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    
                    print(f"🔧 [Core Runtime] Activating tool: {name}")
                    
                    # Dynamically pick and run tool from registry
                    execute_tool = self.tool_registry[name]
                    tool_output = execute_tool(**args)
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": tool_output
                    })
                continue
            break