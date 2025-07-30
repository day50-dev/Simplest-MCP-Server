#!/usr/bin/env python3

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

class LLMToolServer:
    def __init__(self, model_name="Qwen/Qwen3-0.6B"):
        """Initialize the LLM server with tool calling capabilities"""
        print(f"Loading model: {model_name}")
        
        self.device = "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            padding=True,
            torch_dtype=torch.float32,
            device_map="cpu",
            low_cpu_mem_usage=True
        )
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = '<|endoftext|>' #self.tokenizer.eos_token
            
        print("Model loaded successfully!")
    
    def get_system_prompt(self):
        """System prompt that teaches the model about tool calling"""
        return """You are a helpful assistant that can use tools. When you need information that requires a tool call, respond with a JSON object containing:
{
  "tool_call": {
    "name": "tool_name",
    "parameters": {...}
  }
}

Available tools:
- get_favorite_number: Returns the user's favorite number. Takes parameter "user_id" (string).

If the user asks about their favorite number, use the get_favorite_number tool.
"""
    
    def generate(self, prompt, max_length=512, temperature=0.7):
        """Generate text from a prompt"""
        # Create full prompt with system message
        full_prompt = f"System: {self.get_system_prompt()}\n\nUser: {prompt}\n\nAssistant:"
        
        inputs = self.tokenizer.encode(full_prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=len(inputs[0]) + max_length,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.1
            )
        
        response = self.tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True)
        return response.strip()
    
    def parse_tool_call(self, response):
        """Extract tool call from response if present"""
        try:
            # Look for JSON in the response
            json_match = re.search(r'\{.*"tool_call".*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
        except:
            pass
        return None

# Global LLM instance
llm_server = None

@app.route('/generate', methods=['POST'])
def generate():
    """Main generation endpoint"""
    data = request.json
    prompt = data.get('prompt', '')
    max_length = data.get('max_length', 512)
    temperature = data.get('temperature', 0.7)
    
    try:
        response = llm_server.generate(prompt, max_length, temperature)
        
        # Check for tool calls
        tool_call = llm_server.parse_tool_call(response)
        
        result = {
            'response': response,
            'tool_call': tool_call
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

def main():
    global llm_server
    
    print("Initializing LLM server...")
    llm_server = LLMToolServer()
    
    print("Starting server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()
