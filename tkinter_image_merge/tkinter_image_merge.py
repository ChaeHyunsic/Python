from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk

root = Tk()     # tkinter 호출
root.title("image_merge")   # 타이틀 설정

# 파일 추가, 파일 삭제 기능 설정
def add_file():
    files = filedialog.askopenfilenames(title = "이미지 파일을 선택하세요", filetypes = (("PNG 파일", "*.png"), ("모든 파일", "*.*")), initialdir = r"D:\작업\Python\tkinter_image_merge")

    for file in files:
        list_file.insert(END, file)

def del_file():
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

# 파일 추가, 파일 삭제 기능 frame 설정
file_frame = Frame(root)
file_frame.pack(fill = "x", padx = 5, pady = 5)

btn_add_file = Button(file_frame, padx = 5, pady = 5, width = 12, text = "파일추가", command = add_file)
btn_add_file.pack(side = "left")

btn_del_file = Button(file_frame, padx = 5, pady = 5, width = 12, text = "파일삭제", command = del_file)
btn_del_file.pack(side = "right")

# 추가된 파일 목록 기능 frame 설정
list_frame = Frame(root)
list_frame.pack(fill = "both", padx = 5, pady = 5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side = "right", fill = "y")

list_file = Listbox(list_frame, selectmode = "extended", height = 15, yscrollcommand = scrollbar)
list_file.pack(side = "left", fill = "both", expand = True)
scrollbar.config(command = list_file.yview)

# 저장 경로 선택 기능 설정
def browse_path():
    selected = filedialog.askdirectory()
    if selected == '':
        return
    save_path.delete(0, END)
    save_path.insert(0, selected)

# 저장 경로 선택 기능 frame 설정
path_frame = LabelFrame(root, text = "저장경로")
path_frame.pack(fill = "x", padx = 5, pady = 5, ipady = 5)

save_path = Entry(path_frame)
save_path.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5, ipady = 4)

btn_save_path = Button(path_frame, text = "찾아보기", width = 10, command = browse_path)
btn_save_path.pack(side = "right", padx = 5, pady = 5)

# 부가 옵션 기능 frame 설정
option_frame = LabelFrame(root, text = "옵션")
option_frame.pack(padx = 5, pady = 5, ipady = 5)

# 부가 옵션 기능(가로 넓이 지정) frame 설정
width_label = Label(option_frame, text = "가로넓이", width = 8)
width_label.pack(side = "left", padx = 5, pady = 5)

width_option = ["원본유지", "1024", "800", "640"]
width_combo = tkinter.ttk.Combobox(option_frame, state = "readonly", values = width_option, width = 10)
width_combo.current(0)
width_combo.pack(side = "left", padx = 5, pady = 5)

# 부가 옵션 기능(세로 간격 지정) frame 설정
space_label = Label(option_frame, text = "간격", width = 8)
space_label.pack(side = "left", padx = 5, pady = 5)

space_option = ["없음", "좁게", "보통", "넓게"]
space_combo = tkinter.ttk.Combobox(option_frame, state = "readonly", values = space_option, width = 10)
space_combo.current(0)
space_combo.pack(side = "left", padx = 5, pady = 5)

# 부가 옵션 기능 (포맷 지정) frame 설정
format_label = Label(option_frame, text = "포맷", width = 8)
format_label.pack(side = "left", padx = 5, pady = 5)

format_option = [".PNG", ".JPG", ".BMP"]
format_combo = tkinter.ttk.Combobox(option_frame, state = "readonly", values = format_option, width = 10)
format_combo.current(0)
format_combo.pack(side = "left", padx = 5, pady = 5)

# 진행 상황 표시 기능 frame 설정
progress_frame = LabelFrame(root, text = "진행상황")
progress_frame.pack(fill = "x", padx = 5, pady = 5, ipady = 5)

prog_var = DoubleVar()
progress_bar = tkinter.ttk.Progressbar(progress_frame, maximum = 100, variable = prog_var)
progress_bar.pack(fill = "x", padx = 5, pady = 5)

# image merge 실행 기능 설정
def start():
    if list_file.size() == 0:   # 선택된 이미지가 없을 경우
        messagebox.showwarning("경고", "이미지 파일을 추가하세요")
        return

    if len(save_path.get()) == 0:
        messagebox.showwarning("경고", "저장 경로를 선택하세요")
        return

# image merge 실행 기능 frame 설정
run_frame = Frame(root)
run_frame.pack(fill = "x", padx = 5, pady = 5)

btn_close = Button(run_frame, padx = 5, pady = 5, text = "닫기", width = 12, command = root.quit)
btn_close.pack(side = "right", padx = 5, pady = 5)

btn_start = Button(run_frame, padx = 5, pady = 5, text = "시작", width = 12, command = start)
btn_start.pack(side = "right", padx = 5, pady = 5)

root.resizable(False, False)  # 창 크기 변경 불가
root.mainloop()     # 메인 루프 진행