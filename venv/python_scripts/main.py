from llama_cpp import Llama
from pprint import pprint
from pydantic import BaseModel, Field
from typing import Literal, List, Dict, NotRequired

#--------------------------------------------------------------------------------------------------------------
# Files

from python_scripts.function_calling.llm_function_call import FunctionExtraction

#--------------------------------------------------------------------------------------------------------------
# External Libraries here

from duckduckgo_search import DDGS

#--------------------------------------------------------------------------------------------------------------

class MessageTemplate(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

#--------------------------------------------------------------------------------------------------------------

class Agent:
    def __init__(self, tools=None):
        self.llm_path = r"C:\Users\mpauk\Desktop\python_programming\llm_rag\venv\models\mistral-7b-instruct-v0.2.Q6_K.gguf"
        self.messages = []
        self.tools = tools if tools is not None else ""

    def model_exec(self, question):
        model = Llama(model_path=self.llm_path, chat_format="mistral-instruct", n_gpu_layers=50)

        message = MessageTemplate(role="user", content=question)
        message_dict = message.model_dump()

        external_files = FunctionExtraction.file_finder(self.tools)
        external_functions = FunctionExtraction.function_finder(external_files)
        toolbox = FunctionExtraction.function_information_extraction(external_functions)

        #print("TOOLBOX: ", toolbox)

        output = model.create_chat_completion(model=model, messages=[message_dict], functions=toolbox)
        return output["choices"][0]["message"]['content']
    
#--------------------------------------------------------------------------------------------------------------
# Menu

counter = 0
model = Agent()
while True:
    counter += 1
    print("-------------------------------------------------------------------------")
    print(f"Enter your Question or (q)uit: ")
    user_query = input(f"In[{counter}]: ")
    user_query = user_query.lower()
    if user_query == "q":
        print("Thanks for your Questions!")
        break
    else:
        message = model.model_exec(user_query)
        print(f"Out[{counter}]: {message}")
