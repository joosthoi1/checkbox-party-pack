# checkbox-party-pack  
launcher for my games  
images are 290*300    
  
If you would like to add your own game thats possible, first you need to add a mainframe on a row a column   
Now you have to assign an image label to a mainframe index, the index of the mainframe is its place in self.framelist  
generaly this will be the same index it was when created.
you can supply your own title and image.
Now go down to the load and config function and add your program to the functions.  
  
  
#### You might need to put gridcreation.py in each game folder seperatly, or put it in you python's lib folder

If you want to play this, type next in the command line:
```
python -m venv venv
source venv/Scripts/activate     // this is if you have Windows
source venv/bin/activate     // this is if you have UNIX like systems
pip install -r requirements.txt
py checkbox\ party\ pack.py
```
Notice you have to have above python 3.6
