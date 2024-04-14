import tkinter as tk
from tkinter import ttk
import json
from tkinter import filedialog
from tkinter import messagebox


class FRAMEData():
    def __init__(self, id, angles):
        self.id = id
        self.angles = angles
        
class JSONViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT frames converter")
        self.robots = tk.IntVar(value=0)
        self.frames_count = tk.IntVar(value=0)
        # Create a Frame for displaying JSON data
        self.frame = ttk.Frame(root)
        self.frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True,side=tk.LEFT)
        self.left_frame = ttk.LabelFrame(root,text="Настройки конвертера")
        self.left_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True,side=tk.RIGHT)

        self.robot_label = ttk.Label(self.left_frame, text="Количество роботов" )
        self.robot_label.pack(pady=10)
        self.robot_entry = ttk.Entry(self.left_frame,textvariable=self.robots)
        self.robot_entry.pack()
        self.frames_label = ttk.Label(self.left_frame, text="Количество кадров" )
        self.frames_label.pack(pady=10)
        self.frames_entry = ttk.Entry(self.left_frame,textvariable=self.frames_count)
        self.frames_entry.pack()
        self.open_button = ttk.Button(self.left_frame, text="Открыть файл", command=self.open_file)
        self.open_button.pack(padx=20, pady=20)
        # Create a Text widget for displaying JSON content
        self.text_widget = tk.Text(self.frame, wrap=tk.WORD)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create a Scrollbar for the Text widget
        self.scrollbar = ttk.Scrollbar(self.frame, command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        # Load and display JSON data
        #self.load_json_data("kinetics_model25.json")  # Replace with your JSON file path

    def open_file(self):
        fin = filedialog.askopenfile(mode='r',title='Select a File')
        if fin is not None:
            self.load_json_data(fin.name)
            
        fin.close()
    
    def load_json_data(self, json_file):
        formatted_json = ""
        raw_data = []
        try:
            # Load JSON data from the file
            with open(json_file, "r") as file:
                data = json.load(file)
                frames = []
                frames_to_file = []
                r3 = self.robots.get() * 3
                transposed = []
                r3 = r3 -1
                #print(data["workitems"][0]["attributes"]["angle"]["value"])
            for workitem in data["workitems"]:
                fcount = 0
                index = workitem["index"] 
                if self.robots.get() != 0:
                    if index == r3: break
                angles = workitem["attributes"]["angle"]["value"]
                fangles = []
                #print(angles)
                
                for ang in angles:
                    fangles.append( int(round(ang)))
                    fcount = fcount + 1
                frames.append(fangles)

                

            #print(frames)
            if self.frames_count.get() > 0:
                fcount = self.frames_count.get()

            for i in range(fcount):
                # the following 3 lines implement the nested listcomp
                transposed_row = []
                for row in frames:
                    transposed_row.append(row[i])
                transposed.append(transposed_row)


                #raw_data[frame].angles = angles
                #raw_data[frame].frame  = frame
                #raw_data.append({"frame": frame,"angles": fangles})
                #for frame in frames
            index = 0
            for fang in transposed:
                self.text_widget.insert(tk.END, {"type":"frame","frame": index,"angles": fang } )
                self.text_widget.insert(tk.END,"\n")
                #frames_to_file.append({"type":"frame","frame": index,"angles": fang })
                raw_data.append({"type":"frame","frame": index,"angles": fang})
                index = index + 1
            # Format JSON data as a string and display it in the Text widget
            formatted_json = json.dumps(raw_data, indent=4)
            #print("data ", raw_data)
            #self.text_widget.insert(tk.END, formatted_json)

            # Make the Text widget read-only
            self.text_widget.config(state=tk.DISABLED)

        except FileNotFoundError:
            self.text_widget.insert(tk.END, "File not found.")
            self.text_widget.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1600x980")
    app = JSONViewerApp(root)
    root.mainloop()



