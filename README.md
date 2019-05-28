# checkbox-party-pack  
launcher for my games  
images are 290*300  

modules are game specific but it's recommended you at least have keyboard.  
  
If you would like to add your own game thats possible, first you need to add a mainframe on a row a column   
Now you have to assign an image label to a mainframe index, the index of the mainframe is its place in self.framelist  
generaly this will be the same index it was when created.
you can supply your own title and image.
Now go down to the load and config function and add your program to the functions.  
  
Make sure you use tk.Toplevel() and not tk.Tk() to avoid issues with things like variables in the buttons etc.  
  
#### You might need to put gridcreation.py in each game folder seperatly, or put it in you python's lib folder
