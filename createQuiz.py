import tkinter as tk
from tkinter import messagebox
import styles, copy

class creation:
    def __init__(self, quiz):
        self.quiz = quiz
        self.editing = False
        self.saved = True
        
    def createHolder(self):
        self.holder.destroy()
        self.holder = tk.Frame(self.window, bg=styles.background)
        self.holder.pack()

    def createWindow(self):
        self.window = tk.Tk()
        self.window.title("Create Quiz")
        self.window.geometry("400x300")
        self.window.config(bg=styles.background)

        self.window.bind("<KeyPress>", self.binds)
        self.window.protocol("WM_DELETE_WINDOW", self.onClosing)

        self.holder = tk.Frame(self.window)

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

    def submitQuestion(self, question: str, options: list):
        self.quiz.quiz[question] = options
        self.saved = False
        self.window.title("*Create Quiz")

        self.editQuestionScreen()

    def submit(self, name: str, optionInputs: list, checkBoxes: list, typeOfQuesion: bool, oldName: str = None):
        options = []
        for ix, i in enumerate(optionInputs):
            text = i.get()
            if checkBoxes[ix].get():
                text = '`'+text

            options.append(text)

        name = typeOfQuesion+name.get()

        if oldName != None: del(self.quiz.quiz[oldName])

        self.submitQuestion(name, options)

    def addOption(self, optionInputs: list, optionGrid: tk.Frame, checkBoxes: list, singleChoice: bool):
        optionIndex = len(optionInputs)+1
        input = tk.Entry(optionGrid, width=50, bg=styles.lightGray, fg="white")
        input.insert(0, f"Option {optionIndex}")
        input.grid(row=optionIndex, column=0)

        var = tk.BooleanVar()
        checkBoxes.append(var)
        checkBox = tk.Checkbutton(optionGrid, variable=var, bg=styles.background, fg="white",
                                activebackground=styles.background, activeforeground="white", selectcolor=styles.lightGray)
        
        if singleChoice: checkBox.config(command=lambda: self.clearChecks(optionIndex-1, checkBoxes))

        checkBox.grid(row=optionIndex, column=1)

        optionInputs.append(input)

    def clearChecks(self, index: int, checkBoxes: list):
        for i in checkBoxes:
            i.set(False)

        checkBoxes[index].set(True)

    def deleteQuesion(self, nameOfQuestion: str):
        if messagebox.askyesno("Delete", "Are you sure you want to delete the quesion?"):
            del(self.quiz.quiz[nameOfQuestion])
            self.saved = False
            self.window.title("*Create Quiz")
            self.editQuestionScreen()

    def createChoiceQuestion(self, singleChoice: bool, nameOfQuestion: str=None):
        self.createHolder()

        if singleChoice: text = "Create Single Choice"
        else: text = "Create Multiple Choice"

        title = tk.Label(self.holder, text=text, bg=styles.background, fg="white")
        title.pack()

        if nameOfQuestion != None: text = nameOfQuestion[1::]

        name = tk.Entry(self.holder, width=50, bg=styles.lightGray, fg="white")

        if nameOfQuestion == None: name.insert(0, "Quesion Name")
        else: name.insert(0, text)

        name.pack(pady=10)

        optionInputs = []
        optionGrid = tk.Frame(self.holder, bg=styles.background)
        optionGrid.pack()

        checkBoxes = []

        if singleChoice:
            typeOfQ = 's'
        else: typeOfQ = 'm'

        submitButton = tk.Button(self.holder, text="Submit", command=lambda: self.submit(name, optionInputs, checkBoxes, typeOfQ, nameOfQuestion),
                                bg=styles.darkGray, fg="white", activebackground=styles.lightGray, activeforeground="white", relief=tk.FLAT, bd=0)
        submitButton.pack(pady=10)

        if nameOfQuestion != None:
            for index, value in enumerate(self.quiz.quiz[nameOfQuestion]):
                correct = (value[0] == '`')

                if value[0] == '`': value = value[1::]

                input = tk.Entry(optionGrid, width=50, bg=styles.lightGray, fg="white")
                input.insert(0, value)
                input.grid(row=index, column=0)

                optionInputs.append(input)

                var = tk.BooleanVar(value=correct)
                checkBoxes.append(var)
                checkBox = tk.Checkbutton(optionGrid, variable=var, bg=styles.background, fg="white",
                                        activebackground=styles.background, activeforeground="white", selectcolor=styles.lightGray)
                
                if singleChoice: checkBox.config(command=lambda index=index: self.clearChecks(index, checkBoxes))

                checkBox.grid(row=index, column=1)

        addButton = tk.Button(self.holder, text="Add Option")
        addButton.config(command=lambda: self.addOption(optionInputs, optionGrid, checkBoxes, singleChoice), bg=styles.darkGray, fg="white",
                        activebackground=styles.lightGray, activeforeground="white", relief=tk.FLAT, bd=0)
        addButton.pack()

        deleteButton = tk.Button(self.holder, text="Delete Quesion")
        deleteButton.config(command=lambda: self.deleteQuesion(nameOfQuestion), bg=styles.darkGray, fg="white",
                        activebackground=styles.lightGray, activeforeground="white", relief=tk.FLAT, bd=0)
        deleteButton.pack(pady=10)

    def editQuestionScreen(self):
        self.createHolder()

        title = tk.Label(self.holder, text="Editing questions", bg=styles.background, fg="white", font=("Arial", 18))
        title.pack(pady=10)

        for questionName in self.quiz.quiz.keys():
            text = questionName[1::]
            qName = copy.deepcopy(questionName)

            if questionName[0] == "s": typeOfQ = True
            else: typeOfQ = False

            button = tk.Button(self.holder, text=text, command=lambda qName=qName, typeOfQ=typeOfQ: self.createChoiceQuestion(typeOfQ, qName), bg=styles.darkGray, fg="white",
                                activebackground=styles.lightGray, activeforeground="white", relief=tk.FLAT, bd=0)
            button.pack(pady=1)

        addQ = tk.Button(self.holder, text="Add Quesion", command=lambda: self.askTypeOfQuestion(), bg=styles.darkGray, fg="white",
                                activebackground=styles.lightGray, activeforeground="white", relief=tk.FLAT, bd=0)
        addQ.pack(pady=10)


    def askTypeOfQuestion(self):
        self.createHolder()

        title = tk.Label(self.holder, text="What type of question would you like to create?", bg=styles.background, fg="white")
        title.pack(pady=10)

        singleChoice = tk.Button(self.holder, text="Single Choice", command=lambda: self.createChoiceQuestion(True), bg=styles.darkGray, fg="white",
                                activebackground=styles.lightGray, activeforeground="white", relief=tk.FLAT, bd=0)
        singleChoice.pack(pady=10)

        multipleChoice = tk.Button(self.holder, text="Multiple Choice", command=lambda: self.createChoiceQuestion(False), bg=styles.darkGray, fg="white",
                                activebackground=styles.lightGray, activeforeground="white", relief=tk.FLAT, bd=0)
        multipleChoice.pack(pady=10)

    def binds(self, event: tk.Event):
        if event.keycode == 83:
            if event.state == 12:
                self.quiz.save()
            elif event.state == 13:
                self.quiz.savePath = None
                self.quiz.save()