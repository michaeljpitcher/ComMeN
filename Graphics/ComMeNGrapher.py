import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import csv


class Grapher(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "ComMeN grapher")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in [StartPage]:
            frame = F(container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent):
        self.comp_data = {}
        self.time_data = []
        self.node_vars = {}

        tk.Frame.__init__(self, parent)

        tk.Label(self, text="Data file:").grid(row=0, column=0)

        filename = tk.Entry(self)
        filename.grid(row=0, column=1)
        filename.insert(0, 'Experiments/0/0.csv')

        data_button = ttk.Button(self, text="Load data", command=lambda: self.load_data(filename.get()))
        data_button.grid(row=0, column=2)

        self.data_message = tk.StringVar()
        tk.Label(self, textvariable=self.data_message).grid(row=1, column=1)
        self.data_message.set("")

        f = Figure(figsize=(5, 5), dpi=100)
        self.subplot = f.add_subplot(111)
        self.compartment_variable = tk.StringVar(self)

        self.canvas = FigureCanvasTkAgg(f, self)
        # self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas.get_tk_widget().grid(row=2, rowspan=20, columnspan=3)
        self.canvas.show()

        self.compartment_menu = tk.OptionMenu(self, self.compartment_variable, "")
        self.compartment_menu.config(width=20)
        self.compartment_menu.grid(row=23, column=1)

        plot_button = ttk.Button(self, text="Plot", command=lambda: self.update_graph())
        plot_button.grid(row=24, column=1)

        self.pack()

    def load_data(self, filename):
        try:
            csv_file = open(filename, 'r')
            self.data_message.set("Data loaded")
        except IOError:
            self.data_message.set("File {0} not found".format(filename))
            return
        self.subplot.clear()
        self.canvas.show()
        self.comp_data = {}
        self.time_data = []
        csv_reader = csv.DictReader(csv_file)
        compartments = sorted(list(csv_reader.fieldnames))
        compartments.remove('node_id')
        compartments.remove('timestep')

        self.compartment_menu['menu'].delete(0, 'end')
        for choice in compartments:
            self.compartment_menu['menu'].add_command(label=choice, command=tk._setit(self.compartment_variable, choice))

        for c in compartments:
            self.comp_data[c] = {}

        current_time = -1.0
        for row in csv_reader:
            if float(row['timestep']) != current_time:
                self.time_data.append(float(row['timestep']))
                current_time = float(row['timestep'])
            for c in compartments:
                node_data = self.comp_data[c]
                if row['node_id'] not in node_data:
                    node_data[row['node_id']] = []
                node_data[row['node_id']].append(row[c])

        self.pack()

        nodes = self.comp_data.values()[0].keys()
        row = 2
        for n in nodes:
            self.node_vars[n] = tk.IntVar()
            tk.Checkbutton(self, text=n, variable=self.node_vars[n]).grid(row=row, column=3)
            row += 1

    def update_graph(self,):
        self.data_message.set("")
        self.subplot.clear()
        compartment_chosen_data = self.comp_data[self.compartment_variable.get()]
        nodes = [n for n in self.node_vars if self.node_vars[n].get() == 1]

        if not nodes:
            nodes = self.node_vars.keys()

        for key in nodes:
            self.subplot.plot(self.time_data, compartment_chosen_data[key], label=key)
        self.canvas.show()


def run_grapher():
    app = Grapher()
    app.mainloop()
