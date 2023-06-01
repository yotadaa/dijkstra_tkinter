import heapq
import tkinter as tk
from tkinter import font
import math
from pprint import pprint


class TableForm(tk.Frame):
    def __init__(self, master, data):
        super().__init__(master)
        self.data = data
        self.rows = len(data)
        self.columns = len(data[0])
        self.create_table()

    def create_table(self):
        # Create table headers
        for col in range(self.columns):
            header_label = tk.Label(self, text=list(self.data[0].keys())[col], relief=tk.RIDGE, width=15)
            header_label.grid(row=0, column=col, sticky="nsew")

        # Create table data
        for row in range(self.rows):
            for col in range(self.columns):
                attribute_value = self.data[row][list(self.data[0].keys())[col]]
                print(type(attribute_value))
                if type(attribute_value) == list:
                    attribute_value = [i.nama for i in attribute_value]
                elif type(attribute_value) == Node:
                    attribute_value = attribute_value.nama
                if type(attribute_value) == dict:
                    attribute_value = attribute_value.values()
                cell_label = tk.Label(self, text=attribute_value, relief=tk.RIDGE, width=15)
                cell_label.grid(row=row + 1, column=col, sticky="nsew")

        # Configure grid weights to expand the table
        for i in range(self.rows + 1):
            self.grid_rowconfigure(i, weight=1)

        for j in range(self.columns):
            self.grid_columnconfigure(j, weight=1)


class Node:
    def __init__(self,master,x,y):
        self.nama = ''
        self.x,self.y = x,y
        self.focused = False
        self.widget = master.create_oval(x-20,y-20,x+20,y+20,width=2,fill='white',tag='node')
        self.link = []
        self.dist = []

    def __lt__(self, other):
        return self.nama < other.nama

    def __eq__(self, other):
        return self.nama == other.nama

    def __hash__(self):
        return hash(self.nama)
