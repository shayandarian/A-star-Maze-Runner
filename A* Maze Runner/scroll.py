# CODE FROM https://www.joehutch.com/posts/tkinter-dynamic-scroll-area/
# CODE FROM https://www.joehutch.com/posts/tkinter-dynamic-scroll-area/
# CODE FROM https://www.joehutch.com/posts/tkinter-dynamic-scroll-area/


import tkinter as tk

root = tk.Tk()

# Tkinter widgets needed for scrolling.  The only native scrollable container that Tkinter provides is a canvas.
# A Frame is needed inside the Canvas so that widgets can be added to the Frame and the Canvas makes it scrollable.
cTableContainer = tk.Canvas(root)
fTable = tk.Frame(cTableContainer)
sbHorizontalScrollBar = tk.Scrollbar(root)
sbVerticalScrollBar = tk.Scrollbar(root)

# Updates the scrollable region of the Canvas to encompass all the widgets in the Frame
def updateScrollRegion():
	cTableContainer.update_idletasks()
	cTableContainer.config(scrollregion=fTable.bbox())

# Sets up the Canvas, Frame, and scrollbars for scrolling
def createScrollableContainer():
	cTableContainer.config(xscrollcommand=sbHorizontalScrollBar.set,yscrollcommand=sbVerticalScrollBar.set, highlightthickness=0)
	sbHorizontalScrollBar.config(orient=tk.HORIZONTAL, command=cTableContainer.xview)
	sbVerticalScrollBar.config(orient=tk.VERTICAL, command=cTableContainer.yview)

	sbHorizontalScrollBar.pack(fill=tk.X, side=tk.BOTTOM, expand=tk.FALSE)
	sbVerticalScrollBar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
	cTableContainer.pack(fill=tk.BOTH, side=tk.LEFT, expand=tk.TRUE)
	cTableContainer.create_window(0, 0, window=fTable, anchor=tk.NW)

createScrollableContainer()