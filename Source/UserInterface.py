from Results import Results
from Input import Input, DegradationMode
from Data import Statistics

import sys, json
from dataclasses import fields


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
        self.__send_message({"results" : self.__convert_results_data_to_dict(results)})
    
    
    # Sends a message through standard output
    @staticmethod
    def __send_message(message):
        sys.stdout.flush()
        sys.stdout.write(json.dumps(message) + "\n")
        sys.stdout.flush()
    
    
    # Converts dictionary, received from the frontend into an input data structure
    @staticmethod
    def __convert_dict_to_input_data(input_data_dict : dict) -> Input:
           
        kwargs = {}
        for f in fields(Input):
            name = f.name

            if name not in input_data_dict:
                continue  # use default

            val = input_data_dict[name]
            
            kwargs[name] = val
            
        degradation_mode_map = {
            "UNIFORM" : DegradationMode.UNIFORM,
            "CONCENTRATED" : DegradationMode.CONCENTRATED
        }
        if "degradation_mode" in input_data_dict:
            mode_name =  input_data_dict["degradation_mode"]
            if mode_name in degradation_mode_map:
                kwargs["degradation_mode"] = degradation_mode_map[mode_name]
        
        return Input(**kwargs)
    
    
    # Converts results data structure into a dictionary for sending
    @staticmethod
    def __convert_results_data_to_dict(results_data : Results) -> dict:
        
        results_dict = dict()
        results_dict["best_strategy"] = str(results_data.best_strategy).replace("AlgorithmNames.", "")
        results_dict["worst_strategy"] = str(results_data.worst_strategy).replace("AlgorithmNames.", "")
        
        statistics_dict = dict()
        
        statistics_dict["sugarity_data_per_algorithm"] = dict()
        for algorithm, value in results_data.statistics.sugarity_data_per_algorithm.items():
            statistics_dict[str(algorithm).replace("AlgorithmNames.", "")] = value
        
        results_dict["statistics"] = statistics_dict
        
        return results_dict