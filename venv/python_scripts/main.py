from llama_cpp import Llama
from pprint import pprint
from pydantic import BaseModel, Field
from typing import Literal, List, Dict, NotRequired

#--------------------------------------------------------------------------------------------------------------
class MessageTemplate(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

#--------------------------------------------------------------------------------------------------------------

class Agent:
    def __init__(self):
        self.llm_path = r"path/to/your/llm"
        self.messages = []

    def model_exec(self, question):
        model = Llama(model_path=self.llm_path, chat_format="mistral-instruct", n_gpu_layers=50)
        message = MessageTemplate(role="user", content=question)
        message_dict = message.model_dump()
        output = model.create_chat_completion(model=model, messages=[message_dict])
        return output["choices"][0]["message"]['content']
    

model = Agent()
message = model.model_exec("What is two times four?")
pprint(message)
