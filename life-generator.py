# Title : Life Generator
# Author: Jun Kim
# Date: 2/14/2021
# Description: In this program, tkinter will be used to prompt a user to choose a csv file to retrieve data from.
# Then, the user will be prompted to choose which category to filter the data through, and the number of outputs desired
# then the highest rated toys will be written into a csv file in the same directory as the script.

import os                                                                       # used to create relative path to write file
import csv                                                                      # used to work with csv files
import tkinter as tk                                                            # used as a user friendly tool for the program
from tkinter import *
from tkinter import StringVar
from tkinter import ttk
import sys
import pandas as pd
import numpy as np


csv_data = pd.read_csv('amazon_co-ecommerce_sample.csv')
csv_df = pd.DataFrame(csv_data)

csv_df['amazon_category_and_sub_category'] = csv_df['amazon_category_and_sub_category'].str.split(' >').str[0]


input_given = False


if len(sys.argv) >= 2:

    input_csv_name = sys.argv[1]

    input_given = True


if input_given == False:

    window = tk.Tk()                                                            # creates a tkinter object
    window.geometry('500x500')                                                  # set size of tkinter window

    label = tk.Label(text='Toy Generator')                                      # sets the text to be dipslayed by tkinter
    label.pack()

    def category_opener():
        """ this function is used to get the category choice from the user"""

        global category_list
        global category_choice

        category_list = csv_df['amazon_category_and_sub_category'].unique()

        category_choice = StringVar(window)
        category_choice.set('Choose Category')                                  # default value shown when choosing campaign

        dropdown = OptionMenu(window, category_choice, *category_list)          # creates drop down in tkinter
        dropdown.pack()


        number_button = Button(window, text='Choose Number of Toys', command=number_opener).pack()

        return None

    def number_opener():
        """ this function is used to get the Number of Toys from the user"""

        global num_list
        global num_choice

        num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
         11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
         21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
         31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
         41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
         51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
         61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
         71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
         81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
         91, 92, 93, 94, 95, 96, 97, 98, 99, 100]

        num_choice = IntVar(window)
        num_choice.set('Choose Number')                                         # default value shown when choosing campaign

        dropdown = OptionMenu(window, num_choice, *num_list)                    # creates drop down in tkinter
        dropdown.pack()

        end_button = Button(window, text='Create Output', command=window.destroy).pack()

        return None


    category_button = Button(window, text='Choose Category', command=category_opener).pack()

    window.mainloop()

if input_given == True:

    global input_csv_df
    global category_choice
    global num_choice

    #input_csv_data = pd.read_csv(sys.argv[1])                                  # use this to run program by passing an argument

    input_csv_data = pd.read_csv('input.csv')

    input_csv_df = pd.DataFrame(input_csv_data)

    category_choice = input_csv_df['input_item_category'].iloc[0]
    num_choice = int(input_csv_df['input_number_to_generate'].iloc[0])


fieldnames_list = ['input_item_type','input_item_category','input_number_to_generate','output_item_name',
'output_item_rating','output_item_num_reviews',]                                # column names


with open("output.csv", 'w') as new_file:                                       # creates csv to write in

    if input_given == False:

        category_choice = category_choice.get()
        num_choice = num_choice.get()

    print(category_choice)

    csv_df = csv_df[csv_df.amazon_category_and_sub_category == category_choice]

    csv_df = csv_df.sort_values(by='uniq_id', ascending=True)
    csv_df = csv_df.sort_values(by='number_of_reviews', ascending=False)

    csv_df = csv_df.reset_index(drop=True)
    csv_df = csv_df[csv_df.index < (num_choice*10)]


    csv_df = csv_df.sort_values(by='uniq_id', ascending=True)
    csv_df = csv_df.sort_values(by='average_review_rating', ascending=False)

    csv_df = csv_df.reset_index(drop=True)
    csv_df = csv_df[csv_df.index < num_choice]

    csv_df.rename(columns={'product_name': 'output_item_name'}, inplace=True)
    csv_df.rename(columns={'average_review_rating': 'output_item_rating'}, inplace=True)
    csv_df.rename(columns={'number_of_reviews': 'output_item_num_reviews'}, inplace=True)
    csv_df.rename(columns={'uniq_id': 'input_item_type'}, inplace=True)
    csv_df.rename(columns={'amazon_category_and_sub_category': 'input_item_category'}, inplace=True)
    csv_df.rename(columns={'number_available_in_stock': 'input_number_to_generate'}, inplace=True)

    csv_df['input_item_type'] = 'toys'
    csv_df['input_number_to_generate'] = num_choice

    csv_df = csv_df[['input_item_type', 'input_item_category', 'input_number_to_generate',
             'output_item_name', 'output_item_rating','output_item_num_reviews']]

    print(csv_df)

    csv_df.to_csv(new_file, index=False)


root = tk.Tk()
root.title("Output Display")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (0.99 * w, 0.9 * h))


def displayontowindow():
    frame = Frame(root, width=600, height=310, bg="light grey")

    frame = ttk.Frame(root, width=300, height=250)

                                                                                # Canvas creation with double scrollbar
    hscrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
    vscrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
    sizegrip = ttk.Sizegrip(frame)
    canvas = tk.Canvas(frame, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set,
                            xscrollcommand=hscrollbar.set)
    vscrollbar.config(command=canvas.yview)
    hscrollbar.config(command=canvas.xview)

                                                                                # Add controls here
    subframe = ttk.Frame(canvas)

                                                                                # open file
    with open("output.csv", newline="") as file:
        reader = csv.reader(file)

                                                                                # r and c tell us where to grid the labels
        r = 0
        for col in reader:
            c = 0
            for row in col:
                                                                                # added some styling
                label = tk.Label(subframe, width=30, height=2,
                                      text=row, relief=tk.RIDGE)
                label.grid(row=r, column=c)
                c += 1
            r += 1

                                                                                # Packing everything
    subframe.pack(fill=tk.BOTH, expand=tk.TRUE)
    hscrollbar.pack(fill=tk.X, side=tk.BOTTOM, expand=tk.FALSE)
    vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
    sizegrip.pack(in_=hscrollbar, side=BOTTOM, anchor="se")
    canvas.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=tk.TRUE)
    frame.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)

    canvas.create_window(0, 0, window=subframe)
    root.update_idletasks()                                                     # update geometry
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.xview_moveto(0)
    canvas.yview_moveto(0)

displayontowindow()

root.mainloop()
