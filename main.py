import os
import chardet
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def detect_encoding(file_path):
    """检测文件的编码"""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def convert_to_utf8(file_path, log_widget):
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

        log_widget.insert(tk.END, f"Converted: {file_path}\n")
    except Exception as e:
        log_widget.insert(tk.END, f"Failed to convert {file_path}: {e}\n")

def batch_convert(folder_path, file_extensions, log_widget):
    for root1, dirs, files in os.walk(folder_path):
        for file_name in files:
            if any(file_name.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root1, file_name)
                convert_to_utf8(file_path, log_widget)
    messagebox.showinfo("完成", "所有文件已成功转换为 UTF-8！")

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        log_widget.delete(1.0, tk.END)  # 清空日志
        batch_convert(folder_path, selected_extensions.get().split(','), log_widget)

# 创建主窗口
root = tk.Tk()
root.title("编码转换器")

# 创建一个标签
label = tk.Label(root, text="请选择要转换的文件类型和文件夹：")
label.pack(pady=10)

# 文件类型选择
file_types = ['.cpp', '.c', '.py', '.java']
selected_extensions = tk.StringVar(root)
selected_extensions.set(file_types[0])  # 设置默认文件类型

file_type_menu = tk.OptionMenu(root, selected_extensions, *file_types)
file_type_menu.pack(pady=10)

# 创建一个按钮来选择文件夹
select_button = tk.Button(root, text="选择文件夹", command=select_folder)
select_button.pack(pady=10)

# 创建一个滚动文本框来显示日志
log_widget = scrolledtext.ScrolledText(root, width=80, height=20)
log_widget.pack(pady=10)

# 运行 GUI
root.mainloop()