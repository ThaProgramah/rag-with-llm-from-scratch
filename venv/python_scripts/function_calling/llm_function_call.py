from llama_cpp import Llama
from pprint import pprint, pformat
import json
import ast 
import re
import os
from pydantic import BaseModel, Field
from typing import Literal, List, Dict, NotRequired

#--------------------------------------------------------------------------------------------------------------

# External Libraries here

from duckduckgo_search import DDGS

#--------------------------------------------------------------------------------------------------------------

class FunctionProperty(BaseModel):
    type: str
    description: str

class FunctionParameters(BaseModel):
    type: str = "object"
    properties: Dict[str, FunctionProperty]
    required: List[str]

class FunctionHead(BaseModel):
    name: str
    description: str
    parameters: FunctionParameters

#--------------------------------------------------------------------------------------------------------------

class FunctionExtraction:
    file_list = []
    function_list = []

    @staticmethod
    def file_finder(directory_path):
        '''this function finds external functions in the external_functions folder
        and save the function location in a list and returns the list'''

        function_directory = os.path.join(directory_path)
        file_list = []
        for path, sub_dirs, files in os.walk(function_directory):
            for file in files:
                #print("path: ", path, "sub_dirs: ", sub_dirs, "files: ", files)
                if file.endswith(".py"):
                    file_list.append(f'{path}/{file}')
        
        return file_list
    
    @staticmethod
    def function_finder(file_list):
        '''this function reads the content of a file and returns the file content as string'''

        function_list = []
        for file in file_list:
            with open(file, encoding="utf-8") as f:
                file_content = f.read()
                file_content = file_content + '\n'
                function_list.append(file_content)
        code = ''.join(functions for functions in function_list)
        
        return function_list

    @staticmethod
    def function_information_extraction(function_list):
        '''this functions extracts the function information from the functions list'''

        tool_list = []
        for code in function_list:
            print(code)
            function_properties = {}
            function_parameters = FunctionParameters(properties=function_properties, required=[])
            module = ast.parse(code)

            for node in module.body:
                if isinstance(node, ast.FunctionDef):
                    function_head = FunctionHead(name=node.name, 
                                                description=ast.get_docstring(node), 
                                                parameters=function_parameters)
                    tmp_docstring_list = []
                    tmp_docstring_list.append(ast.get_docstring(node))
                
            for columnwise in tmp_docstring_list:
                tmp_docstring_list = re.split('\n', columnwise)
            
            new_tmp_docstring_list = []
            for tmp_string in tmp_docstring_list:
                docstring_flag = ':'
                if docstring_flag in tmp_string:
                    new_tmp_docstring_list.append(tmp_string)

            for param_name, param_type in zip(new_tmp_docstring_list, module.body[0].args.args):
                param_name, *description = re.split(':', param_name)
                param_description = ''.join(word for word in description)
                function_property = FunctionProperty(type=param_type.annotation.id, 
                                                    description=param_description.strip())
                function_properties[param_name] = function_property.model_dump()
                function_parameters.properties.update(function_properties)
                function_parameters.required.append(param_name)

            function_template = function_head.model_dump_json()
            tool_list.append(function_template)

        return tool_list
