# Author: Miguel Martinez Lopez
#
# Version: 1.0.7
#
# Uncomment the next line to see my email
# print("Author's email: %s"%"61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex"))

import calendar
import datetime
from transverse.Util import Util
from Controleur.PlayListManager import PlayListManager

import tkinter as Tkinter
import tkinter.font as tkFont
import tkinter.ttk as ttk

from tkinter.constants import CENTER, LEFT, N, E, W, S
from tkinter import StringVar

def get_calendar(locale, fwday):
    # instantiate proper calendar class
    if locale is None:
        return calendar.TextCalendar(fwday)
    else:
        return calendar.LocaleTextCalendar(fwday, locale)


class Calendar(ttk.Frame):
    datetime = calendar.datetime.datetime
    timedelta = calendar.datetime.timedelta

    def __init__(self, master=None, year=None, month=None, firstweekday=calendar.MONDAY, locale=None, 
                 activebackground='#b1dcfb', activeforeground='black', selectbackground='#003eff', 
                 selectforeground='white', command=None, borderwidth=1, relief="solid", on_click_month_button=None,
                 pm=PlayListManager(None)):
        """
        WIDGET OPTIONS

            locale, firstweekday, year, month, selectbackground,
            selectforeground, activebackground, activeforeground, 
            command, borderwidth, relief, on_click_month_button
        """

        if year is None:
            year = self.datetime.now().year
        
        if month is None:
            month = self.datetime.now().month

        self._selected_date = None

        self._sel_bg = selectbackground 
        self._sel_fg = selectforeground

        self._act_bg = activebackground 
        self._act_fg = activeforeground
        
        self.on_click_month_button = on_click_month_button
        
        self._selection_is_visible = False
        self._command = command
        self.pm = pm
        ttk.Frame.__init__(self, master, borderwidth=borderwidth, relief=relief)
        
        self.bind("<FocusIn>", lambda event:self.event_generate('<<DatePickerFocusIn>>'))
        self.bind("<FocusOut>", lambda event:self.event_generate('<<DatePickerFocusOut>>'))
    
        self._cal = get_calendar(locale, firstweekday)

        # custom ttk styles
        style = ttk.Style()
        style.layout('L.TButton', (
            [('Button.focus', {'children': [('Button.leftarrow', None)]})]
        ))
        style.layout('R.TButton', (
            [('Button.focus', {'children': [('Button.rightarrow', None)]})]
        ))

        self._font = tkFont.Font()
        
        self._header_var = StringVar()

        # header frame and its widgets
        hframe = ttk.Frame(self)
        lbtn = ttk.Button(hframe, style='L.TButton', command=self._on_press_left_button)
        lbtn.pack(side=LEFT)
        
        self._header = ttk.Label(hframe, width=15, font=Util.getFont('font3'), anchor=CENTER, textvariable=self._header_var)
        self._header.pack(side=LEFT, padx=12)
        
        rbtn = ttk.Button(hframe, style='R.TButton', command=self._on_press_right_button)
        rbtn.pack(side=LEFT)
        hframe.grid(columnspan=7, pady=4)

        self._day_labels = {}

        days_of_the_week = self._cal.formatweekheader(3).split()
 
        for i, day_of_the_week in enumerate(days_of_the_week):
            Tkinter.Label(self, text=day_of_the_week, font=Util.getFont('font3'), background='grey90').grid(row=1, column=i, sticky=N+E+W+S)

        for i in range(6):
            for j in range(7):
                self._day_labels[i,j] = label = Tkinter.Label(self, background = "white", font=Util.getFont('font4'))
                
                label.grid(row=i+2, column=j, sticky=N+E+W+S, padx=5, pady=10)
                #label.bind("<Enter>", lambda event: event.widget.configure(background=self._act_bg, foreground=self._act_fg))
                #label.bind("<Leave>", lambda event: event.widget.configure(background="white"))

                label.bind("<1>", self._pressed)
        
        # adjust its columns width
        font = tkFont.Font()
        maxwidth = max(font.measure(text) for text in days_of_the_week)
        for i in range(7):
            self.grid_columnconfigure(i, minsize=maxwidth, weight=1)

        self._year = None
        self._month = None

        # insert dates in the currently empty calendar
        self._build_calendar(year, month)

    def _build_calendar(self, year, month):
        if not( self._year == year and self._month == month):
            self._year = year
            self._month = month

            # update header text (Month, YEAR)
            header = self._cal.formatmonthname(year, month, 0)
            self._header_var.set(header.title())

            # update calendar shown dates
            cal = self._cal.monthdayscalendar(year, month)
            for i in range(len(cal)):
                
                week = cal[i] 
                fmt_week = [('%02d' % day) if day else '' for day in week]
                
                for j, day_number in enumerate(fmt_week):
                    statPL = self.pm.getStatPL(year, month, day_number)
                    self._day_labels[i,j]["text"] = day_number + Util.getUnicodeCharExposant(statPL)
                    try:
                        if Util.estDateAnterieurAujourdhui(year, month, day_number):
                            self._day_labels[i,j]["bg"] = 'red'
                        else:
                            if statPL == 0:
                                self._day_labels[i,j]["bg"] = 'steel blue'
                            else:
                                self._day_labels[i,j]["bg"] = 'green'    
                    except ValueError: #cas vide sur le jour            
                        self._day_labels[i,j]["bg"] = 'white'
                        self._day_labels[i,j]["text"] = day_number #ne pas mettre exposant zero seul
            if len(cal) < 6:
                for j in range(7):
                    self._day_labels[5,j]["text"] = ""
                    self._day_labels[5,j]["bg"] = 'white'

        if self._selected_date is not None and self._selected_date.year == self._year and self._selected_date.month == self._month:
            self._show_selection()

    def _find_label_coordinates(self, date):
         first_weekday_of_the_month = (date.weekday() - date.day) % 7
         
         return divmod((first_weekday_of_the_month - self._cal.firstweekday)%7 + date.day, 7)
        
    
    def _pressed(self, evt):
        """Clicked somewhere in the calendar."""
        
        text = evt.widget["text"]
        
        if text == "":
            return

        day_number = int(text[0:2]) #le 3ieme character est l'exposant

        new_selected_date = datetime.datetime(self._year, self._month, day_number)
        self._selected_date = new_selected_date
         
        if self._command:
            self._command(self._selected_date)

    def _on_press_left_button(self):
        self.prev_month()
        
        if self.on_click_month_button is not None:
            self.on_click_month_button()
    
    def _on_press_right_button(self):
        self.next_month()

        if self.on_click_month_button is not None:
            self.on_click_month_button()
        
    def select_current_date(self):
        """Update calendar to current date."""
        if self._selection_is_visible: self._clear_selection()

        self._selected_date = datetime.datetime.now()
        self._build_calendar(self._selected_date.year, self._selected_date.month)

    def prev_month(self):
        """Updated calendar to show the previous week."""
        if self._selection_is_visible: self._clear_selection()
        
        date = self.datetime(self._year, self._month, 1) - self.timedelta(days=1)
        self._build_calendar(date.year, date.month) # reconstuct calendar

    def next_month(self):
        """Update calendar to show the next month."""
        if self._selection_is_visible: self._clear_selection()

        date = self.datetime(self._year, self._month, 1) + \
            self.timedelta(days=calendar.monthrange(self._year, self._month)[1] + 1)

        self._build_calendar(date.year, date.month) # reconstuct calendar
    
    def get_selection(self):
        """Return a datetime representing the current selected date."""
        return self._selected_date
        
    selection = get_selection

    def set_selection(self, date):
        """Set the selected date."""
        if self._selected_date is not None and self._selected_date != date:
            self._clear_selection()

        self._selected_date = date

        self._build_calendar(date.year, date.month) # reconstruct calendar

      
    @property
    def current_text(self):
        return self.date_var.get()
        
    @current_text.setter
    def current_text(self, text):
        return self.date_var.set(text)
        
    @property
    def current_date(self):
        try:
            date = datetime.datetime.strptime(self.date_var.get(), self.date_format)
            return date
        except ValueError:
            return None
    
    @current_date.setter
    def current_date(self, date):
        self.date_var.set(date.strftime(self.date_format))
        
    @property
    def is_valid_date(self):
        if self.current_date is None:
            return False
        else:
            return True

    
    def show_calendar(self):
        if not self._is_calendar_visible:
            self.calendar_frame.place(in_=self, relx=0, rely=1)
            self.calendar_frame.lift()

        self._is_calendar_visible = True

    def hide_calendar(self):
        if self._is_calendar_visible:
            self.calendar_frame.place_forget()
        
        self._is_calendar_visible = False

    def erase(self):
        self.hide_calendar()
        self.date_var.set("")
    
    @property
    def is_calendar_visible(self):
        return self._is_calendar_visible

    
    def _on_click(self, event):
        str_widget = str(event.widget)

        if str_widget == str(self):
            if not self._is_calendar_visible:
                self.show_date_on_calendar()
        else:
            if not str_widget.startswith(str(self.calendar_frame)) and self._is_calendar_visible:
                self.hide_calendar()


