from llama_cpp import Llama
from pprint import pprint
from pydantic import BaseModel, Field
from typing import Literal, List, Dict, NotRequired

from python_scripts.function_calling.llm_function_call import file_finder
from python_scripts.function_calling.llm_function_call import function_finder
from python_scripts.function_calling.llm_function_call import function_information_extraction

#--------------------------------------------------------------------------------------------------------------

class MessageTemplate(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

#--------------------------------------------------------------------------------------------------------------

class Agent:
    def __init__(self):
        self.llm_path = r"venv/model/mistral-7b-instruct-v0.2.Q6_K.gguf"
        self.messages = []

    def model_exec(self, question):
        model = Llama(model_path=self.llm_path, chat_format="mistral-instruct", n_gpu_layers=50)
        message = MessageTemplate(role="user", content=question)
        message_dict = message.model_dump()
        output = model.create_chat_completion(model=model, messages=[message_dict],
                                              functions=function_information_extraction())
        return output["choices"][0]["message"]['content']
    
#--------------------------------------------------------------------------------------------------------------
# Menu

model = Agent()
message = model.model_exec("What is Sandmänchen?")
pprint(message)
