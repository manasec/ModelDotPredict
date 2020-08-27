"""
 USAGE:
 python modeldotpredict.py --directory <path> --labels <label1> <label2> <labeln> --extensions <.jpg> <.png>
"""
import argparse
try:
    #Python2
    import Tkinter as tk   
except ImportError:
    # Python3
    import tkinter as tk 
import os
from shutil import copyfile, move
from PIL import ImageTk, Image

class Model:
    def __init__(self, parent, labels, allpaths):
        self.parent = parent

        frame = tk.Frame(parent)
        frame.grid()

        self.index = 0
        self.allpaths = allpaths
        self.labels = labels
        self.labelcount = len(labels)
        self.totalpaths = len(allpaths)

        self.image_raw = None
        self.image = None
        self.image_panel = tk.Label(frame)

        self.set_img(allpaths[self.index])

        self.buttons = []
        for label in labels:
            self.buttons.append(
                    tk.Button(frame, text=label, width=10, height=1, command=lambda l=label: self.poll(l))
            )

        for key in range(self.labelcount):
            parent.bind(str(key+1), self.pollfromkey)

        progress_string = "%d/%d"%(self.index, self.totalpaths)
        self.progress_label = tk.Label(frame, text=progress_string, width=10)

     
        for col, button in enumerate(self.buttons):
            button.grid(row=0, column=col, sticky='we')

 
        self.progress_label.grid(row=0, column=self.labelcount, sticky='we')

        self.image_panel.grid(row=1, column=0, columnspan=self.labelcount+1, sticky='we')

        

    def next_img(self):
     
        self.index += 1
        progress_string = "%d/%d"%(self.index, self.totalpaths)
        self.progress_label.configure(text=progress_string)

        if self.index < self.totalpaths:
            self.set_img(self.allpaths[self.index])
        else:
            self.parent.quit()

    def set_img(self, path):
       
        image = self._load_img(path)
        self.image_raw = image
        self.image = ImageTk.PhotoImage(image)
        self.image_panel.configure(image=self.image)

    def poll(self, label):
       
        input_path = self.allpaths[self.index]
        self._copy_img(input_path, label)
        self.next_img()

    def pollfromkey(self, event):
       
        pressed_key = int(event.char)
        label = self.labels[pressed_key-1]
        self.poll(label)

    @staticmethod
    def _load_img(path, size=(800,600)):
    
        image = Image.open(path)
        image = image.resize(size, Image.ANTIALIAS)
        return image

    @staticmethod
    def _copy_img(input_path, label):
     
        root, file_name = os.path.split(input_path)
        output_path = os.path.join(root, label, file_name)
        print( "%s ------> %s"%(file_name, label))
        copyfile(input_path, output_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='directory where the mess is!', required=True)
    parser.add_argument('-l', '--labels', nargs='+', help='the labels/classes , space seperated', required=True)
    parser.add_argument('-e', '--extensions', nargs='+', help='image file extensions (jpg,png,tiff,etc)')

    args = parser.parse_args()

    directory = args.directory
    labels = args.labels
    extensions = args.extensions
    if extensions==None:
        extensions=['jpg','png']
    if not extensions[0].startswith('.'):
        extensions = ["."+e for e in extensions]

    for label in labels:
        if not os.path.exists(os.path.join(directory, label)):
            os.makedirs(os.path.join(directory, label))

    allpaths = []
    for file in os.listdir(directory):
        for e in extensions:
            if file.endswith(e):
                path = os.path.join(directory, file)
                allpaths.append(path)

    root = tk.Tk()
    app = Model(root, labels, allpaths)
    root.mainloop()
