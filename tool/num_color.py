import tkinter as tk

def show_text():
    text = entry.get()

    # Textを初期化
    output.delete("1.0", tk.END)

    for ch in text:
        if ch == "0":
            tag = "zero"
        elif ch == "1":
            tag = "one"
        elif ch == "2":
            tag = "two"
        elif ch == "3":
            tag = "three"
        else:
            tag = "other"

        output.insert(tk.END, ch, tag)

# ウィンドウ
root = tk.Tk()
root.title("文字ごと色分けGUI")
root.geometry("400x200")

# 入力欄
entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10)

# ボタン
tk.Button(root, text="表示", command=show_text).pack()

# 出力用 Text（編集不可）
output = tk.Text(root, height=2, font=("Arial", 16))
output.pack(pady=10)
output.config(state=tk.NORMAL)

# 色設定
output.tag_config("zero",  foreground="red")
output.tag_config("one",   foreground="blue")
output.tag_config("two",   foreground="green")
output.tag_config("three", foreground="orange")
output.tag_config("other", foreground="black")

root.mainloop()
