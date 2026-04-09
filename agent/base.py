import sys
import time
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_groq import ChatGroq
from config.settings import CONFIG
from logger import logger
from exception import CustomException

# Initialize groq LLM 
llm = ChatGroq(model=CONFIG['model']['name'], temperature=CONFIG['model']['temperature'])

def execute_agent(agent_name: str, system_prompt: str, user_content: str, tools: list = None, structured_output=None):
    """Core execution engine for agents, handling tool calling and structured outputs."""
    try:
        logger.info(f"\n----->> Executing {agent_name}...")
        
        delay = CONFIG.get('system_config', {}).get('api_delay', 30)
        
        if structured_output:
            current_llm = llm.with_structured_output(structured_output)
        elif tools:
            current_llm = llm.bind_tools(tools)
        else:
            current_llm = llm

        messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_content)]
        
        logger.info(f"[{agent_name}] Throttling API (Sleeping {delay}s)...")
        time.sleep(delay)
        response = current_llm.invoke(messages)
        
        max_iterations = 3 
        iteration = 0
        
        while tools and hasattr(response, "tool_calls") and response.tool_calls and iteration < max_iterations:
            messages.append(response)
            tool_map = {t.name: t for t in tools}
            
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                logger.info(f"{agent_name} executing tool: '{tool_name}'")
                
                tool_func = tool_map[tool_name]
                tool_result = tool_func.invoke(tool_args)
                
                messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"]))
            
            logger.info(f"[{agent_name}] Tool execution complete. Throttling API (Sleeping {delay}s)...")
            time.sleep(delay)

            response = current_llm.invoke(messages) 
            iteration += 1
            
        if structured_output:
            return response 
        return response.content
        
    except Exception as e:
        raise CustomException(e, sys)