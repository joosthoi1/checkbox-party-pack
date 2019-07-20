# checkbox-party-pack  
launcher for my games  
images are 290*300    

If you would like to add your own game that's possible, simply add a mainframe with x and y arguments.  
Then, add an imagelabel, you need to add an index, that index is the index where the mainframe is in the list.  
If you created your game (called the mainframe function) as the second one, the index will be 1 (index starts at 0)  
Note, you put the imagelabel right under the mainframe call and do it with an index of -1 so it will bind to the previously loaded one:  
```py
self.mainframe(2,1)
self.imagelabel(-1, "Beautiful title", "game/image.png")
```
you can supply your own title and image.  
Now go down to the load and config function and add your program to the functions.  
Usually this will be something like this:
```py
if name == 'App name':
    self.root.destroy()
    ImportName.board()
    main()
```
And:
```py
if name == 'App name':
    ImportName.config()
```
note: Make sure to import your application.
note: name is the name you gave your app in imagelabel

#### You might need to put gridcreation.py in each game folder separately, or put it in you python's lib folder (usually this isn't necessary)

If you want to play this, type next in the command line:
```
python -m venv venv
source venv/Scripts/activate     // this is if you have Windows
source venv/bin/activate     // this is if you have UNIX like systems
pip install -r requirements.txt
py checkbox\ party\ pack.py
```
Notice you have to have above python 3.6
