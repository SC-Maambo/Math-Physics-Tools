def main():
    import tkinter as tk
    from math import sqrt
    app = tk.Tk()
    app.configure(bg="steelblue")

    #Clear row function to remove widgets from a specific row
    def clear_row(parent_widget, row_index):
        """Destroys all widgets in a specific grid row within a parent widget."""
        for widget in parent_widget.winfo_children():
            if isinstance(widget, tk.Widget) and widget.grid_info().get("row") == row_index:
                widget.destroy()
                
    a_input = tk.Entry(app)
    b_input = tk.Entry(app)
    c_input = tk.Entry(app)

    tk.Label(app, text="Enter the value of A: ",bg='steelblue').grid(row=0)
    a_input.grid(row=0 ,column=1)

    tk.Label(app, text="Enter the value of B: ",bg='steelblue').grid(row=1)
    b_input.grid(row=1, column=1)

    tk.Label(app, text="Enter the value of C: ",bg='steelblue').grid(row=2)
    c_input.grid(row=2, column=1)
    status_var = tk.StringVar()
    def calculate():
        try:
            clear_row(app, 7)
            
        
            
            a = float(a_input.get())
            b = float(b_input.get())
            c = float(c_input.get())
            
            delta = (b * b) - (4 * a * c)
            if delta > 0:
                status_var.set("Two real roots")
                tk.Label(app, textvariable=status_var, font=("Arial", 10),bg= 'steelblue').grid(row=5)
                root1 = (-b + sqrt(delta)) / (2 * a)
                root2 = (-b - sqrt(delta)) / (2 * a)
                answer = str("The first answer is: "+ str(root1) + "\nThe second answer is: "+ str(root2))
                
                tk.Label(app, text= answer,bg='steelblue').grid(row=7)
                
            elif delta < 0:
                status_var.set("No real roots")
                tk.Label(app, textvariable=status_var, font=("Arial", 10),bg='steelblue').grid(row=5)
            else:
                status_var.set("One real roots")
                tk.Label(app, textvariable=status_var, font=("Arial", 10),bg='steelblue').grid(row=5)
                root1 = (-b - sqrt(delta)) / (2 * a)
                answer = str("The answer is: " +str(root1))
                
                tk.Label(app, text= answer,bg='steelblue').grid(row=7)
        except ValueError:
            clear_row(app, 5)
            clear_row(app, 7)
            status_var.set("Please enter valid numbers")
            tk.Label(app, textvariable=status_var, font=("Arial", 10),bg='steelblue').grid(row=5)
    tk.Button(app, text="Calulate", width= 25, command= calculate).grid(row=4, pady=10)    
    tk.Label(app, text= "ax² + bx + c = 0", font= ('arial', 20),bg='steelblue',fg="white").grid(row=3, columnspan=3, pady=10)
    tk.mainloop()
main()
