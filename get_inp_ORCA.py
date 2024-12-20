from tkinter import *
from tkinter import filedialog
import os  # Added import for os module

# Function to load configuration (.in) files
def loadfile1():
    global configFiles
    configFiles = filedialog.askopenfilenames(filetypes=(('IN files', '*.in'), ('All files', '*.*')))
    textBox.insert(END, '\n'.join(configFiles))
    textBox.insert(END, '\n')

# Function to load XYZ file
def loadfile2():
    global xyzFiles
    xyzFiles = filedialog.askopenfilenames(filetypes=(('XYZ files', '*.xyz'), ('All files', '*.*')))
    textBox.insert(END, '\n'.join(xyzFiles))
    textBox.insert(END, '\n')

# Function to generate ORCA input files
def genFiles():
    """
    Generates ORCA input files by combining XYZ coordinates and configuration settings.
    The XYZ coordinates have a '*' added on a new line after all coordinates as required by ORCA.
    """
    try:
        ix = 1  # XYZ file index
        for xyzFile in xyzFiles:
            with open(xyzFile) as source2:
                imol = 1  # Molecule index

                while True:
                    try:
                        atomCount = int(source2.readline().strip())  # Read the number of atoms
                    except ValueError:
                        break  # End of file or invalid format

                    mol = ''
                    source2.readline()  # Skip comment line

                    # Collect all atomic coordinates
                    for _ in range(atomCount):
                        line = source2.readline().strip()
                        mol += line + '\n'

                    mol += '*\n'  # Add the * on a new line after all coordinates

                    # Loop through each configuration file and generate inputs
                    for cf in configFiles:
                        config_name = os.path.splitext(os.path.basename(cf))[0]

                        with open(cf) as source1, open(f'{config_name}_molecule_{ix}_conformer_{imol}.in', 'w') as destination:
                            # Write header
                            destination.write(f'# Molecule {ix}; Conformer number {imol} ({config_name})\n')

                            # Process and replace %base
                            for line in source1:
                                if line.strip().startswith('%base'):
                                    destination.write(f'%base "{config_name}_{ix}_{imol}"\n')
                                else:
                                    destination.write(line)

                            # Append molecular coordinates
                            destination.write(mol)

                    imol += 1  # Increment molecule index

            ix += 1  # Increment XYZ file index

    except Exception as e:
        textBox.insert(END, f'Error: {e}\n')

# Function to close the application
def quit():
    window.destroy()

# Function to print loaded file paths to the console
def printFilesList():
    print('\n'.join(configFiles))
    print('\n'.join(xyzFiles))

# Create the main application window
window = Tk()
window.title('ORCA Input File Generator')
window.resizable(False, False)

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
