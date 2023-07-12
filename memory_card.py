from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QHBoxLayout, QVBoxLayout, 
        QGroupBox, QButtonGroup, QRadioButton,  
        QPushButton, QLabel)
from random import *


class Question():
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        # all the lines must be given when creating the object, and will be recorded as properties
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3


questions_list = [] 
questions_list.append(Question('The state language of Brazil', 'Portuguese', 'English', 'Spanish', 'Brazilian'))
questions_list.append(Question('Which color does not appear on the American flag?', 'Green', 'Red', 'White', 'Blue'))
questions_list.append(Question('A traditional residence of the Yakut people', 'Urasa', 'Yurt', 'Igloo', 'Hut'))

app = QApplication([])
btn_OK = QPushButton('Answer') # answer button
lb_Question = QLabel('The most difficult question in the world!') # question text


RadioGroupBox = QGroupBox("Answer options") # on-screen group for radio buttons with answers


rbtn_1 = QRadioButton('Option 1')
rbtn_2 = QRadioButton('Option 2')
rbtn_3 = QRadioButton('Option 3')
rbtn_4 = QRadioButton('Option 4')


RadioGroup = QButtonGroup() # this groups the radio buttons so we can control their behavior
RadioGroup.addButton(rbtn_1)
RadioGroup.addButton(rbtn_2)
RadioGroup.addButton(rbtn_3)
RadioGroup.addButton(rbtn_4)
layout_ans1 = QHBoxLayout()
layout_ans2 = QVBoxLayout() # the vertical ones will be inside the horizontal one
layout_ans3 = QVBoxLayout()
layout_ans2.addWidget(rbtn_1) # two answers in the first column
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3) # two answers in the second column
layout_ans3.addWidget(rbtn_4)

layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3) # put the columns in the same line


RadioGroupBox.setLayout(layout_ans1) # a “panel” with the answer options is ready


AnsGroupBox = QGroupBox("Test result")
lb_Result = QLabel('Are you correct or not?') # “correct” or “incorrect” will be written here
lb_Correct = QLabel('The answer will be here!') # the correct answer text will be written here
layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result, alignment=(Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(lb_Correct, alignment=Qt.AlignHCenter, stretch=2)
AnsGroupBox.setLayout(layout_res)


layout_line1 = QHBoxLayout() # question
layout_line2 = QHBoxLayout() # answer options or test result
layout_line3 = QHBoxLayout() # "Answer" button


layout_line1.addWidget(lb_Question, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
layout_line2.addWidget(RadioGroupBox)
layout_line2.addWidget(AnsGroupBox)
AnsGroupBox.hide() # hide the answer panel because the question panel should be visible first


layout_line3.addStretch(1)
layout_line3.addWidget(btn_OK, stretch=2) # the button must be large
layout_line3.addStretch(1)

layout_card = QVBoxLayout()
layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)
layout_card.setSpacing(5) # spaces between the contents


def show_result():
    ''' Show the answer panel. '''
    RadioGroupBox.hide()
    AnsGroupBox.show()
    btn_OK.setText('Next question')


def show_question():
    ''' Show the question panel. '''
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn_OK.setText('Answer')
    # clear selected radio button
    RadioGroup.setExclusive(False) # remove the limits so we can reset the radio buttons
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    RadioGroup.setExclusive(True)

answers = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]
def ask(q: Question):
    ''' This function writes the value of the question and answers in the corresponding widgets. The answer options are distributed randomly. '''
    shuffle(answers) # shuffle the list of buttons; now a random button is first in the list
    answers[0].setText(q.right_answer) # fill the first element of the list with the correct answer and the other elements with incorrect answers
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    lb_Question.setText(q.question) # question
    lb_Correct.setText(q.right_answer) # answer
    show_question() # show the question panel

def show_correct(res):
    lb_Result.setText(res)
    show_result()


def check_answer():
    if answers[0].isChecked():
        show_correct('Correct!')
        window.score +=1
        print("Scatistics\n-Total questions:", window.total, '\n-Right answers:', window.score)
        print('Rating:', (window.score / window.total * 100), '%')
    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            show_correct('Incorrect!')
            print('Rating:', (window.score / window.total * 100), '%')
        


def next_question():
    window.total += 1
    print("Scatistics\n-Total questions:", window.total, '\n-Right answers:', window.score)
    cur_question = randint(0, len(questions_list) - 1)
    q = questions_list[cur_question] # take a question
    ask(q) # ask it


def click_OK():
    ''' This determines whether to show another question or check the answer to this question. '''
    if btn_OK.text() == 'Answer':
        check_answer() # check the answer
    else:
        next_question() # next question


# Make the current question from the list a property of the “window” object. That way, we can easily change its functions:
    # ideally, variables like this one should be properties
                            # we’d have to write a class whose instances have these properties,
                            # but Python allows us to create a property for a single instance


 # when a button is clicked, we choose what exactly happens

# Everything is set up. Now we ask the question and show the window:


window = QWidget()
window.setLayout(layout_card)
window.score = 0
window.total = 0

btn_OK.clicked.connect(click_OK)
window.setWindowTitle('Memo Card')
window.cur_question = -1
next_question()
window.show()


app.exec()