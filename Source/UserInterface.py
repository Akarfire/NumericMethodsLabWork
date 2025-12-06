from Results import Results
from Input import Input

import sys, json


class UserInterface:
    
    def __init__(self, core):
        self.core = core
        
    # Listening to the input from the frontend
    def run_ui(self):
        
        for line in sys.stdin:
            
            # try:
            msg = json.loads(line)
            
            if "input_data" in msg:
                input_data_dict = msg["input_data"]
                print(input_data_dict)
                self.core.call_run(self.__convert_dict_to_input_data(input_data_dict))
            
            else:
                self.__send_message({"Error" : "No input data provided"})
                
            # except Exception as e:
            #     self.__send_message({"Error" : str(e)})
    
    
    # Sends results of the calculations back to the frontend
    def send_results(self, results : Results):
        self.__send_message(self.__convert_results_data_to_dict(results))
    
    
    # Sends a message through standard output
    @staticmethod
    def __send_message(message):
        sys.stdout.write(json.dumps(message) + "\n")
        sys.stdout.flush()
    
    
    # Converts dictionary, received from the frontend into an input data structure
    @staticmethod
    def __convert_dict_to_input_data(input_data_dict : dict) -> Input:
        return Input()
    
    # Converts results data structure into a dictionary for sending
    @staticmethod
    def __convert_results_data_to_dict(results_data : Results) -> dict:
        return dict()