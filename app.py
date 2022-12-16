import tkinter as tk
from tkinter import messagebox
import quiz, time, styles, math

class app:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x400")
        self.root.title("Quiz")
        self.root.config(bg=styles.background)
        self.root.resizable(False, False)
        self.questions = {}

        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)

        self.createMainApp()

        self.quiz = quiz.quiz()

        self.correctAnswers = 0

        if self.checkForSaves(): self.quiz.load()
        else:
            self.running = False
            self.root.destroy()
            self.quiz.createQuiz.createWindow()
            return

        self.questions = self.quiz.quiz
        self.running = True

        self.playQuiz()

    def onClosing(self):
        self.running = False
        self.root.destroy()

    def checkForSaves(self):
        hasQuiz = messagebox.askyesno("Play?", "Do you want to play?")

        if hasQuiz:
            return True
        else:
            return False

    def createMainApp(self):
        self.title = tk.Label(self.root, text="Quiz", font=("Arial", 18, "bold"), bg=styles.background, fg="white")

        self.quizGrid = tk.Frame(self.root, bg=styles.background)

        self.title.pack()
        self.quizGrid.pack()

    def buttonClick(self, multiChoice: bool = False, buttons: list = [], buttonIndex: int = 0, correct: str = "",
                    checkVars: list = [], answerIndexes: list = [], checkBoxes: list = []):

        setCorrect = lambda button: button.config(bg=styles.correct)
        setIncorrect = lambda button: button.config(bg=styles.incorrect)

        if multiChoice:
            for index, checkVar in enumerate(checkVars):
                #Retrieve variable from tk.BooleanVar()
                var = checkVar.get()

                if index in answerIndexes:
                    if var:
                        setCorrect(buttons[index])
                        setCorrect(checkBoxes[index])
                    else:
                        setIncorrect(buttons[index])
                        setIncorrect(checkBoxes[index])
                else:
                    if var: 
                        setIncorrect(buttons[index])
                        setIncorrect(checkBoxes[index])
        else:
            setIncorrect(buttons[buttonIndex])
            for button in buttons:
                if button["text"] == correct: setCorrect(button)
        
        self.root.update()
        time.sleep(3)

        self.answered = True

    def onPress(self, event=None, checkBox=None):
        checkBox.config(bg=styles.lightGray)
    
    def onRelease(self, event=None, checkBox=None):
        checkBox.config(bg=styles.darkGray)

    def playQuiz(self):
        try:
            self.questionLabel = tk.Label(self.quizGrid, text="", font=("Arial", 18), bg=styles.background, fg="white")
            self.questionLabel.grid(row=0, column=0)
        except Exception: return

        buttons = []
        checkBoxes = []
        submitButton = None

        for key, val in self.questions.items():
            
            for button in buttons: button.destroy()
            for checkBox in checkBoxes: checkBox.destroy()

            if submitButton != None: submitButton.destroy()

            buttons = []
            checkBoxes = []

            checkBoxVars = []

            self.answered = False

            typeOfQ = key[0]
            key = key[1::]

            correctStr = ""
            answerIndexes = []

            self.questionLabel.config(text=key)

            questionsGrid = tk.Frame(self.quizGrid, bg=styles.background)
            questionsGrid.grid(row=1, column=0, pady=100)

            for index, answer in enumerate(val):
                if answer[0] == '`':
                    answer = answer[1:]
                    if typeOfQ == 's':
                        correctStr = answer
                    else:
                        answerIndexes.append(index)

                width = round(self.root.winfo_width() / len(val) / 12)

                frame = tk.Frame(questionsGrid, bg=styles.background)

                button = tk.Button(frame, text=answer, font=("Arial", 13, "bold"), bg=styles.darkGray, fg="white", height=5, width=width,
                                wraplength=width*6, bd=0, activebackground=styles.lightGray, activeforeground="white")
                button.pack()

                frame.grid(row=0, column=index, padx=10)

                if typeOfQ == 'm':
                    checkVar = tk.BooleanVar()
                    checkBoxVars.append(checkVar)
                    checkBox = tk.Checkbutton(frame, variable=checkVar, bg=styles.darkGray, state=tk.DISABLED, bd=1)
                    checkBoxes.append(checkBox)
                    checkBox.place(x=0, y=0)

                    button.config(command=lambda checkVar=checkVar: checkVar.set(not checkVar.get()))
                    button.bind("<ButtonPress>", lambda event, checkBox=checkBox: self.onPress(event, checkBox))
                    button.bind("<ButtonRelease>", lambda event, checkBox=checkBox: self.onRelease(event, checkBox))
                else:
                    button.config(command=lambda index=index: self.buttonClick(False, buttons, index, correctStr))

                buttons.append(button)

            if len(checkBoxes) != 0:
                submitButton = tk.Button(questionsGrid, text="Next", font=("Arial", 16), fg="white", activeforeground="white",
                                bg=styles.darkGray, activebackground=styles.lightGray, bd=0)
                submitButton.config(command=lambda: self.buttonClick(True, buttons, checkVars=checkBoxVars, answerIndexes=answerIndexes, checkBoxes=checkBoxes))
                submitButton.grid(row=1, column=round(len(val) / 4)+1, pady=20, sticky=tk.EW)

            while not self.answered and self.running:
                self.root.update()
            if not self.running: self.root.destroy; return


if __name__ == '__main__':
    app()