class Control():
    def __init__(self, rootTK, entrywidth=None, entrystyle=None, datevar=None, dateformat="%Y-%m-%d", onselect=None,  
                 borderwidth=1, relief="solid", pm=PlayListManager(None)):
        
        self.tk=rootTK
        if datevar is not None:
            self.date_var = datevar
        else:
            self.date_var = Tkinter.StringVar()
           
        self.date_format = dateformat
        
        self._is_calendar_visible = True
        self._on_select_date_command = onselect
        self.pm = pm
       
        '''
        associer la frame avec tous les evenements
        '''
    def associerEvts(self):
        
        
        # CTRL + PAGE UP: Move to the previous month.
        self.frame.bind("<Control-Prior>", lambda event: self.calendar_frame.prev_month())
        
        # CTRL + PAGE DOWN: Move to the next month.
        self.frame.bind("<Control-Next>", lambda event: self.calendar_frame.next_month())

        # CTRL + SHIFT + PAGE UP: Move to the previous year.
        self.frame.bind("<Control-Shift-Prior>", lambda event: self.calendar_frame.prev_year())

        # CTRL + SHIFT + PAGE DOWN: Move to the next year.
        self.frame.bind("<Control-Shift-Next>", lambda event: self.calendar_frame.next_year())
        
        # CTRL + LEFT: Move to the previous day.
        self.frame.bind("<Control-Left>", lambda event: self.calendar_frame.select_prev_day())
        
        # CTRL + RIGHT: Move to the next day.
        self.frame.bind("<Control-Right>", lambda event: self.calendar_frame.select_next_day())
        
        # CTRL + UP: Move to the previous week.
        self.frame.bind("<Control-Up>", lambda event: self.calendar_frame.select_prev_week_day())
        
        # CTRL + DOWN: Move to the next week.
        self.frame.bind("<Control-Down>", lambda event: self.calendar_frame.select_next_week_day())

        # CTRL + END: Close the datepicker and erase the date.
        self.frame.bind("<Control-End>", lambda event: self.erase())

        # CTRL + HOME: Move to the current month.
        self.frame.bind("<Control-Home>", lambda event: self.calendar_frame.select_current_date())
        
        # CTRL + SPACE: Show date on calendar
        self.frame.bind("<Control-space>", lambda event: self.show_date_on_calendar())
        
        # CTRL + Return: Set to entry current selection
        self.frame.bind("<Control-Return>", lambda event: self.set_date_from_calendar())

        '''
        affiche la frame avec ses composants
        '''
    def afficher(self):
        wdw = Tkinter.Toplevel()
        wdw.geometry(Util.configValue('dimensions', 'geometryCalender'))
        wdw.title(Util.configValue('commun', 'titreCal'))
       # wdw.geometry("{}x{}+{}+{}".format(300, 390, 400, 300))
        #wdw.geometry('+400+300')
        self.frame = wdw
        
        self.__dessiner()
        self.associerEvts()
        #rendre la fenetre modale
       # wdw.transient(self.tk)
        wdw.grab_set()
       # self.tk.wait_window(wdw)
        #wdw.pack(expand=True, fill="both")
        self.calendar_frame.pack(anchor="w")
    
    '''
        dessine la frame avec ses composants
        '''
    def __dessiner(self):   
       # ttk.Entry.__init__(self, self.frame, textvariable=self.date_var)
        firstweekday=calendar.MONDAY
        locale='fr'
        activebackground='#b1dcfb'
        activeforeground='black'
        selectbackground='#003eff' 
        selectforeground='white'
        self.calendar_frame = Calendar(self.frame, firstweekday=firstweekday, locale=locale, activebackground=activebackground,
                                        activeforeground=activeforeground, selectbackground=selectbackground, 
                                        selectforeground=selectforeground, pm=self.pm,
                                            command=self._on_selected_date)
        
        # on affiche la frame
        #self.calendar_frame.show_date_on_calendar()
    
    '''
        callback sur click date calendrier
        '''
    def _on_selected_date(self, date):
        
        if self._on_select_date_command is not None:
            self._on_select_date_command(date)
