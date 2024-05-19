from tkinter import *
import math
from pygame import mixer
import speech_recognition as sr
from PIL import Image, ImageTk
from abc import ABC, abstractmethod

# Initialize pygame mixer
mixer.init()

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class App(Tk, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.__title = "Smart Calculator"
        self.config(bg='#808080')
        self.geometry('680x486+100+100')

class ButtonFactory(ABC):
    @abstractmethod
    def create_button(self, root, text, command=None):
        pass

class StandardButtonFactory(ButtonFactory):
    def create_button(self, root, text, command=None):
        return Button(root, width=5, height=2, bd=2, relief=SUNKEN, text=text, bg='#808080', fg="white", 
                      font=("arial", 18, "bold"), activebackground="#808080", command=command)

class CalculatorOperations:
    def __init__(self):
        self.__operations = {
            "ADD": lambda a, b: a + b, "ADDITION": lambda a, b: a + b, "SUM": lambda a, b: a + b, "+": lambda a, b: a + b,
            "SUBTRACTION": lambda a, b: a - b, "DIFFERENCE": lambda a, b: a - b, "-": lambda a, b: a - b, "SUBTRACT": lambda a, b: a - b,
            "PRODUCT": lambda a, b: a * b, "MULTIPLICATION": lambda a, b: a * b, "MULTIPLY": lambda a, b: a * b, "TIMES": lambda a, b:a*b,
            "DIVISION": lambda a, b: a / b if b != 0 else 'Error', "DIV": lambda a, b: a / b if b != 0 else 'Error', "DIVIDE": lambda a, b: a / b if b != 0 else 'Error',
            "LCM": lambda a, b: math.lcm(a, b), "HCF": lambda a, b: math.gcd(a, b),
            "MOD": lambda a, b: a % b, "REMAINDER": lambda a, b: a % b, "MODULUS": lambda a, b: a % b
        }

    def perform_operation(self, operation, a, b):
        if operation in self.__operations:
            return self.__operations[operation](a, b)
        else:
            raise ValueError("Operation not supported")
    
    def get_operations(self):
        return self.__operations

operations_instance = CalculatorOperations()

def audio():
    mixer.music.load("music1.wav")
    mixer.music.play()
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio_data = recognizer.listen(source)
            text = recognizer.recognize_google(audio_data)
            print(text)
            mixer.music.load("music2.wav")
            mixer.music.play()
            text_list = text.split(" ")
            operations = operations_instance.get_operations()
            for word in text_list:
                print("Word: ", word)
                if word.upper() in operations:
                    l = [int(num) for num in text_list if num.isdigit()]
                    if len(l) >= 2:
                        result = operations_instance.perform_operation(word.upper(), l[0], l[1])
                        entryField.delete(0, END)
                        entryField.insert(END, result)
        except Exception as e:
            print("Error:", e)

def click(value):
    ex = entryField.get()
    answer = None

    try:
        if value == "C":
            ex = ex[0:len(ex)-1]
            entryField.delete(0, END)
            entryField.insert(0, ex)
            return
        elif value == "CE":
            entryField.delete(0, END)
        elif value == "=":
            answer = eval(ex)
        elif value == "π":
            entryField.insert(END, str(math.pi))
        elif value == "2π":
            entryField.insert(END, str(2 * math.pi))
        elif value == "e":
            entryField.insert(END, str(math.e))
        elif value == "√":
            entryField.insert(END, str(math.sqrt(float(ex))))
        elif value == chr(8731):
            entryField.insert(END, str(float(ex) ** (1/3)))
        elif value == "x\u00B2":
            entryField.insert(END, str(float(ex) ** 2))
        elif value == "x\u00B3":
            entryField.insert(END, str(float(ex) ** 3))
        elif value == "x\u02b8":
            entryField.insert(END, "**")
        elif value == "cosθ":
            entryField.insert(END, str(math.cos(math.radians(float(ex)))))
        elif value == "sinθ":
            entryField.insert(END, str(math.sin(math.radians(float(ex)))))
        elif value == "tanθ":
            entryField.insert(END, str(math.tan(math.radians(float(ex)))))
        elif value == "cosh":
            entryField.insert(END, str(math.cosh(float(ex))))
        elif value == "sinh":
            entryField.insert(END, str(math.sinh(float(ex))))
        elif value == "tanh":
            entryField.insert(END, str(math.tanh(float(ex))))
        elif value == "log₁₀":
            entryField.insert(END, str(math.log10(float(ex))))
        elif value == "ln":
            entryField.insert(END, str(math.log(float(ex))))
        elif value == "deg":
            entryField.insert(END, str(math.degrees(float(ex))))
        elif value == "rad":
            entryField.insert(END, str(math.radians(float(ex))))
        elif value == "x!":
            entryField.insert(END, str(math.factorial(int(ex))))
        else:
            entryField.insert(END, value)
            return

        if answer is not None:
            entryField.delete(0, END)
            entryField.insert(0, answer)
    except Exception as e:
        print("Error:", e)

# Initialize the app
root = App()

# Set up the calculator GUI
logoImage = Image.open("logo.jpeg")
resized_image = logoImage.resize((80, 80), Image.Resampling.LANCZOS)
logoImage = ImageTk.PhotoImage(resized_image)
logoLabel = Label(root, image=logoImage, bd=0, bg="#808080")
logoLabel.grid(row=0, column=0)

micImage = Image.open("logo2.png")
resized_mic_image = micImage.resize((75, 75), Image.Resampling.LANCZOS)
micImageTk = ImageTk.PhotoImage(resized_mic_image)
micButton = Button(root, image=micImageTk, bd=0, bg="#808080", command=audio)
micButton.grid(row=0, column=7)

entryField = Entry(root, font=("arial", 20, "bold"), bg='#808080', fg='white', bd=10, relief=SUNKEN, width=30)
entryField.grid(row=0, column=0, columnspan=8)

# Create buttons using the factory method
factory = StandardButtonFactory()
button_text_list = ["C", "CE", "√", "+", "π", "cosθ", "tanθ", "sinθ",
                    "1", "2", "3", "-", "2π", "cosh", "tanh", "sinh",
                    "4", "5", "6", "*", chr(8731), "x\u02b8", "x\u00B3", "x\u00B2",
                    "7", "8", "9", chr(247), "ln", "deg", "rad", "e",
                    "0", ".", "%", "=", "log₁₀", "(", ")", "x!"]

rowvalue = 1
columnvalue = 0
for i in button_text_list:
    button = factory.create_button(root, i, lambda button=i: click(button))
    button.grid(row=rowvalue, column=columnvalue, pady=1)
    columnvalue += 1
    if columnvalue > 7:
        rowvalue += 1
        columnvalue = 0

# Main loop to run the application
root.mainloop()