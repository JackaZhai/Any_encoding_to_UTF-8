import os
import chardet
import tkinter as tk
from tkinter import filedialog, messagebox

def detect_encoding(file_path):
    """检测文件的编码"""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def convert_to_utf8(file_path):
    try:
        # 检测文件编码
        encoding = detect_encoding(file_path)
        if not encoding:
            raise ValueError("无法检测文件编码")

        # 使用检测到的编码读取文件内容
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()

        # 将文件内容写回为 UTF-8 编码
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Converted: {file_path}")
    except Exception as e:
        print(f"Failed to convert {file_path}: {e}")

def batch_convert(folder_path, file_extension):
    for root1, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(file_extension):
                file_path = os.path.join(root1, file_name)
                convert_to_utf8(file_path)
    messagebox.showinfo("完成", f"所有文件已成功转换为 UTF-8！")

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        batch_convert(folder_path, selected_extension.get())

# 创建主窗口
root = tk.Tk()
root.title("编码转换器")

# 创建一个标签
label = tk.Label(root, text="请选择要转换的文件夹：")
label.pack(pady=10)

# 文件类型选择
file_types = ['.cpp', '.c', '.py', '.java']
selected_extension = tk.StringVar(root)
selected_extension.set(file_types[0])  # 设置默认文件类型

file_type_menu = tk.OptionMenu(root, selected_extension, *file_types)
file_type_menu.pack(pady=10)

# 创建一个按钮来选择文件夹
select_button = tk.Button(root, text="选择文件夹", command=select_folder)
select_button.pack(pady=20)

# 运行 GUI
root.mainloop()
