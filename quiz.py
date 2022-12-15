from tkinter import filedialog
import json
import createQuiz

class quiz:
    def __init__(self):
        self.savePath = None
        self.fileName = None
        self.loaded = False

        self.createQuiz = createQuiz.creation(self)

        self.quiz = {}

    def load(self, path=None, loaded=True):
        if path == None:
            path = filedialog.askopenfilename()

        try:
            with open(path, 'r') as file:
                self.quiz = json.load(file)
        except Exception as e:
            print(f"FAILED TO LOAD... \n{e}")

        self.loaded = loaded

    def save(self):
        if self.savePath == None:
            self.savePath = filedialog.asksaveasfile().name

        try:
            with open(self.savePath, 'w') as file:
                file.write(json.dumps(self.quiz))
            self.createQuiz.saved = True
            self.createQuiz.window.title("Create Quiz")
            
        except Exception as e:
            print(f"FAILED TO SAVE... \n{e}")