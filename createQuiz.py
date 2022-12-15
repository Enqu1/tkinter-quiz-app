import tkinter as tk
from tkinter import messagebox
import styles, copy

class creation:
    def __init__(self, quiz):
        self.quiz = quiz
        self.editing = False
        self.saved = True

    def createWindow(self):
        self.window = tk.Tk()
        self.window.title("Create Quiz")
        self.window.geometry("400x300")

        self.window.bind("<KeyPress>", self.binds)
        self.window.protocol("WM_DELETE_WINDOW", self.onClosing)

        if messagebox.askyesno(title="Load", message="Do you want to edit a quiz?"):
            self.editing = True
            self.quiz.load(loaded=False)
            self.editQuestionScreen()
        else:
            self.askTypeOfQuestion(tk.Frame(self.window))

        self.window.mainloop()

    def onClosing(self):
        if not self.saved:
            if messagebox.askyesno(title="Save", message="Quiz not saved. Would you like to save it?"):
                self.quiz.save()
        
        if messagebox.askyesno(title="Quit", message="Are you sure you would like to quit?"):
            self.window.destroy()

    def submitQuestion(self, question: str, options: list, holder: tk.Frame):
        self.quiz.quiz[question] = options
        self.saved = False
        self.window.title("*Create Quiz")

        holder.destroy()

        self.editQuestionScreen()

    def submit(self, name: str, optionInputs: list, checkBoxes: list, holder: tk.Frame, typeOfQuesion: bool, oldName: str = None):
        options = []
        for ix, i in enumerate(optionInputs):
            text = i.get()
            if checkBoxes[ix].get():
                text = '`'+text

            options.append(text)

        name = typeOfQuesion+name.get()

        if oldName != None: del(self.quiz.quiz[oldName])

        self.submitQuestion(name, options, holder)

    def addOption(self, optionInputs: list, optionGrid: tk.Frame, checkBoxes: list, singleChoice: bool):
        optionIndex = len(optionInputs)+1
        input = tk.Entry(optionGrid, width=50)
        input.insert(0, f"Option {optionIndex}")
        input.grid(row=optionIndex, column=0)

        var = tk.BooleanVar()
        checkBoxes.append(var)
        checkBox = tk.Checkbutton(optionGrid, variable=var)
        
        if singleChoice: checkBox.config(command=lambda: self.clearChecks(optionIndex, checkBoxes))

        checkBox.grid(row=optionIndex, column=1)

        optionInputs.append(input)

    def clearChecks(self, index: int, checkBoxes: list):
        for i in checkBoxes:
            i.set(False)

        checkBoxes[index].set(True)

    def createChoiceQuestion(self, holder: tk.Frame, singleChoice: bool, nameOfQuestion: str=None):
        holder.destroy()

        holder = tk.Frame(self.window)

        if singleChoice: text = "Create Single Choice"
        else: text = "Create Multiple Choice"

        title = tk.Label(holder, text=text)
        title.pack()

        if nameOfQuestion != None: text = nameOfQuestion[1::]

        name = tk.Entry(holder, width=50)

        if nameOfQuestion == None: name.insert(0, "Quesion Name")
        else: name.insert(0, text)

        name.pack(pady=10)

        optionInputs = []
        optionGrid = tk.Frame(holder)
        optionGrid.pack()

        checkBoxes = []
        submitButton = tk.Button(holder)

        if nameOfQuestion != None:
            for index, value in enumerate(self.quiz.quiz[nameOfQuestion]):
                correct = (value[0] == '`')

                if value[0] == '`': value = value[1::]

                input = tk.Entry(optionGrid, width=50)
                input.insert(0, value)
                input.grid(row=index, column=0)

                optionInputs.append(input)

                var = tk.BooleanVar(value=correct)
                checkBoxes.append(var)
                checkBox = tk.Checkbutton(optionGrid, variable=var)
                
                if singleChoice: checkBox.config(command=lambda index=index: self.clearChecks(index, checkBoxes))

                checkBox.grid(row=index, column=1)

            if singleChoice:
                typeOfQ = 's'
            else: typeOfQ = 'm'
            submitButton = tk.Button(holder, text="Submit", command=lambda: self.submit(name, optionInputs, checkBoxes, holder, typeOfQ, nameOfQuestion))
            submitButton.pack(pady=10)

        addButton = tk.Button(holder, text="Add Option")
        addButton.config(command=lambda: self.addOption(optionInputs, optionGrid, checkBoxes, singleChoice))
        addButton.pack()

        holder.pack()

    def editQuestionScreen(self):
        holder = tk.Frame(self.window)

        title = tk.Label(holder, text="Editing question")
        title.pack()

        for questionName in self.quiz.quiz.keys():
            text = questionName[1::]
            qName = copy.deepcopy(questionName)

            if questionName[0] == "s": typeOfQ = True
            else: typeOfQ = False

            button = tk.Button(holder, text=text, command=lambda qName=qName, typeOfQ=typeOfQ: self.createChoiceQuestion(holder, typeOfQ, qName))
            button.pack()

        addQ = tk.Button(holder, text="Add Quesion", command=lambda: self.askTypeOfQuestion(holder))
        addQ.pack(pady=10)

        holder.pack()


    def askTypeOfQuestion(self, holder: tk.Frame):
        holder.destroy()
        holder = tk.Frame(self.window)

        title = tk.Label(holder, text="What type of question would you like to create?")
        title.pack(pady=10)

        singleChoice = tk.Button(holder, text="Single Choice", command=lambda: self.createChoiceQuestion(holder, True))
        singleChoice.pack(pady=10)
        multipleChoice = tk.Button(holder, text="Multiple Choice", command=lambda: self.createChoiceQuestion(holder, False))
        multipleChoice.pack(pady=10)

        holder.pack()

    def binds(self, event: tk.Event):
        if event.state == 12 and event.keycode == 83:
            self.quiz.save()