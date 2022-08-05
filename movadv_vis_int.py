# GUI for Movie-Advise 

# Tk module
from tkinter import *
from tkinter import  ttk 
# Import back-end file
from movieadvise import get_movie_advise


#Flags that indicate if required information is filled or not
search_limit_flag = 0
chechbuttons_flag = 0

# Prime Parrent aka Main Window
main_window = Tk()
main_window.title("Movie Adviser by Python-Volod")
main_window.resizable(False, False)

#Entry field for movie name 
mov_name_widget = ttk.Frame(main_window)
search_name = StringVar()
text_mov_name = ttk.Label(mov_name_widget, text = "Name of movie or series")
mov_name_ent = ttk.Entry(mov_name_widget,textvariable= search_name , width = 30, )
# Geometry inside mov_name_widget 
text_mov_name.grid(column= 0, pady = 4, row= 0)
mov_name_ent.grid(column=0, row =1)


#Entry field for search limit
search_limit_widget = ttk.Frame(main_window)
# #Checks if search_limit is an integer value
def is_integer(inp , is_negative = 1):
    try:
        inp = int(inp)
        global search_limit_flag
        search_limit_flag = 1
        return True
    except:
        if is_negative == 0 or is_negative == "0":
            return True
        else:
            return False
# Adds is_integer as validation function 
reg = main_window.register(is_integer)
search_limit = IntVar(main_window, value = 1)
search_limit_ent = ttk.Entry(search_limit_widget, textvariable= search_limit, width = 10 ,validate = "all", validatecommand= (reg , "%P",  "%d"))
text_search_limit = ttk.Label(search_limit_widget, text = "Search limit")
search_limit_ent.grid(column=0, row = 1)
text_search_limit.grid(column =0, pady = 5, row = 0)


# Checkboxes for type of results 
checkboxes_widget = ttk.Frame(main_window)
movie_type = StringVar()
series_type = StringVar()
#Set's search type flag to on 
def search_type_flag():
    global chechbuttons_flag
    chechbuttons_flag = 1
    print(chechbuttons_flag)

movie_type_check = ttk.Checkbutton(checkboxes_widget, variable = movie_type, text= "Movies", command= search_type_flag)
series_type_check = ttk.Checkbutton(checkboxes_widget, variable = series_type , text = "Series", command = search_type_flag)
movie_type_check.grid(column = 0, pady= 5, row= 0, sticky="W")
series_type_check.grid(column = 0, pady = 5, row = 1, sticky="W")


# Text with current state of operations and gif
text_im_widged = ttk.Frame(main_window)
text_state = ttk.Label(text_im_widged ,text="Fill in all fields with appropriate information and press search" , borderwidth= 3 , relief = "ridge")
text_state.grid(column = 0, row =0 , sticky = "N")

#Destroys user-input widgets when used
def destroy_initial_page():
    text_im_widged.destroy()
    mov_name_widget.destroy()
    search_limit_widget.destroy()
    checkboxes_widget.destroy()
    execute_button.destroy()



# Dictionary with information needed for tag's /* To change font depending on genre */

tag_info_dict = {}

# Execute button and function, performes search based on input values /* Python_B name is a tribute to my friend */ 
def Python_B():
    if search_limit_flag == 1 and chechbuttons_flag == 1:
        execute_button["state"] = "disabled"
        # Creates a list of movie suggestions and stores them in result, then formes one string object with text
        result = get_movie_advise(search_name.get(), search_limit.get(), (movie_type.get(), series_type.get()))
        result_text = ""
        # Is used as key for tag_info_dict
        answer_count = 0
        for tape in result:
            tag_info_dict[answer_count] = (len(tape.get_text()), tape.get_genre().split(",")[0])
            result_text += tape.get_text()
            answer_count += 1
        # Creates Frame to hold text widget and a scrollbar
        stage_answer_widget = Frame(main_window)
        #Creates response text widget,scrollbar and configures tags
        scrollbar_response = Scrollbar(stage_answer_widget)
        response_text_widget = Text(stage_answer_widget, height= 200, width= 250 ,  yscrollcommand= scrollbar_response.set)
        response_text_widget.insert(END , result_text)
        scrollbar_response.config(command= response_text_widget.yview)
        #destroys previous widgets and set's everything on the screen
        main_window.resizable(True, True)
        scrollbar_response.pack(side = RIGHT, fill=Y)
        response_text_widget.pack()
        destroy_initial_page()
        stage_answer_widget.pack()
    else:
        text_state["text"] = "Nessesary information is not yet fielded"
execute_button = ttk.Button(text= "Execute" , state="active" , command = Python_B)





# Geometry 
text_im_widged.grid(column= 0, row = 0, sticky = "N")
mov_name_widget.grid(column =0 , row = 1, sticky = "W")
search_limit_widget.grid(column = 1 , row = 1, sticky= "E")
checkboxes_widget.grid(column = 0, row = 3, sticky= "SW")
execute_button.grid(column = 1 , row = 3 , sticky = "SE")



# Makes application interactive
main_window.mainloop()
