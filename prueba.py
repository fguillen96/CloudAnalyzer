import tkinter
import tkinter.messagebox
import traceback


class Foo():
    def __init__(self):
        # Initialize a new GUI window
        tkinter.Tk.report_callback_exception = callback_error  # TkInter callbacks run in different threads, so if we want to handle generic exceptions caused in a TkInter callback, we must define a specific custom exception handler for that
        root = tkinter.Tk()

        # The error() function is triggered when the following is uncommented
        #number = 1 / 0

        # Define a button and draw it
        button = tkinter.Button(root, text='Generate an error', command=self.generate_error)
        button.pack()

        # Loop forever
        root.mainloop()

    def generate_error(self):
        # The "callback_error()" function is triggered when the button is clicked
        number = 1 / 0


def error(message, exception):
    # Build the error message
    if exception is not None:
        message += '\n\n'
        message += traceback.format_exc()

    # Also log the error to a file
    # TODO

    # Show the error to the user
    tkinter.messagebox.showerror('Error', message)

    # Exit the program immediately
    exit()


def callback_error(self, *args):
    # Build the error message
    message = 'Generic error:\n\n'
    message += traceback.format_exc()

    # Also log the error to a file
    # TODO

    # Show the error to the user
    tkinter.messagebox.showerror('Error', message)

    # Exit the program immediately
    exit()



if __name__ == '__main__':
    try:
        # Run the Foo class
        Foo()

    except Exception as e:
        error('Generic error:', e)