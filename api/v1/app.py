from fastapi import APIRouter,HTTPException
from ai_agent.agent import Agent
from mcp_server.prompts import agent_prompt
from dotenv import load_dotenv
from mcp_server.constants import examples
from pydantic import BaseModel
import os
from mcp_server.tools import *
tools = APIRouter()

# Loading the api key
load_dotenv()


def create_dynamic_prompt(prompt,actions:dict[str,list],examples)->str:
    try:
        # Merging the action with prompt

        # Question: What is the capital of France?
        # Thought: I should look up France on Wikipedia
        # Action: wikipedia: France
        # PAUSE

        # You will be called again with this:

        # Observation: France is a country. The capital is Paris.

        # You then output:

        # Answer: The capital of France is Paris

        # Example values
        final_example = []
        for example in examples:
                new_example = ""
                question = example[0].get("Question","")
                action = example[0].get("Action","")
                pause = example[0].get("PAUSE","")
                thought = example[0].get("Though","")
                # for key,value in example[0].items():
                new_example = f"Question: {question}\nThough: {thought}\nAction: {action}\n{pause}"
                new_example += "You will be called again with this:"
                item = example[1]
                observation = item["Observation"]
                answer = item["Answer"]
                new_example += f"Observations:{observation}\nYou then output:\nAnswer:{answer}\n"
                new_example +="-"*10
                final_example.append(new_example)
        # Joining all the examples.        
        example_string = "\n".join(final_example)

        known_actions = []
        for key, value in actions.items():
            dynamic_actions = f"{key}:{value[1]}\n"
            known_actions.append(dynamic_actions)
        final_result = "\n".join(known_actions)
        prompt = prompt.format(actions = final_result,examples = example_string)
        return prompt
    except Exception as e:
        print(f"While Creating dynamic prompt {e}")
        return ""
    

# Initialzing the actions.
known_actions  = {
    "fetch_details":[fetch_details,fetch_details.__doc__],
"register_user":[register_user,register_user.__doc__],
"create_appointment": [create_appointment,create_appointment.__doc__],
"update_appointment":[update_appointment,update_appointment.__doc__],
"delete_appointment": [delete_appointment,delete_appointment.__doc__],
"greetings":[greetings,greetings.__doc__]
}

prompt = create_dynamic_prompt(agent_prompt,known_actions,examples)
# print(f"Prompt: {prompt}")
 # Calling the agent.
api_key = os.getenv("GOOGLE_API_KEY")
agent = Agent(api_key,system_prompt=prompt,max_turns=5,known_actions=known_actions)





class Question(BaseModel):
    user_query: str

@tools.post("/qna")
def ask_question(q: Question):
    try:
        print(f"User query: {q.user_query}")
        user_query = q.user_query
       

        # Api key
        response = agent.run(user_query)

        return response
    except Exception as e:
        print(f"While generating the qna {e}")
        raise HTTPException(500,detail="Failed to generate the response.")