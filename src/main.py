import tkinter as tk
from tkinter import ttk
import json
ROBOTS = 6

class FRAMEData():
    def __init__(self, id, angles):
        self.id = id
        self.angles = angles
        
class JSONViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT frames player")
     
        # Create a Frame for displaying JSON data
        self.frame = ttk.Frame(root)
        self.frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Create a Text widget for displaying JSON content
        self.text_widget = tk.Text(self.frame, wrap=tk.WORD)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a Scrollbar for the Text widget
        self.scrollbar = ttk.Scrollbar(self.frame, command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        # Load and display JSON data
        self.load_json_data("kinetics_model.json")  # Replace with your JSON file path

    def load_json_data(self, json_file):
        formatted_json = ""
        raw_data = []
        try:
            # Load JSON data from the file
            with open(json_file, "r") as file:
                data = json.load(file)
                #print(data["workitems"][0]["attributes"]["angle"]["value"])
            for workitem in data["workitems"]:
                frame = workitem["index"]
                angles = workitem["attributes"]["angle"]["value"]
                #print(angles)
                fangles = []
                for i in range(ROBOTS * 3):
                    fangles.append(angles[i])             
                #raw_data[frame].angles = angles
                #raw_data[frame].frame  = frame
                raw_data.append({"frame": frame,
                           "angles": fangles})
            # Format JSON data as a string and display it in the Text widget
            formatted_json = json.dumps(raw_data, indent=4)
            #print("data ", raw_data)
            self.text_widget.insert(tk.END, formatted_json)

            # Make the Text widget read-only
            self.text_widget.config(state=tk.DISABLED)

        except FileNotFoundError:
            self.text_widget.insert(tk.END, "File not found.")
            self.text_widget.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1600x1500")
    app = JSONViewerApp(root)
    root.mainloop()



