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
        self.root.title("MQTT frames converter")
     
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
        self.load_json_data("kinetics_model25.json")  # Replace with your JSON file path

    def load_json_data(self, json_file):
        formatted_json = ""
        raw_data = []
        try:
            # Load JSON data from the file
            with open(json_file, "r") as file:
                data = json.load(file)
                frames = []
                frames_to_file = []
                
                transposed = []
                
                #print(data["workitems"][0]["attributes"]["angle"]["value"])
            for workitem in data["workitems"]:
                fcount = 0
                angles = workitem["attributes"]["angle"]["value"]
                fangles = []
                #print(angles)
                for ang in angles:
                    fangles.append( int(round(ang)))
                    fcount = fcount + 1
                frames.append(fangles)

            #print(frames)    
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
    root.geometry("1600x1500")
    app = JSONViewerApp(root)
    root.mainloop()



