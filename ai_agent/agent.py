from ai_agent.llm import ChatBot
import re

class Agent:
    def __init__(self, api_key,system_prompt="", max_turns=1, known_actions=None):
        self.max_turns = max_turns
        self.bot = ChatBot(api_key,system=system_prompt)
        self.known_actions = known_actions
        self.action_re =  re.compile(r'^Action:\s*(\w+)(?::\s*(.*))?$')
        self.answer_re = re.compile(r'Answer:\s*(.*)', re.MULTILINE)
        
    def run(self, question):
        i = 0
        next_prompt = question
        
        while i < self.max_turns:
            i += 1
            result = self.bot(next_prompt)
            print("Results: ",result)
            answer_match = self.answer_re.search(result) # type: ignore
            actions = [self.action_re.match(a) for a in result.split('\n') if self.action_re.match(a)]
            print(f"Action: {actions} Answer Match: {answer_match}")
            if actions and "Answer" not in result: # type: ignore
                # There is an action to run
                action, action_input = actions[0].groups() # type: ignore
                print(f"Actions: {action} Input {action_input}")
                if action not in self.known_actions: # type: ignore
                    raise Exception("Unknown action: {}: {}".format(action, action_input))
                print(" -- running {} {}".format(action, action_input))
                try:
                    action_input = tuple(action_input.strip().split(","))   
                except Exception as e:
                    print(f"Exception While trasforming the input: {e}")
                    action_input = [action_input]
                observation = self.known_actions[action][0](*action_input) # type: ignore
                print("Observation:", observation)
                next_prompt = "Observation: {}".format(observation)
            else:
                print("In else")
                try:
                    result = answer_match.group(1)
                except:
                    result = "Can you repeat again I was working on some other task. Sorry!"
                return result
            