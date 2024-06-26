The purpose of this project is to allow users to sync highlights from a kindle e-reader, into a custom markdown template in Obsidian. Books not sourced from the kindle store are compatible.
![Project Photo](https://github.com/Azal-Amer/Kindle-To-Obsidian-Port/blob/main/Pasted%20image%2020240314230653.png?raw=true|250)
# Setup
To setup, install the packages listed in the python file, and modify the directories in both the shell and python to match your use-cases.
# Features
## Notification Updates
Using AppleScript, the shell can update you on the process without your needing to worry.
## Quick Updating

The script will automatically update your obsidian vault when run with new quotes, by keeping a copy of the last synced text. You can edit the markdown files and not worry about any damage to your files. As long as the filename is in the database, it will update.
## Renaming
For books not in the kindle store, there should be a convenient way to sync with a different name. 
![Photo of renaming Markdown. Containes a table with two columns to interface with the renaming system](https://github.com/Azal-Amer/Kindle-To-Obsidian-Port/blob/main/Pasted%20image%2020240314231038.png?raw=true)
The app will automatically correct any references made by the Kindle, to these titles. Simply make a table in the format above, and point the code toward it. 

# ToDo
- [ ] Make the script utilize a launch daemon to run on connection to the kindle
- [ ] Create a setup tool for easier installation
