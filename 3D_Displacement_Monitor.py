import pandas as pd
import numpy
import matplotlib.pyplot as plt
import tkinter as tk
from Conv import Conv
from tkinter import *
from tkinter import filedialog
global average_ttff
# Calculate the equivalent distance in E U coordinates of the baseline

def show_entry_fields():
    global average_ttff
    print("File name: \nRover Serial number: %s\nMask in millimeter: %s" % (e2.get(), e3.get()))
    dataframe = pd.read_csv(filename, skiprows=range(1, 2))  # read csv file as an argument and skip the first 2 readings
    data = dataframe[dataframe.StationID == int(e2.get())]

    timeToFix = data['timeToFix']
    time = data['Time']

    # take the mean of first 10 rows of lon, lat & alt as a baseline
    lat_sample = data['Latitude'].iloc[3:13].mean()
    lon_sample = data['Longitude'].iloc[3:13].mean()
    alt_sample = data['Height'].iloc[3:13].mean()
    sample = Conv(lat_sample, lon_sample)
    x_base, y_base = sample.converter()
    #x_base, y_base = converter(lat_sample, lon_sample)

    # Read the whole data lon, lat & alt of data variable (only rover SN 901)
    lat = data['Latitude']
    lon = data['Longitude']
    alt = data['Height']
    actual = Conv(lat, lon)
    x, y = actual.converter()

    #x, y = converter(lat, lon)

    # Calculate the shift in E, N & U coordinates
    E = x - x_base
    N = y - y_base
    U = (alt - alt_sample) / 10

    average_ttff = timeToFix.mean()  # calculate the average time to first fix
    print("Average time to first fix: %0.2f seconds" % average_ttff)

    # Plot displacement with spikes masked out.
    if e3.get():
        E_upper = numpy.ma.masked_where(E > int(e3.get()), E)
        E_lower = numpy.ma.masked_where(E_upper < (-1 * int(e3.get())), E_upper)
        E = E_lower

        N_upper = numpy.ma.masked_where(N > int(e3.get()), N)
        N_lower = numpy.ma.masked_where(N_upper < (-1 * int(e3.get())), N_upper)
        N = N_lower

        U_upper = numpy.ma.masked_where(U > int(e3.get()), U)
        U_lower = numpy.ma.masked_where(U_upper < (-1 * int(e3.get())), U_upper)
        U = U_lower

    else:
        ()

    # plot 4 figures in array 2 x 2
    format_float = "{:.2f}".format(average_ttff)
    var = StringVar()
    var.set(format_float)
    l6 = tk.Label(window, text="Average Time To First Fix in seconds:").grid(row=11, column=0)
    l6 = tk.Label(window, textvariable =var, fg='red').grid(row=11, column=1)  ###
    fig, axs = plt.subplots(2, 2, figsize=(17, 10))

    fig.suptitle("Rover serial number %d" % int(e2.get()), fontsize=20, color='green')
    axs[0, 0].plot(time, E)
    axs[0, 0].grid(True)
    axs[0, 0].set_title("East Displacement")
    axs[0, 0].set_ylabel('Displacement in mm')
    start, end = axs[0, 0].get_xlim()
    axs[0, 0].set_xticks(numpy.arange(start, end, 7))

    axs[1, 0].plot(time, N)
    axs[1, 0].set_title("North Displacement")
    axs[1, 0].sharex(axs[0, 0])
    axs[1, 0].set_ylabel('Displacement in mm')
    axs[1, 0].grid(True)

    start, end = axs[1, 0].get_xlim()
    axs[1, 0].set_xticks(numpy.arange(start, end, 7))
    axs[0, 1].plot(time, U)
    axs[0, 1].set_title("Up Displacement")
    axs[0, 1].set_ylabel('Displacement in mm')
    axs[0, 1].grid(True)
    start, end = axs[0, 1].get_xlim()
    axs[0, 1].set_xticks(numpy.arange(start, end, 7))

    axs[1, 1].plot(time, timeToFix)
    axs[1, 1].set_title("Time To First Fix")
    axs[1, 1].set_ylabel('Time in seconds')
    axs[1, 1].grid(True)
    start, end = axs[1, 1].get_xlim()
    axs[1, 1].set_xticks(numpy.arange(start, end, 7))

    fig.tight_layout()
    plt.show()

def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("CSV (Comma delimited)", "*.csv*"), ("all files","*.*")))
    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)
    if(filename):
            my_str.set(filename)
            open(filename,'r')

window = tk.Tk()
window.title("Rover Displacement Plot")
window.geometry("1000x400")
#window.configure(background='grey')
my_font1 = ('times', 18, 'bold')
my_font2 = ('times', 12)
l0 = tk.Label(window,text='Rover Displacement Plot',width=30,font=my_font1,fg='red').grid(row=1,column=1)
l1 = tk.Label(window,text='                        ',width=30,font=my_font1,fg='red').grid(row=2,column=1)
l2 = tk.Label(window, text="File name").grid(row=4, column=0)
l3 = tk.Label(window, text="                    Rover Serial Number").grid(row=6, column=0)
l4 = tk.Label(window, text="                         Mask value in millimeters\n             "
                           "                  (max displacement/clip level)").grid(row=7, column=0)
l5 = tk.Label(window,text='***  Mask value must be integer number in millimeters, leave it blank if not using masking  ***',width=80,fg='black').grid(row=9,column=1)

e2 = tk.Entry(window)
e3 = tk.Entry(window)

e2.grid(row=6, column=1)
e3.grid(row=7, column=1)

label_file_explorer = Label(window, text="File Explorer using Tkinter", width=100, height=4, fg="blue")
button_explore = Button(window, text="Upload File", command=browseFiles, font=my_font2)

button_explore.grid(row=4, column=1)

my_str = tk.StringVar()
l2=tk.Label(window,textvariable=my_str,fg='red').grid(row=5,column=1) # show name and path of the uploaded file
my_str.set("")

tk.Button(window, text='Plot', command=show_entry_fields, font=my_font2).grid(row=8, column=1, sticky=tk.W, pady=4)
tk.Button(window, text='Quit', command=window.quit, font=my_font2).grid(row=8, column=2, sticky=tk.W, pady=4)

#l6=tk.Label(window,textvariable=average_ttff,fg='red').grid(row=8,column=1) ###

tk.mainloop()
