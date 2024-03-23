import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import winsound
import webbrowser
import pyjokes

def listen_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source) 
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None

def respond(response_text):
    print(response_text)
    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")
    sound = AudioSegment.from_mp3("response.mp3")
    sound.export("response.wav", format="wav")
    winsound.PlaySound("response.wav", winsound.SND_FILENAME)

tasks = []
listeningToTask = False

def main():
    global tasks
    global listeningToTask
    
    while True:
        command = listen_command()

        triggerName = "max"

        
        if command and triggerName in command:
            if listeningToTask:
                tasks.append(command)
                listeningToTask = False
                respond("Adding " + command + " to your task list. You have " + str(len(tasks)) + " in your list now.")
            elif "add a task" in command:
                listeningToTask = True
                respond("Sure, what is the task?")
            elif "list tasks" in command:
                if tasks:
                    respond("Sure. Your tasks are:")
                    for task in tasks:
                        respond(task)    
                else:
                    respond("Your task list is empty")
            elif "open web" in command:
                respond("Opening Chrome.")
                webbrowser.open("http://www.google.com")
            elif "drop a joke" in command:
                joke = pyjokes.get_joke()
                respond(joke)
            elif "quit" in command:
                respond("Goodbye!")
                break
            else:
                respond("Sorry, I could not handle that command.")

if __name__ == "__main__":
    main()
