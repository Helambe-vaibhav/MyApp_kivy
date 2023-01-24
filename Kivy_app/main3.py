# Helambe Vaibhav
# version 1
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivy import *
from kivymd import *
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import MDList
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.datatables import MDDataTable

from datetime import datetime
import DataBaseFiles
    
# create a class for the main screen
class MainScreen(MDScreen):
    # load kv file in class 
    Builder.load_file("main3.kv")
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # get button by id
        self.time_label = self.ids.time_label
        # schedule update_time function to be called every second
        Clock.schedule_interval(self.update_time, 1)
        self.CurrentAccountBalance = self.ids.CurrentAccountBalance
    
    # this function is called when the screen is entered
    def on_enter(self, *args):
        self.update_time()
        acc = DataBaseFiles.AccountData()
        self.CurrentAccountBalance.text = "Balance: "+str(acc.get_total_Balance())

    # this function is called every second to update the time to make dynamic labels for button
    def update_time(self, *args):
        with open("lifeGoal.txt", "r") as f:
            lifegoalDate = f.readline()
            lifegoalDate = lifegoalDate.strip()
            f.close()
        lifegoalDate = datetime.strptime(lifegoalDate, "%d/%m/%Y")        
        remaining_time = lifegoalDate - datetime.now()
        days = remaining_time.days
        hours = remaining_time.seconds // 3600
        minutes = (remaining_time.seconds // 60) % 60
        seconds = remaining_time.seconds % 60
        self.time_label.text = f"{days}:{hours}:{minutes}:{seconds}"
    
    # this function is called when Time button is pressed
    def go_to_life_goal(self):
        self.manager.current = "LifeGoal"
        self.manager.transition.direction = "up"
    
    # this function is called when Balance button is pressed
    def go_to_Acccount(self):
        self.manager.current = "Account"
        self.manager.transition.direction = "left"

    # this function is called when Skills button is pressed
    def go_to_skillsCat(self):
        self.manager.current = "SkillsCat"
        self.manager.transition.direction = "right"
    
# create a class for the LifeGoal screen
class LifeGoal(MDScreen):
    def __init__(self, **kwargs):
        super(LifeGoal, self).__init__(**kwargs)
        # get button by id
        self.date_label = self.ids.date_label
        self.goal_label = self.ids.goal_label
        self.edit_button = self.ids.edit_button
    

    def edit_life_goal(self):
        self.remove_widget(self.date_label)
        self.remove_widget(self.goal_label)
        self.remove_widget(self.edit_button)
        self.date_textfield = MDTextField(
            hint_text = "Enter date",
            pos_hint = {"center_x": 0.6, "center_y": 0.8},
            size_hint_x = None,
            width = 150
        )
        self.goal_textfield = MDTextField(
            hint_text = "Enter goal",
            pos_hint = {"center_x": 0.6, "center_y": 0.7},
            size_hint_x = None,
            width = 150
        )
        self.save_button = MDFloatingActionButton(
            icon = "check",
            pos_hint = {"center_x": 0.9, "center_y": 0.1},
            on_press = self.save_life_goal
        )
        self.add_widget(self.date_textfield)
        self.add_widget(self.goal_textfield)
        self.add_widget(self.save_button)

    def save_life_goal(self, *args):
        date = self.date_textfield.text
        goal = self.goal_textfield.text
        with open("lifeGoal.txt", "w") as f:
            f.write(date + "\n")
            f.write(goal)
            f.close()
        self.remove_widget(self.date_textfield)
        self.remove_widget(self.goal_textfield)
        self.remove_widget(self.save_button)
        #  got o on_enter method
        self.on_enter()
        self.add_widget(self.date_label)
        self.add_widget(self.goal_label)
        self.add_widget(self.edit_button)

    def on_enter(self, *args):
        with open("lifeGoal.txt", "r") as f:
            date = f.readline()
            date = date.strip()
            goal = f.readline()
            goal = goal.strip()
            f.close()
        self.date_label.text = date
        self.goal_label.text = goal

    def go_to_main_screen(self):
        self.manager.current = "MainScreen"
        self.manager.transition.direction = "left"
    
class Account(MDScreen):
    def __init__(self, **kwargs):
        super(Account, self).__init__(**kwargs)
        self.total_balance_label = self.ids.total_balance_label
        self.transactions = DataBaseFiles.AccountData()
        self.total_balance_label.text = str(self.transactions.get_total_Balance())
        self.description_textfield = self.ids.description_textfield
        self.amount_textfield = self.ids.amount_textfield
        self.add_transaction_button = self.ids.add_transaction_button
        self.data_tables = MDDataTable(
            size_hint = (0.9, 0.6),
            pos_hint = {"center_x": 0.5, "center_y": 0.47},
            use_pagination = True,
            # row data and column data size must be the same
            column_data = [
                ("Description", dp(40)),
                ("Amount", dp(15)),
                ("Date", dp(25))
            ],
            row_data = self.transactions.get_all_records()
        )
        self.add_widget(self.data_tables)


    def income_button_pressed(self):
        self.type = 0
        self.add_widget(self.data_tables)
        self.add_widget(self.add_transaction_button)
        self.save_transaction()
        
    
    def expense_button_pressed(self):
        self.type = 1
        self.add_widget(self.data_tables)
        self.add_widget(self.add_transaction_button)
        self.save_transaction()

    def save_transaction(self):
        description = self.description_textfield.text
        amount = self.amount_textfield.text
        type = self.type
        self.transactions.add_new_record(type,description, int(amount))
        self.total_balance_label.text = str(self.transactions.get_total_Balance())
        self.data_tables.row_data = self.transactions.get_all_records()
    
    def add_new_transaction(self):
        self.remove_widget(self.data_tables)
        self.remove_widget(self.ids.add_transaction_button)
        
    def go_to_main_screen(self):
        self.manager.current = "MainScreen"
        self.manager.transition.direction = "right"

class SkillsCat(MDScreen):
    def __init__(self, **kwargs):
        super(SkillsCat, self).__init__(**kwargs)
        self.skillsDB = DataBaseFiles.SkillsData()
        self.all_categorys = self.skillsDB.get_all_categorys()
        # create MDTEXTFIELD
        self.category_textfield = MDTextField(
            id = "category_textfield",
            hint_text = "Enter Category",
            pos_hint = {"center_x": 0.4, "center_y": 0.8},
            size_hint = (0.6, 0.1),
            helper_text = "Enter Category",
            helper_text_mode = "on_focus"
        )
    def on_enter(self, *args):
        # create scroallable list
        self.category = MDList(
            id = "skills_list",
            pos_hint = {"center_x": 0.5, "center_y": 0.4},
            size_hint = (0.6, 0.6)
        )
        for category in self.all_categorys:
            print(category)
            self.category.add_widget(
                OneLineListItem(
                    text = category,
                    on_press = self.show_skills
                )
            )
        self.add_widget(self.category)
        self.add_widget(self.category_textfield)

    def go_to_main_screen(self):
        self.manager.current = "MainScreen"
        self.manager.transition.direction = "right"

        
    def show_skills(self, instance):
        print(instance.text)

    def save_category(self):
        temp_category = self.category_textfield.text
        print(temp_category)
        self.skillsDB.add_category(temp_category)
        self.category.add_widget(
            OneLineListItem(
                text = temp_category,
                on_press = self.show_skills
            )
        )
        self.category_textfield.text = ""

class MainApp(MDApp):
    def build(self):
        Window.size = (300, 600)
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainScreen(name="MainScreen"))
        screen_manager.add_widget(Account(name="Account"))
        screen_manager.add_widget(LifeGoal(name="LifeGoal"))
        screen_manager.add_widget(SkillsCat(name="SkillsCat"))
        return screen_manager
        

if __name__ == "__main__":
    MainApp().run()





