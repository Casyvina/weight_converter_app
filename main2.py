import customtkinter as ctk
from settings import *
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class App(ctk.CTk):
    def __init__(self):
        # window setup
        super().__init__(fg_color = GREEN)
        self.title('')
        self.iconbitmap('')
        self.geometry('400x400')
        self.resizable(False, False)
        self.change_title_bar_color() 
        
        # layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1,2,3), weight=1, uniform='a')
        
        # data
        self.metric_bool = ctk.BooleanVar(value = True)
        self.height_int = ctk.IntVar(value=170)
        self.weight_float = ctk.DoubleVar(value=65)
        self.bmi_string = ctk.StringVar()
        self.update_bmi()
        
        # tracing
        self.height_int.trace_add('write', self.update_bmi)
        self.weight_float.trace_add('write', self.update_bmi)
        self.metric_bool.trace_add('write', self.change_units)
               
        
        # widgets
        ResultText(self, self.bmi_string)
        self.weight_input = WeightInput(self, self.weight_float, self.metric_bool)
        self.height_input = HeightInput(self, self.height_int, self.metric_bool)
        UnitSwitcher(self, self.metric_bool)
        
        # Run app
        self.mainloop()     

    def change_title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTIBUTE = 35
            COLOR = TITLE_HEX_COLOR
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass
           
    def update_bmi(self, *args):
        height_meter = self.height_int.get() / 100
        weight_kg = self.weight_float.get()
        bmi_result = round(weight_kg / height_meter ** 2, 2)
        self.bmi_string.set(bmi_result)
    
    def change_units(self, *args):
        self.height_input.update_text(self.height_int.get())
        self.weight_input.update_weight()  
    
class ResultText(ctk.CTkLabel):
    def __init__(self, parent, bmi_string):
        font = ctk.CTkFont(family= FONT, size=MAIN_TEXT_SIZE, weight="bold",)
        super().__init__(master=parent, text=22.5, font=font, text_color=WHITE, textvariable = bmi_string)
        self.grid(column=0, row=0, rowspan=2, sticky = 'nsew')
  
class WeightInput(ctk.CTkFrame):
    def __init__(self, parent, weight_float, metric_bool):
        super().__init__(master = parent, fg_color = WHITE)
        self.grid(column=0, row=2, sticky='nsew', padx=10, pady=10)
        self.weight_float = weight_float  
        self.metric_bool = metric_bool
        
        # output logic
        self.output_string = ctk.StringVar()
        self.update_weight()
        
        # layout
        self.rowconfigure(0, weight=1, uniform='b')
        self.columnconfigure(0, weight=2, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        self.columnconfigure(2, weight=3, uniform='b')
        self.columnconfigure(3, weight=1, uniform='b')
        self.columnconfigure(4, weight=2, uniform='b')
        
        # widgets
        font = ctk.CTkFont(family=FONT, size= INPUT_FONT_SIZE)
        label = ctk.CTkLabel(self, text= '70kg', textvariable= self.output_string, text_color= BLACK, font=font)
        label.grid(row=0, column=2)
        
        # buttons
        minus_button = ctk.CTkButton(self, command= lambda: self.update_weight(('minus', 'large')), text='-', font= font, text_color = BLACK, fg_color = LIGHT_GRAY)
        minus_button.grid(row=0, column=0, sticky='ns', padx=8, pady=8)
        
        small_minus_button = ctk.CTkButton(self, command= lambda: self.update_weight(('minus', 'small')), text='-', font= font, text_color = BLACK, fg_color = LIGHT_GRAY)
        small_minus_button.grid(row=0, column=1, padx=4, pady=4)
        
        plus_button = ctk.CTkButton(self, command= lambda: self.update_weight(('plus', 'large')), text='+', font= font, text_color = BLACK, fg_color = LIGHT_GRAY)
        plus_button.grid(row=0, column=4, sticky='ns', padx=8, pady=8)
        
        small_plus_button = ctk.CTkButton(self, command= lambda: self.update_weight(('plus', 'small')), text='+', font= font, text_color = BLACK, fg_color = LIGHT_GRAY)
        small_plus_button.grid(row=0, column=3, padx=4, pady=4)
    
    def update_weight(self, info= None):
        if info:

            if self.metric_bool.get():
                amount = 1 if info[1] == 'large' else 0.1
            else:
                amount = 0.453592 if info[1] == 'large' else 0.453592 / 16
            
            if info[0] == 'plus':
                self.weight_float.set(self.weight_float.get() + amount)
            else:
                self.weight_float.set(self.weight_float.get() - amount)
            
        if self.metric_bool.get():
            self.output_string.set(f'{round(self.weight_float.get(),1)}kg')
        else:
            raw_ounces = self.weight_float.get() * 2.20462 * 16
            pounds, ounces = divmod(raw_ounces, 16)
            self.output_string.set(f'{int(pounds)}lb {int(ounces)}oz')
    

class HeightInput(ctk.CTkFrame):
    def __init__(self, parent, height_int, metric_bool):
        super().__init__(master = parent, fg_color = WHITE)
        self.grid(row=3, column=0, sticky= 'nsew', padx=10, pady=10)
        self.metric_bool = metric_bool
        
        # widgets
        slider = ctk.CTkSlider(
            master = self,
            command= self.update_text,
            button_color = GREEN,
            button_hover_color = GRAY,
            progress_color= GREEN,
            fg_color = LIGHT_GRAY,
            variable= height_int,
            from_ = 100,
            to = 250
        )
        slider.pack(side='left', fill='x', expand=True, pady=10, padx=10)
        
        self.output_string = ctk.StringVar()
        self.update_text(height_int.get())
        
        output_text = ctk.CTkLabel(self, textvariable = self.output_string, text='1.80m', text_color=BLACK, font=ctk.CTkFont( family= FONT, size = INPUT_FONT_SIZE))
        output_text.pack(side="left", padx=20)
    
    def update_text(self, amount):
        if self.metric_bool.get():
            text_string = str(int(amount))
            meter = text_string[0]
            cm = text_string[1:]
            self.output_string.set(f'{meter}.{cm}m')
            
        else: # IMPERIAL
            feet, inches = divmod(amount / 2.54, 12)
            self.output_string.set(f'{int(feet)}\'{int(inches)}\"')
  
      
class UnitSwitcher(ctk.CTkLabel):
    def __init__(self, parent, metric_bool):
        super().__init__(master = parent, 
                            text = 'metric',
                            text_color= DARK_GREEN, 
                            font= ctk.CTkFont(family= FONT, size = SWITCH_FONT_SIZE,
                        weight="bold"))
        self.place(relx=0.98, rely=0.01, anchor='ne')
        self.metric_bool = metric_bool
        self.bind('<Button>', self.change_units)
    
    def change_units(self, event):
        # change the metric bool True -> False
        self.metric_bool.set(not self.metric_bool.get())
        
        if self.metric_bool.get():
            self.configure(text = 'metric')
        else:
            self.configure(text = 'Imperial')
        

if __name__ == "__main__":
    App()
