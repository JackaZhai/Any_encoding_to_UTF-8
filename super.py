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

def convert_to_utf8(file_path, target_encoding):
    try:
        # 检测文件编码
        encoding = detect_encoding(file_path)
        if not encoding:
            raise ValueError("无法检测文件编码")

        # 使用检测到的编码读取文件内容
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()

        # 将文件内容写回为目标编码
        with open(file_path, 'w', encoding=target_encoding) as file:
            file.write(content)

        print(f"Converted: {file_path}")
    except Exception as e:
        print(f"Failed to convert {file_path}: {e}")

def batch_convert(folder_path, file_extension, target_encoding):
    for root1, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(file_extension):
                file_path = os.path.join(root1, file_name)
                convert_to_utf8(file_path, target_encoding)
    messagebox.showinfo("完成", f"所有文件已成功转换为 {target_encoding} 编码！")

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        batch_convert(folder_path, selected_extension.get(), selected_encoding.get())

# 创建主窗口
root = tk.Tk()
root.title("编码转换器")

# 创建一个标签
label = tk.Label(root, text="请选择要转换的文件后缀名和目标编码后，选择要转换的文件夹：")
label.pack(pady=10)

# 文件类型选择
file_types = ['.cpp', '.c', '.py', '.java']
selected_extension = tk.StringVar(root)
selected_extension.set(file_types[0])  # 设置默认文件类型

file_type_menu = tk.OptionMenu(root, selected_extension, *file_types)
file_type_menu.pack(pady=10)

# 编码选择
encodings = ['utf-8', 'utf-16', 'latin-1', 'ascii']
selected_encoding = tk.StringVar(root)
selected_encoding.set(encodings[0])  # 设置默认编码

encoding_menu = tk.OptionMenu(root, selected_encoding, *encodings)
encoding_menu.pack(pady=10)

# 创建一个按钮来选择文件夹
select_button = tk.Button(root, text="选择文件夹", command=select_folder)
select_button.pack(pady=20)

# 运行 GUI
root.mainloop()