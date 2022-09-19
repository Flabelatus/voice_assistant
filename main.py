import random

from neuralintents import GenericAssistant
import pyttsx3 as tts
import speech_recognition as sr
import random

# Initialize the voice setup
recognizer = sr.Recognizer()
speaker = tts.init()
speaker.setProperty('rate', 180)
todo_list = []


def greeting():
    greetings_list = [
        "Hello!",
        "what can I do for you?",
        "Hello there!",
        "Hello my friend!",
    ]

    random_starting_phrase = random.randint(0, len(greetings_list))
    speaker.say(greetings_list[random_starting_phrase])
    speaker.runAndWait()


def good_bye():
    good_bye_list = [
        "See you later!",
        "Good bye!",
        "Adios!",
        "Later!",
        "Exiting now"
    ]

    random_goodbye_phrase = random.randint(0, len(good_bye_list))
    speaker.say(good_bye_list[random_goodbye_phrase])
    speaker.runAndWait()
    exit(1)


def read_todo():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        voice = recognizer.listen(source)
        recognizer.recognize_google(voice)
        speaker.say("Items in your todo list are")
        for todo_item in todo_list:
            speaker.say(todo_item)
        speaker.runAndWait()


def read_time():
    pass


def take_note():
    speaker.say("What do you want me to write to your note?")
    speaker.runAndWait()

    task_done = False

    global recognizer
    while not task_done:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                voice = recognizer.listen(source)
                note = recognizer.recognize_google(voice)
                note = note.lower()
                speaker.say("Please choose a file name!")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                voice = recognizer.listen(source, timeout=10, phrase_time_limit=5)

                filename = recognizer.recognize_google(voice)
                filename = filename.lower()

                with open(f'{filename}.txt', 'w') as my_note:
                    my_note.write(note)
                    task_done = True
                    speaker.say("I successfully created the note {}"
                                .format(filename))
                    speaker.runAndWait()
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("I did not understand you. Please try again!")
            speaker.runAndWait()


def add_todo():
    speaker.say("What do you want to add to your to do list?")
    speaker.runAndWait()
    done = False
    global recognizer
    while not done:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                voice = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                todo = recognizer.recognize_google(voice)
                todo = todo.lower()
                todo_list.append(todo)
                done = True
                speaker.say("I added {} to your to do list".format(todo))
                speaker.runAndWait()

        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say('Can you repeat again please?')
            speaker.runAndWait()


mapping = {'greeting': greeting,
           'good_bye': good_bye,
           'read_time': read_time,
           'take_note': take_note,
           'add_todo': add_todo,
           'read_todo': read_todo
           }

assistant = GenericAssistant('intents.json', intent_methods=mapping)
assistant.train_model()


def main():
    global recognizer
    while True:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                message = recognizer.recognize_google(audio)
                message = message.lower()
            assistant.request(message)
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()


if __name__ == '__main__':
    main()
