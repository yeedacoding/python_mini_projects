from tkinter import *


def click(key):
    if key == '=':
        try:
            result = eval(entry.get())  # entry.get() ->기입창의 텍스트를 문자열로 반환
            # 0 = entry위젯이서 첫 번째 문자 / END = entry위젯에서 마지막 컨텐츠
            entry.delete(0, END)
            entry.insert(END, str(result))
        except:
            entry.insert(END, "오류가 발생했습니다.")  # 정상적인 입력이 일어나지 않으면 오류 발생
    elif key == 'C':
        entry.delete(0, END)  # 'C'를 누르면 마찬가지로 다 지우기
    else:
        # 누른 버튼이 '='가 아니라면 마지막으로 입력한 문자 다음으로도 계속 문자를 받을 수 있도록 설정
        entry.insert(END, key)


window = Tk()
window.title("태헌의 계산기")
window.geometry("349x565")          # 생성되는 window 창의 너비x높이 설정
window.resizable(False, False)      # window창의 사이즈 조절 여부(너비, 높이)
window.configure(bg='white')


# 화면을 구성할 요소들을 작성

buttons = ['C', '/',
           '7', '8', '9', '*',
           '4', '5', '6', '-',
           '1', '2', '3', '+',
           '0', '.', '=']


entry = Entry(window, width=20, bg='white', borderwidth=0, font=('arial', 20, 'bold'),
              fg="black", insertbackground="black", justify="right")
entry.grid(row=0, column=0, columnspan=5, ipady=50)
# 하위 버튼들의 column 갯수가 5개이므로 columnspan = 5


i = 0
for button in buttons:  # for문을 통해 buttons 리스트에 있는 요소들을 하나씩 가져와 검사

    # 포문 안에서 함수정의하면 포문 돌때마다 재정의... 낭비..
    def cmd(x=button):  # 모든 버튼에 cmd함수 적용
        return click(x)

    if button.isdigit() == False:  # button가 숫자가 아니면 색깔은 노랑색
        color = "yellow"
    else:
        color = "white"

    # 예외처리로 시도해봤지만 실패
    # number인지 operator인지 판단하여 각각의 위치와 디자인을 지정
    main_button = Button(window, text=button, width=11, height=5, padx=1,
                         relief="ridge", bg=color, command=cmd)

    if button == "0":
        # 반복되는 문장들은 깔끔하게 만들 수 있으면 좋을텐데..
        button1 = Button(window, text=button, width=22,
                         height=5,  padx=6, relief="ridge", bg=color, command=cmd)
        button1.grid(row=5, column=0, columnspan=2)
    elif button == ".":
        button2 = main_button
        button2.grid(row=5, column=2)
    elif button == "=":
        button3 = main_button
        button3.grid(row=5, column=3)
    elif button == "C":
        button4 = Button(window, text=button, width=35,
                         height=5,  padx=4, relief="ridge", bg="orange", command=cmd)
        button4.grid(row=1, column=0, columnspan=3)
    elif button == "/":
        button5 = main_button
        button5.grid(row=1, column=3)
    else:
        button = main_button
        button.grid(row=(i//4)+2, column=i % 4)  # entry와 row=1 이후에 버튼이 생성됨
        i += 1


window.mainloop()