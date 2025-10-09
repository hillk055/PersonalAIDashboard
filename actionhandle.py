import inspect
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st


class ToDoListHandler:
    def __init__(self):
        self.df = pd.read_excel('', index_col=0)
        self.df['Due Date'] = pd.to_datetime(self.df['Due Date']).dt.date
        self.to_do_df = None
        self.date = datetime.today().date()

    def show(self) -> None:
        """Refresh filtered to-do list for today."""
        self.to_do_df = self.df[self.df['Due Date'] == self.date]

    def navigate_to_to_do_list(self) -> None:
        """Navigate to do list"""

        return st.switch_page("pages/Notes.py")

    def add_to_todo_list(self, to_do: str, when: datetime, period: int, frequency: int) -> None:

        """
            Adds a repeating task to the to-do list.

            Parameters
            ----------
            to_do : str
                A short, clear task name. Example: "Go for a run" or "Email report".
            when : str (format: "YYYY-MM-DD")
                The start date for the first task occurrence.
            period : int
                Total number of days to repeat the task (the overall duration).
            frequency : int
                The number of days between each repetition.

            Returns
            -------
            None

            AI Instruction
            --------------
            When generating inputs for this function:
              - If when cannot be inferred -> Default today's date
              - If period cannot be inferred -> Default 365 days from now
              -if frequency cannot be inferred -> Default every day
              - Example return:
                workout, 2025-10-07, 30, 2
            """
        try:
            period = int(period)
            frequency = int(frequency)

        except TypeError:
            return

        new_items = []
        when = datetime.strptime(when, "%Y-%m-%d").date()
        date = when
        end_date = date + timedelta(days=period)

        while date < end_date:
            new_items.append({'Task': to_do, 'Due Date': date, 'Done': False})
            date += timedelta(days=frequency)

        added_items = pd.DataFrame(new_items)
        self.df = pd.concat([self.df, added_items], ignore_index=True)
        self.show()

    def mark_task_complete(self, task: str) -> None:
        """
        Mark a specific task as completed if it is due today, and refresh the to-do list display.

        Parameters
        ----------
        task : str
        The name of the task to mark as done.
           """

        self.df.loc[(self.df['Due Date'] == self.date) & (self.df['Task'] == task), 'Done'] = True
        self.show()

    def mark_task_incomplete(self, task):
        """
        Mark a specific task as uncompleted if selected by the user and refresh the to-do list display.

        Parameters
        ----------
        task : str
        The name of the task to mark as not done.
        """

        self.df.loc[(self.df['Due Date'] == self.date) & (self.df['Task'] == task), 'Done'] = False
        self.show()

    def remove_task(self, task, date_to_rm):
        if date_to_rm == 'All':
            self.df = self.df[~(self.df['Task'] == task)]
        else:
            self.df = self.df[~((self.df['Task'] == task) & (self.df['Due Date'] == date_to_rm))]
        self.to_do_list()

    def save_input(self):
        self.df.to_excel('')


class InventoryHandler:

    def __init__(self):

        self.df = pd.read_csv('')
        self.df['Best Before'] = pd.to_datetime(self.df['Best Before'])
        self.date = datetime.today().date()
        self.date = pd.to_datetime(self.date)
        print(self.date)
    
    @staticmethod
    def get_date_difference(df, date):

        df['Days Before Expiry'] = df['Best Before'] - date
        return df
        
    def prioritise_items_by_best_before_date(self):
        
        self.df = self.get_date_difference(self.df, self.date)
    
    def best_before_date_tracker(self):
        pass

        pass
    def add_items(self):
        pass
    def update_price(self):
        # Need to add memory for the AI to handle this if price is not specified
        pass

    def remove_items(self, items: list) -> None:

        for x in items:
            self.df = self.df[~(self.df['Item'] == x)]

    def get_price_multiple_items(self):
        pass

    def __str__(self):
        # provide a summary/overview of the inventory
        pass
    def __len__(self):
        # provide the length of the inventory
        pass

class BudgetHandler:

    def __init__(self):
        pass






def make_action():

    action = 'add_to_todo_list'

    '''funcs = {name: func for name, func in inspect.getmembers(ActionHandler(), predicate=inspect.ismethod)
             if not name.endswith('__')}
    print(funcs)
    funcs[action]()'''


if __name__ == "__main__":

    inv = InventoryHandler()
    inv.prioritise_items_by_best_before_date()

