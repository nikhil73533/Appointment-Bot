from google import genai
from google.genai.types import GenerateContentConfig
from mcp_server.prompts import user_prompt

class ChatBot:
    """ Class responsable to implement the google gemini SDK.
    """    
    client:genai.Client    
    temprature:float
    output_tokens:int

    def __init__(self,api_key, system="You are an help full assistent",temprature = 0.1,output_tokens = 500):
        self.system = system
        self.client = genai.Client(api_key=api_key)
        self.output_tokens = output_tokens

        self.temprature = temprature
        self.messages = []
        self.past_messages = []
        if self.system:
            self.system  = str({"role": "system", "content": system})
    
    def __call__(self, message):
        
        input = {"role": "user", "content": message}
        if "Observation" in message:
            input = {"role":"assistant","content":message}
        if(len(self.messages)>0):
           print('hurraay.... ',self.messages)
           self.past_messages = [msg["content"] for msg in self.messages if msg["role"] == "user"]
           
        # final_message =  user_prompt.format(past_user_messages = self.past_messages,message = str(input))
        self.messages.append(input)
        result = self.generate_response(str(self.messages))
        self.messages.append({"role": "assistant", "content": result})
        print(f"Message: {self.messages} ")
        return result
        
    def generate_response(self,message):
        try:
            response = self.client.models.generate_content(
            model="gemini-2.0-flash",   
            contents=message,
            config=GenerateContentConfig(
                temperature=self.temprature,
                max_output_tokens=self.output_tokens,
                system_instruction=[
                 self.system
                ])
        )
            return response.text
        except Exception as e:
            print(f"While Generating Response: {e}")
            return None
        

# if __name__=="__main__":
#     api_key = "AIzaSyBTVGlMV4FUZ6joPhjnfG3pA1mdIIUFGYI"
#     agent = ChatBot(api_key)
#     response = agent("Hi")
#     print(response)