class App:
    def __init__(self,root):
        self.char = ''
        self.pick = False
        self.create = True
        self.path = []
        self.beginNode = None
        self.endNode = None
        self.root = root
        self.currentColor = ''
        self.color_list = ['red', 'green', 'aqua', 'yellow', 'orange', 'purple', 'pink', 'brown', 'magenta']
        self.namaList = []
        self.lineList=[]
        self.lineListCount = -1
        self.namaewa = ''
        self.top = False
        self.currentInput = None
        self.toDestroy=False
        self.canvas = tk.Canvas(self.root, bg='white', width=800,height=600)
        self.canvas.pack()
        self.onFocus = None
        self.node = []
        self.count = -1
        self.line=[]
        self.lc = -1
        self.label = None
        self.tempLine=self.canvas.create_line(0,0,0,0,width=3)
        self.is_maximized = self.root.wm_state() == 'zoomed'

        self.statusText = 'MODE : EDIT'
        self.status = self.canvas.create_text(400,50 ,text=self.statusText,font= font.Font(size=16))
        self.charWidget = self.canvas.create_text(10,50,text=self.char,anchor='w',font=font.Font(size=16))

        self.canvas.bind("<Button-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)
        self.root.bind('<Configure>',self.rootUpdate)
        self.root.bind('<space>',self.space)
        self.root.bind('<Motion>',self.wondering)
        self.root.bind('<BackSpace>',self.reset)
        self.root.bind('<Button-3>',self.reset)
        self.root.bind('<Return>',self.shortestPath)
        self.root.bind('<Tab>',self.changeMode)
        self.root.bind('<KeyPress>', self.keyPressed)
        self.root.bind("<KeyRelease>",self.keyReleased)

    def keyPressed(self,e):#mukhtada
        self.char = e.char
        self.canvas.itemconfigure(self.charWidget,text=self.char)
    def keyReleased(self,e):
        self.char = ''
        self.canvas.itemconfigure(self.charWidget, text=self.char)
    def changeMode(self,e):
        self.reset(None)
        if self.create == True:
            self.statusText= 'MODE : PILIH AWAL DAN AKHIR'
            self.create = False
        else:
            self.statusText = 'MODE : EDIT'
            self.create = True
        self.canvas.itemconfigure(self.status,text=self.statusText)

    def check(self,e):
        pass

    def dijkstra(self, start_node, end_node):
        distances = {node: float('inf') for node in self.node}
        distances[start_node] = 0
        previous_nodes = {node: None for node in self.node}
        queue = [(0, start_node)]

        process = []
        process.append({
            'current_node': start_node,
            'visited_nodes': [],
            'unvisited_nodes': self.node,
            'distances': distances.copy()
        })

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_node == end_node:
                path = []
                while current_node is not None:
                    path.insert(0, current_node)
                    current_node = previous_nodes[current_node]
                return path, process

            if current_distance > distances[current_node]:
                continue

            for neighbor, distance in zip(current_node.link, current_node.dist):
                new_distance = current_distance + int(distance)
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(queue, (new_distance, neighbor))

            process.append({
                'current_node': current_node,
                'visited_nodes': list(process[-1]['visited_nodes']) + [current_node],
                'unvisited_nodes': list(process[-1]['unvisited_nodes']),
                'distances': distances.copy()
            })
            process[-1]['unvisited_nodes'].remove(current_node)

        return None, process

    def shortestPath(self,e):
        if self.beginNode and self.endNode:
            pathway_items = self.canvas.find_withtag('pathway')
            self.canvas.delete(*pathway_items)
            self.path,self.processes = self.dijkstra(self.beginNode, self.endNode)
            if self.beginNode is not None and self.endNode is not None:
                for i in range(len(self.path)-1):
                    coords1 = self.canvas.coords(self.path[i].widget)
                    coords2 = self.canvas.coords(self.path[i+1].widget)
                    x1,y1 = coords1[0]+20,coords1[1]+20
                    x2,y2 = coords2[0]+20,coords2[1]+20
                    self.canvas.create_line(x1,y1,x2,y2,tag='pathway',fill='red',width=5)
                self.canvas.tag_raise('node')
                self.canvas.tag_raise('nama')
                self.canvas.tag_raise('distCount')
            self.beginNode = None
            self.endNode = None
            runProcesses = TableForm(self.root,self.processes)
            runProcesses.place(x=0,y=0,relwidth=1)

    def rootUpdate(self, e):
        tags = e.widget
        self.is_maximized = self.root.wm_state() == 'zoomed'
        if self.is_maximized:
            self.canvas.config(width=self.root.winfo_width(), height=self.root.winfo_height())
            self.canvas.coords(self.status,self.root.winfo_width()//2,50)
        else:
            self.canvas.config(width=800, height=600)
        self.root.minsize(800, 600)


    def validate_input(self,text):
        if text.isdigit() or not text:
            self.toDestroy = True
            return True
        return False
    def save_input(self,e):
        self.currentInput = self.entry_var.get()
        self.cancel = False
        if self.toDestroy:
            self.root.unbind_all('<Configure>')
            self.popup.destroy()
    def create_popup(self,e):
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Popup Window")
        self.popup.attributes('-topmost', True)
        self.popup.resizable(False, False)
        self.popup.configure(borderwidth=2, highlightthickness=2)
        self.popup.overrideredirect(True)

        main_window_width = self.root.winfo_width()
        main_window_height = self.root.winfo_height()
        popup_width = 200
        popup_height = 150
        x = self.root.winfo_rootx() + self.root.winfo_width() // 2 - popup_width // 2
        y = self.root.winfo_rooty() + self.root.winfo_height() // 2 - popup_height // 2

        self.popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        label = tk.Label(self.popup, text='Jarak')
        label.pack()

        self.entry_var = tk.StringVar()
        validate_cmd = (self.popup.register(self.validate_input), '%P')
        self.entry = tk.Entry(self.popup, textvariable=self.entry_var, validate='key', validatecommand=validate_cmd)
        self.entry.pack(pady=20)
        exit_button=tk.Button(self.popup,text='Batal',command=self.exiting)
        exit_button.pack(side=tk.LEFT)
        save_button = tk.Button(self.popup, text="Save")
        save_button.pack(side=tk.RIGHT)
        save_button.bind('<Button-1>',self.save_input)
        self.popup.bind("<Return>",self.save_input)

        self.popup.grab_set()
        self.popup.focus_set()
        self.root.bind('<Configure>',self.popupUpdate)

        self.popup.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close button

        self.popup.wait_window()

    def exiting(self):
        self.cancel = True
        self.popup.destroy()

    def popupUpdate(self,e):
        popup_width = 200
        popup_height = 150
        x = self.root.winfo_rootx() +  self.root.winfo_width() // 2 - popup_width // 2
        y = self.root.winfo_rooty() +  self.root.winfo_height() // 2 - popup_height // 2
        self.popup.geometry(f"+{x}+{y}")


    def validate_input2(self, text):
        if not text:
            self.toDestroy = True
            return True
        return False

    def save_input2(self):
        self.namaewa = self.entry_var2.get()
        self.root.unbind_all('<Configure>')
        self.popup2.destroy()

    def create_popup2(self, e):
        self.popup2 = tk.Toplevel(self.root)
        self.popup2.title("Popup Window")
        self.popup2.attributes('-topmost', True)
        self.popup2.resizable(False, False)
        self.popup2.overrideredirect(True)
        self.popup2.configure(borderwidth=2, highlightthickness=2)
        main_window_width = self.root.winfo_width()
        main_window_height = self.root.winfo_height()
        popup_width = 200
        popup_height = 300#mukhtada
        x = self.root.winfo_rootx() + self.root.winfo_width() // 2 - popup_width // 2
        y = self.root.winfo_rooty() + self.root.winfo_height() // 2 - popup_height // 2

        self.popup2.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        label = tk.Label(self.popup2, text='Nama')
        label.pack()

        self.entry_var2 = tk.StringVar()
        #validate_cmd = (self.popup2.register(self.validate_input2), '%P')
        self.entry2 = tk.Entry(self.popup2, textvariable=self.entry_var2)
        self.entry2.pack(pady=20)
        save_button = tk.Button(self.popup2, text="Save", command=self.save_input2)
        save_button.pack()
        xx,yy=0,200
        i = -1
        c = -1
        self.button = []

        for color in self.color_list:
            i += 1
            c += 1
            if c > 2:
                c=0
            if i > 2 and i <= 5:
                yy = 230
            elif i > 5 and i<=8:
                yy=260
            self.button.append(tk.Button(self.popup2, bg='white',text=color, width=5))
            self.button[i].place(x=c*60+10,y=yy)
            self.button[i].bind('<Button-1>',self.changeColor)

        self.popup2.grab_set()
        self.popup2.focus_set()

        self.root.bind('<Configure>',self.popupUpdate2)

        self.popup2.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close button

        self.popup2.wait_window()

    def changeColor(self,e):
        for i in self.button:
            i.config(bg='white')
        widget = e.widget
        self.currentColor = widget.cget('text')
        if self.currentColor == 'green':
            self.currentColor = 'light green'
        widget.config(bg='light gray')
        self.canvas.itemconfigure(self.node[self.count].widget,fill=self.currentColor)

    def popupUpdate2(self,e):
        popup_width = 200
        popup_height = 300
        x = self.root.winfo_rootx() + self.root.winfo_width() // 2 - popup_width // 2
        y = self.root.winfo_rooty() + self.root.winfo_height() // 2 - popup_height // 2
        self.popup2.geometry(f"+{x}+{y}")

    def scroll_start(self,e):
        self.canvas.scan_mark(e.x, e.y)
    def scroll_move(self,e):
        self.canvas.scan_dragto(e.x, e.y, gain=1)

    def releaseDrag(self,e):
        self.canvas.coords(self.tempLine,0,0,0,0)
    def drag(self,e):
        x = self.canvas.canvasx(e.x)
        y = self.canvas.canvasy(e.y)
        self.canvas.coords(self.tempLine, self.onFocus2.x, self.onFocus2.y,x,y)

    def reset(self,e):
        for master in self.node:
            self.canvas.itemconfigure(master.widget, outline='black', width=2)
            master.focused=False
        pathway_items = self.canvas.find_withtag('pathway')
        if pathway_items:
            self.canvas.delete(*pathway_items)
        self.onFocus=None
        self.beginNode = None
        self.endNode = None

    def wondering(self,e):
        self.root.bind('<Button-1>',self.wonderingEnd)
    def wonderingEnd(self,e):
        x = self.canvas.canvasx(e.x)
        y = self.canvas.canvasy(e.y)
        master = self.findItem(x,y)
        if master:
            if self.onFocus:
                if master!=self.onFocus:
                    if self.onFocus not in master.link or master not in self.onFocus.link:
                        self.create_popup(None)
                        if self.cancel:
                            return
                        self.root.bind('<Configure>', self.rootUpdate)
                        self.root.bind('<Configure>',self.resetRoot)
                    if self.onFocus not in master.link:
                        master.link.append(self.onFocus)
                        distance = self.currentInput if self.currentInput else 0
                        master.dist.append(distance)
                    if master not in self.onFocus.link:
                        cfont = font.Font(size=15)
                        self.lineList.append(self.canvas.create_line(self.onFocus.x, self.onFocus.y, master.x, master.y,width=3,fill='light gray'))
                        distance = self.currentInput if self.currentInput else 0
                        lineDistance = math.sqrt((master.x-self.onFocus.x)**2+(master.y-self.onFocus.y))

                        reduced_length = lineDistance / 2

                        # Find the new endpoint coordinates
                        new_endpoint_x = self.onFocus.x + (master.x - self.onFocus.x) / 2
                        new_endpoint_y = self.onFocus.y + (master.y - self.onFocus.y) / 2

                        self.canvas.create_text(new_endpoint_x, new_endpoint_y,text=self.currentInput,fill='black',font=cfont,tag='distCount')

                        self.onFocus.link.append(master)
                        self.onFocus.dist.append(distance)
        for master in self.node:
            self.canvas.tag_raise(master.widget)
            self.canvas.tag_raise("nama")
        self.root.bind('<space>', self.space)
    def findItem(self,x,y):
        tag = self.canvas.find_overlapping(x, y, x + 1, y + 1)
        if len(tag) > 0:
            tag = tag[0]
            master = None
            for i in self.node:
                if i.widget == tag:
                    master = i
                    return master
    def focusing(self,e):
        x = self.canvas.canvasx(e.x)
        y = self.canvas.canvasy(e.y)
        if self.create:
            master = self.findItem(x,y)
            if master:
                if master.focused:
                    self.canvas.itemconfigure(master.widget, outline='black', width=2)
                    master.focused=False
                    self.onFocus=None
                    return
                if self.onFocus is None:
                    self.canvas.itemconfigure(master.widget, outline='black',width=5)
                    master.focused=True
                    self.onFocus=master
                    self.onFocus2=master
        else:
            if self.beginNode is None:
                master = self.findItem(x, y)
                self.beginNode = master
                self.canvas.itemconfigure(master.widget,width=5,outline='red')
            elif self.beginNode is not None and self.endNode is None:
                master = self.findItem(x,y)
                self.endNode = master
                self.canvas.itemconfigure(master.widget,width=5,outline='red')


    def view(self,e):
        self.top = True
        while self.top:
            self.timing+=1
            self.root.update()
    def turnEye(self,e):
        self.timing = 0
        self.top = False

    def resetRoot(self,e):
        pass

    def space(self,e):
        if self.create:
            x = self.canvas.canvasx(e.x)
            y = self.canvas.canvasy(e.y)
            self.node.append(Node(self.canvas,x,y))
            self.count+=1
            self.create_popup2(None)
            self.root.bind('<Configure>', self.rootUpdate)
            self.node[self.count].nama = self.namaewa
            if self.currentColor == '':
                self.currentColor = 'white'
            if self.currentColor == 'green':
                self.currentColor = 'light green'
            self.canvas.itemconfigure(self.node[self.count].widget,fill=self.currentColor)
            self.root.bind('<Configure>', self.resetRoot)
            self.canvas.create_text(x,y,text=self.namaewa,tag='nama')
            self.canvas.tag_bind(self.node[self.count].widget, '<Button-1>', self.focusing)
            self.canvas.config(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('800x600+50+50')
    run = App(root)
    root.mainloop()
