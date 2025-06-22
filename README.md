# Multicopy
### Introducing Custom MultiCopy Tool – Built to Do One Thing Well

Have you ever found yourself needing to copy multiple pieces of information like notes, documentation, or code snippets, and wished to paste them all efficiently in one go, in the order you copied them?

That’s the idea behind MultiCopy - a lightweight clipboard assistant built using Python. It lets you:

-  Toggle MultiCopy Mode using a keyboard shortcut (e.g., Ctrl+Shift+M)
-  Copy multiple items from anywhere — files, websites, code editors
-  Paste everything in one go (Ctrl+Shift+P), maintaining the exact order (FIFO)
-  View and edit the collected items in a simple text window
-  Click “Copy Edited Content” and use Ctrl+V wherever you like
-  Keep full control of the clipboard - no background sync, no cloud, no bloat


MultiCopy is my personal solution to solve a problem. It is a focused utility that helps me gather multiple snippets and paste them exactly once, and in one go, cleanly and efficiently.

If you’ve ever wished your clipboard could do a little more, you might enjoy trying this. Just download the executable along with the PNG and ICO files. It has a simple GUI and self-guided help to use it. The code is available on GitHub if you want to extend it for your needs.


#### create the executable using the command
```
pyinstaller --onefile --noconsole --icon=multicopy.ico multicopyv1.py
```
