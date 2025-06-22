import pyperclip
import keyboard
import pyautogui
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
import sys

clipboard_queue = []
multi_copy_enabled = False

# GUI setup
root = tk.Tk()
#icon = tk.PhotoImage(file="multicopy.png")
#root.iconphoto(True, icon)
root.iconbitmap("multicopy.ico")

root.title("MultiCopy")
root.geometry("500x260")
root.resizable(False, False)


# Tkinter variables
status_var = tk.StringVar(value="Multi-Copy Mode: OFF")
checkbox_var = tk.BooleanVar(value=False)

# ========== FUNCTIONALITY ==========

def toggle_multi_copy_gui():
    toggle_multi_copy()
    checkbox_var.set(multi_copy_enabled)

def toggle_multi_copy_hotkey():
    toggle_multi_copy()
    checkbox_var.set(multi_copy_enabled)

def toggle_multi_copy():
    global multi_copy_enabled
    multi_copy_enabled = not multi_copy_enabled
    status = "ON" if multi_copy_enabled else "OFF"
    #status_var.set(f"Multi-Copy Mode: {status}")
    #print(f"[Multi-Copy] {status}")
    
def safe_copy(text, max_retries=5, delay=1):
    for _ in range(max_retries):
        print("\n*****Printing the text in FIFO*****\n")
        print(text)
        print("\n****End****\n")

        print("\n*****pyperclip.paste()*****\n")
        print(pyperclip.paste())
        print("\n****End pyperclip.paste()****\n")
        
        pyperclip.copy(" ")
        pyperclip.copy(text)
        time.sleep(delay)
        print("\n*****pyperclip.paste() 2nd time *****\n")
        print(pyperclip.paste())
        print("\n****End pyperclip.paste()****\n")        
        if pyperclip.paste() == text:
            return True
        else:
            print("clipboard not synced")
    return False    

def paste_all_fifo():
    if clipboard_queue:
        combined_text = '\n\n'.join(clipboard_queue)+ '\n'
        
        if safe_copy(combined_text):
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'v')
            clipboard_queue.clear()
            print("FIFO Paste executed.")
        else:
            print("Failed to update clipboard reliably.")
    else:
        print("Clipboard queue is empty.")
        

def on_copy_event():
    time.sleep(0.1)
    if multi_copy_enabled:
        copied = pyperclip.paste()
        if not clipboard_queue or copied != clipboard_queue[-1]:
            clipboard_queue.append(copied)
            print(f"[+ Copied] {copied[:40]}...")


def show_copied_items():
    show_window = tk.Toplevel(root)
    show_window.title("Copied Items")
    show_window.geometry("700x400")  # initial size
    show_window.minsize(400, 200)    # optional: prevent too small
    
    icon = tk.PhotoImage(file="multicopy.png")    
    show_window.iconphoto(True, icon)

    # Make the window resizable
    show_window.columnconfigure(0, weight=1)
    show_window.rowconfigure(0, weight=1)

    # Add ScrolledText that expands with window
    text_area = scrolledtext.ScrolledText(show_window, wrap=tk.WORD, font=("Segoe UI", 10))
    text_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))

    # Pre-fill with copied queue
    text_area.insert(tk.END, '\n\n'.join(clipboard_queue) + '\n')

    # Add button frame
    button_frame = tk.Frame(show_window)
    button_frame.grid(row=1, column=0, pady=10)

    def copy_modified_content():
        content = text_area.get("1.0", tk.END).strip()
        if content:
            pyperclip.copy(content)
            time.sleep(0.2)
            clipboard_queue.clear()

    paste_button = tk.Button(button_frame, text="Copy Edited Content", command=copy_modified_content, bg="#5cb85c", fg="white")
    paste_button.pack()
 

def stop_app():
    print("Shutting down...")
    root.destroy()
    sys.exit()

# ========== GUI LAYOUT ==========
tk.Label(root, text="Keyboard Shortcuts:", font=("Segoe UI", 9, "bold")).pack(pady=(10, 0))

instructions = (
    "Ctrl+C       → Copy\n"
    "Ctrl+Shift+P → Paste All (FIFO)"
)
#tk.Label(root, textvariable=status_var, font=("Segoe UI", 9, "bold")).pack(pady=5)
tk.Checkbutton(root, text="Enable Multi-Copy or Ctrl+Shift+M to toggle", variable=checkbox_var, command=toggle_multi_copy_gui).pack()
tk.Label(root, text=instructions, justify='left', font=("Segoe UI", 9, "bold")).pack()
tk.Button(root, text="Edit Copied Items", command=show_copied_items, width=30).pack(pady=5)
#tk.Button(root, text="Paste All (FIFO) or Ctrl+Shift+P", command=paste_all_fifo, bg="#0275d8", fg="white", width=30).pack(pady=5)
tk.Button(root, text="Exit", command=stop_app, bg="#d9534f", fg="white", width=10).pack(pady=10)

# ========== HOTKEYS ==========
def background_hotkeys():
    keyboard.add_hotkey('ctrl+shift+M', toggle_multi_copy_hotkey)
    keyboard.add_hotkey('ctrl+shift+P', paste_all_fifo)
    keyboard.add_hotkey('ctrl+c', on_copy_event)
    keyboard.wait()

threading.Thread(target=background_hotkeys, daemon=True).start()

# Start GUI loop
root.mainloop()
