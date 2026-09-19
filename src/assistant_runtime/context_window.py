from . import AI



def context_window():

    if AI.reset_triggered == True:
        with open("chatcontext.txt", "r") as file:
            text = file.read()

        text 


        with open("chatcontext.txt", "w") as file:
            pass
        