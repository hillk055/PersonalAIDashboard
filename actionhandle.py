import inspect
from datetime import datetime, timedelta
import pandas as pd


class ToDoListHandler:
    def __init__(self):
        self.df = pd.read_excel('', index_col=0)
        self.df['Due Date'] = pd.to_datetime(self.df['Due Date']).dt.date
        self.to_do_df = None
        self.date = datetime.today().date()

    def to_do_list(self):
        """Refresh filtered to-do list for today."""
        self.to_do_df = self.df[self.df['Due Date'] == self.date]

    def add_to_todo_list(self, to_do, when, period, frequency):

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
        self.to_do_list() 

    def mark_task_complete(self, task):
        self.df.loc[(self.df['Due Date'] == self.date) & (self.df['Task'] == task), 'Done'] = True
        self.to_do_list()  

    def mark_task_incomplete(self, task):
        self.df.loc[(self.df['Due Date'] == self.date) & (self.df['Task'] == task), 'Done'] = False
        self.to_do_list()

    def remove_task(self, task, date_to_rm):
        if date_to_rm == 'All':
            self.df = self.df[~(self.df['Task'] == task)]
        else:
            self.df = self.df[~((self.df['Task'] == task) & (self.df['Due Date'] == date_to_rm))]
        self.to_do_list()

    def save_input(self):
        self.df.to_excel('')



def make_action():

    action = 'add_to_todo_list'

    '''funcs = {name: func for name, func in inspect.getmembers(ActionHandler(), predicate=inspect.ismethod)
             if not name.endswith('__')}
    print(funcs)
    funcs[action]()'''


if __name__ == "__main__":

    pass

