# PoladAsadovSmartCalculator
 Smart Calculator written with python has Voice command feature
Intorduction: This application is a voice-activated, smart calculator designed using Python. It integrates multiple libraries to create a rich user interface that supports both click and voice commands to perform mathematical operations. To run the application, ensure Python and libraries such as Tkinter, pygame, PIL, and speech_recognition are installed. Execute the script from your preferred environment

Users can interact with the calculator through a graphical interface or by using voice commands. The application supports basic arithmetic, trigonometric, logarithmic functions, and has sound feedback features.

Singleton Design Patter: The Singleton pattern ensures that only one instance of the App class exists. This avoids duplication and ensures that the application's state is centralized and consistent. class Singleton(type): _instances = {} def call(cls, *args, **kwargs): if cls not in cls._instances: instance = super().call(*args, **kwargs) cls._instances[cls] = instance return cls._instances[cls]

Encapsulation is used to hide the internal state of the application, such as the window title (__title), which is set privately within the class. This protects the application's data integrity and prevents external modifications. class App(Tk, metaclass=Singleton): def init(self): super().init() self.__title = "Smart Calculator"

Inheritance allows StandardButtonFactory to derive from the abstract ButtonFactory class. It inherits the create_button method template and provides its specific implementation, allowing for consistent button creation across the application. class ButtonFactory(ABC): @abstractmethod def create_button(self, root, text, command=None): pass class StandardButtonFactory(ButtonFactory): def create_button(self, root, text, command=None): return Button(root, text=text, ...)

Abstraction is demonstrated by defining an abstract base class (ButtonFactory) that specifies a method (create_button) but leaves the implementation details to its subclasses. This approach abstracts the button creation process, decoupling the button specification from its creation. class ButtonFactory(ABC): @abstractmethod def create_button(self, root, text, command=None): pass Polymorphism is shown here as the create_button method is implemented differently across different factories. This specific implementation allows the application to handle different button types dynamically at runtime. class StandardButtonFactory(ButtonFactory): def create_button(self, root, text, command=None): return Button(root, width=5, height=2, bd=2, ...)

The Factory Method pattern is used to create buttons through a centralized StandardButtonFactory. This method standardizes the creation process and makes the application easier to maintain and modify. factory = StandardButtonFactory() buttons = ["C", "+", "=", ...] for label in buttons: button = factory.create_button(root, label, lambda: click(label)) button.grid(...)

