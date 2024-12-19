# Import required modules from tkinter
from tkinter import *  # Import all classes and functions from tkinter
from tkinter import filedialog  # For file selection dialogs
import os  # For extracting file names

# Function to load configuration (.in) files
def loadfile1():
    """
    Opens a file dialog to select multiple .in files (settings files).
    The selected files are stored in the global variable 'configFiles'.
    The file paths are displayed in the text box.
    """
    global configFiles  # Make configFiles accessible globally
    configFiles = filedialog.askopenfilenames(filetypes=(("IN files", "*.in"), ('All files', '*.*')))
    textBox.insert(END, '\n'.join(configFiles))  # Display file paths in the text box
    textBox.insert(END, '\n')

# Function to load XYZ file
def loadfile2():
    """
    Opens a file dialog to select an XYZ file (molecular structure file).
    The selected file path is stored in the global variable 'xyzFile'.
    The file path is displayed in the text box.
    """
    global xyzFile  # Make xyzFile accessible globally
    xyzFile = filedialog.askopenfilenames(filetypes=(("XYZ files", "*.xyz"), ('All files', '*.*')))
    textBox.insert(END, '\n'.join(xyzFile))  # Display file paths in the text box
    textBox.insert(END, '\n')

# Function to generate output files based on loaded configuration and XYZ files
def genFiles():
    """
    Generates new input files by combining the selected XYZ file (molecular coordinates)
    with settings files (.in).
    
    Steps:
    1. Reads the atomic coordinates from the XYZ file.
    2. Combines the atomic data with content from each settings file.
    3. Writes new input files named in the format 'diMe_Box_H_<config_name>_<molecule_index>.in'.
    
    Notes:
    - XYZ file format: 
        Line 1: Number of atoms
        Line 2: Comment
        Remaining lines: Atomic coordinates (element, x, y, z)
    - Assumes specific structure for configuration (.in) files.
    """
    # Open the XYZ file and start processing
    with open(xyzFile[0]) as source2:
        imol = 1  # Molecule index
        while True:
            try:
                atomCount = int(source2.readline().strip())  # Read the number of atoms
            except:
                return  # End of file or invalid format
            
            mol = ''  # Initialize molecule data
            source2.readline()  # Skip comment line in XYZ file
            for l in range(atomCount):
                mol += source2.readline()  # Read atomic coordinates

            # Loop through each configuration (.in) file
            for cf in configFiles:
                # Extract the base name of the configuration file (without path and extension)
                config_name = os.path.splitext(os.path.basename(cf))[0]
                
                # Open the configuration file and create output files
                with open(cf) as source1, open(f'12_{config_name}_{imol}.in', 'w') as destination:
                    # Write checkpoint file header
                    destination.write(f'%chk=12_{config_name}_{imol}.chk\n')
                    
                    source1.readline()  # Skip the first line in the .in file
                    # Copy the next 7 lines (assumed header content)
                    for j in range(7):
                        destination.write(source1.readline())
                    
                    # Write molecular coordinates
                    destination.write(mol + '\n')
            imol += 1  # Increment molecule index

# Function to close the application
def quit():
    """
    Closes the application window.
    """
    window.destroy()

# Function to print loaded file paths to the console
def printFilesList():
    """
    Prints the loaded configuration (.in) files and XYZ file paths to the console.
    """
    print('\n'.join(configFiles))
    print('\n'.join(xyzFile))

# Create the main application window
window = Tk()
window.title('Concatenation of .XYZ and .in Files')
window.resizable(False, False)  # Disable window resizing

# Create the top panel for buttons and labels
panel = Frame(window, height=75, bg='lightblue')
panel.pack(side='top', fill='x')

# Create the text display area
textFrame = Frame(window, width=600, height=340)
textFrame.pack(side='bottom', fill='both')
textBox = Text(textFrame, font=('Helvetica', '12'), wrap='word', bg='lightblue')
textBox.pack(side='left', fill='both')

# Add a scrollbar to the text display area
scroll = Scrollbar(textFrame)
scroll.pack(side='right', fill='y')
scroll['command'] = textBox.yview
textBox['yscrollcommand'] = scroll.set

# Add labels and buttons to the top panel
l1 = Label(panel, text='1. Load ALL the settings files -->', bg='lightblue')
l1.place(x=10, y=10)
lBtn1 = Button(panel, text='Load', command=loadfile1)
lBtn1.place(x=180, y=10)

l2 = Label(panel, text='2. Load the .XYZ file -->', bg='lightblue')
l2.place(x=10, y=40)
lBtn2 = Button(panel, text='Load', command=loadfile2)
lBtn2.place(x=180, y=40)

save = Button(panel, text='Generate output files', command=genFiles)
save.place(x=230, y=10, height=55)

btnQuit = Button(panel, text='Quit', command=quit)
btnQuit.place(x=700, y=10, width=40, height=55)

# Start the main event loop
window.mainloop()
