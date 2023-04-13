#OpenAi integration
from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
completion = openai.Completion()

def bigBrain(question, chat_log = None):
    fileLog = open("MainEngine\\Database\\chatLog.txt","r")
    chat_log_template = fileLog.read()

    if chat_log is None:
        chat_log = chat_log_template
    
    prompt = f"{chat_log}You : {question}\nJarvis : "
    response = completion.create(
        model = "text-davinci-002",
        prompt = prompt,
        temperature = 0.5,
        max_tokens = 60,
        top_p = 0.3,
        frequency_penalty = 0.5,
        presence_penalty = 0
    )

    answer = response.choices[0].text.strip()
    chat_log_template_update = f"\nYou : {question} \nFriday : {answer}"
    fileLog = open("MainEngine\\Database\\chatLog.txt","a")
    fileLog.write(str(chat_log_template_update))
    fileLog.close

    return answer

# print(bigBrain("Hello! How are you?"))

def textToImage():
    response = openai.Image.create(
    prompt=input("Enter your imagination here:\n"),
    n=1,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']
    print(image_url)

# textToImage()
#Start this loop to feed data to ai
# while(True):
#     query = input("query: ").lower()
#     bigBrain(query)