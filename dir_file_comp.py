# This is a sample Python script.

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
import pandas as pd
import xlsxwriter


def ClickFileOpen(text_field):
    full_file_name = filedialog.askopenfilename(initialdir="C:/Temp", title="Choose your file",
                                                filetypes=(("all files", "*.*"), ("jpeg files", "*.jpg")))
    text_field.set(full_file_name)


def ClickFileSave(text_field):
    full_file_name = filedialog.asksaveasfilename(initialdir="C:/Temp", title="Choose your file",
                                                  filetypes=(("Excel 통합문서", "*.xlsx"), ("all files", "*.*")))
    text_field.set(full_file_name)


def get_size_bytes(size, size_key):
    size_in_byte = 0.0
    if size_key == 'B':  # bytes
        size_in_byte = size
    if size_key == 'K':  # kilobytes
        size_in_byte = size * 1024
    if size_key == 'M':  # megabytes
        size_in_byte = size * 1024 * 1024
    if size_key == 'G':  # gigabytes
        size_in_byte = size * 1024 * 1024 * 1024
    if size_key == 'T':  # terabytes
        size_in_byte = size * 1024 * 1024 * 1024 * 1024
    return size_in_byte


def build_old_list(full_path_file):
    f = open(full_path_file, 'r')
    lines = f.readlines()
    f.close()

    column_fields = ['Type Permission', 'NO Hard Link', 'Owner', 'Group', 'Size', 'Date Time', 'Name', 'Path' ]

    f_type_permission = []
    f_no_hard_link = []
    f_owner = []
    f_group = []
    f_size = []
    f_date_time = []
    f_name = []
    f_path = []
    in_path = ''

    for line in lines :
        columns = line.split()
        if len(columns) == 1:
            column = columns[0]
            if '.' == column[0:1]:      # '.' path
                in_path = columns[0]
        if len(columns) > 8 :
            column = columns[0]
            if '-' == column[0:1] :     # 'd' directory, '-' file
                file_date_time = columns[5] + ' ' + columns[6] + ' ' + columns[7]
                file_name = ''
                for i in range(8, len(columns)) :
                    file_name = file_name + columns[i] + ' '
                f_type_permission.append(columns[0])
                f_no_hard_link.append(columns[1])
                f_owner.append(columns[2])
                f_group.append(columns[3])
                f_size.append(columns[4])
                f_date_time.append(file_date_time)
                f_name.append(file_name.rstrip())
                f_path.append(in_path)

    # print(f_type_permission)
    # print(f_date_time)
    # print(f_name)

    df = pd.DataFrame(columns=column_fields)
    df['Type Permission'] = f_type_permission
    df['NO Hard Link'] = f_no_hard_link
    df['Owner'] = f_owner
    df['Group'] = f_group
    df['Size'] = f_size
    df['Date Time'] = f_date_time
    df['Name'] = f_name
    df['Path'] = f_path
    return df


def build_new_list(full_path_file):
    f = open(full_path_file, 'r')
    lines = f.readlines()
    f.close()

    column_fields = ['Type Permission', 'NO Hard Link', 'Owner', 'Group', 'Size', 'Date Time', 'Name', 'Path' ]

    f_type_permission = []
    f_no_hard_link = []
    f_owner = []
    f_group = []
    f_size = []
    f_date_time = []
    f_name = []
    f_path = []
    in_path = ''
    for line in lines :
        columns = line.split()
        if len(columns) == 1:
            column = columns[0]
            if '.' == column[0:1]:  # '.' path
                in_path = columns[0]
        if len(columns) > 8 :
            column = columns[0]
            if '-' == column[0:1] :     # 'd' directory, '-' file
                file_date_time = columns[5] + ' ' + columns[6] + ' ' + columns[7]
                file_name = ''
                for i in range(8, len(columns)) :
                    file_name = file_name + columns[i] + ' '
                f_type_permission.append(columns[0])
                f_no_hard_link.append(columns[1])
                f_owner.append(columns[2])
                f_group.append(columns[3])
                f_size.append(columns[4])
                f_date_time.append(file_date_time)
                f_name.append(file_name.rstrip())
                f_path.append(in_path)

    # print(f_type_permission)
    # print(f_date_time)
    # print(f_name)

    df = pd.DataFrame(columns=column_fields)
    df['Type Permission'] = f_type_permission
    df['NO Hard Link'] = f_no_hard_link
    df['Owner'] = f_owner
    df['Group'] = f_group
    df['Size'] = f_size
    df['Date Time'] = f_date_time
    df['Name'] = f_name
    df['Path'] = f_path
    return df


def isExistFile(path_file):
    # 파일 유무 검사
    if path_file == '':
        error_message = "공백인 파일명은 사용할 수 없습니다\n"
        msg = messagebox.showerror("Error File Name", error_message)
        return False
    file = Path(path_file)
    if not file.exists():
        error_message = str(path_file) + "파일이 없습니다\n"
        msg = messagebox.showerror("Error File Name", error_message)
        return False
    return True


def create_excel(old_df, new_df):

    excel_file = Path(txtTargetFile.get())

    excel_writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    old_df.to_excel(excel_writer, sheet_name='IBM', index=False)
    new_df.to_excel(excel_writer, sheet_name='AWS', index=False)
    excel_writer.save()


def ClickBuildCompFile():
    report_df = pd.DataFrame()

    # 파일 유무 검사
    in_text = txtSourceFile1.get()
    if not isExistFile(in_text):
        return
    in_text = txtSourceFile2.get()
    if not isExistFile(in_text):
        return

    file_name = Path(txtSourceFile1.get())
    old_df = build_old_list(file_name)
    file_name = Path(txtSourceFile2.get())
    new_df = build_new_list(file_name)

    old_df = old_df.astype({'Size':'int'})      # Size 칼럼을 integer 로 변경
    sum_old_df = old_df['Size'].sum()
    print(sum_old_df)

    new_df = new_df.astype({'Size':'int'})      # Size 칼럼을 integer 로 변경
    sum_new_df = new_df['Size'].sum()
    print(sum_new_df)

    create_excel(old_df, new_df)

    msgbox_info = "디렉토리/파일 비교 결과 파일이 생성되었습니다\n"
    msg = messagebox.showinfo("DIR/FILE", msgbox_info)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    window = Tk()
    window.title("Progress DIR/FILE Analysis")
    window.geometry("500x160")
    window.resizable(False, False)

    lblBlank = Label(window, text=' ')
    lblTitle = Label(window, text=' 이 프로그램은 디렉토리/파일 비교 결과를 생성합니다')
    lblSourceFile1 = Label(window, text=' Source 파일 : ')
    lblSourceFile2 = Label(window, text=' Target 파일 : ')
    lblTargetFile = Label(window, text='  결과 파일 : ')

    in_text_source1 = StringVar()
    in_text_source2 = StringVar()
    in_text_target = StringVar()
    txtSourceFile1 = Entry(window, textvariable=in_text_source1, width=40)
    txtSourceFile2 = Entry(window, textvariable=in_text_source2, width=40)
    txtTargetFile = Entry(window, textvariable=in_text_target, width=40)

    btnSourceFile1 = Button(window, text="...", command=lambda: ClickFileOpen(in_text_source1))
    btnSourceFile2 = Button(window, text="...", command=lambda: ClickFileOpen(in_text_source2))
    btnTargetFile = Button(window, text="...", command=lambda: ClickFileSave(in_text_target))
    btnBuildTarget = Button(window, text="비교 결과 파일 생성", command=ClickBuildCompFile)

    lblTitle.grid(row=0, column=2)

    lblSourceFile1.grid(row=1, column=0)
    txtSourceFile1.grid(row=1, column=2)
    btnSourceFile1.grid(row=1, column=3)

    lblSourceFile2.grid(row=2, column=0)
    txtSourceFile2.grid(row=2, column=2)
    btnSourceFile2.grid(row=2, column=3)

    lblBlank.grid(row=3, column=0)

    lblTargetFile.grid(row=4, column=0)
    txtTargetFile.grid(row=4, column=2)
    btnTargetFile.grid(row=4, column=3)

    btnBuildTarget.grid(row=5, column=1, columnspan=2)

    window.mainloop()