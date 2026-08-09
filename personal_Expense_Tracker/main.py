import json
import os


Data_file = os.path.join(os.path.dirname(__file__), "data.json")    

week_size = 7
month_size = 30

def load_data():
    with open(Data_file, "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open(Data_file, "w") as f:
        json.dump(data, f, indent=4)

class ExpenseTracker:
    def __init__(self):
        self.data=load_data()

    def is_first_run(self):
        return (self.data["limits"]["daily"] == 0 and self.data["limits"]["weekly"] == 0 and self.data["limits"]["monthly"] == 0) and self.data["categories"] == []

    def setup(self):
        print("Welcome to the your personal expense tracker!")
        print("Let's set up your daily, weekly, and monthly limits.")
        daily_limit = float(input("Enter your daily limit: "))
        weekly_limit = float(input("Enter your weekly limit: "))
        monthly_limit = float(input("Enter your monthly limit: "))
        self.data["limits"]["daily"] = daily_limit
        self.data["limits"]["weekly"] = weekly_limit
        self.data["limits"]["monthly"] = monthly_limit

        print("Now, let's set up your expense categories.")
        categories_number = int(input("How many categories do you want to add? "))
        for i in range(categories_number):
            category=input(f"Enter Category {i+1}: ")
            self.data["categories"].append(category)

        save_data(self.data)

    def enter_daily_expenses(self):
        self.data["day_count"] += 1
        day=self.data["day_count"]

        self.data["expenses"][f"Day {day}"] = {}

        for i in self.data["categories"]:
            expense=float(input(f"Enter your daily expense for {i}: "))
            self.data["expenses"][f"Day {day}"][i] = expense

        save_data(self.data)

    def check_daily_limit(self):
        day_num=self.data["day_count"]
        today=self.data["expenses"][f"Day {day_num}"]
        today_expense=sum(today.values())

        if today_expense>self.data["limits"]["daily"]:
            print(f"You have exceeded your daily limit of {self.data['limits']['daily']}. Your total expense today is {today_expense}.")
        else:
            print(f"You are within your daily limit of {self.data['limits']['daily']}. Your total expense today is {today_expense}.")

    def weekly_report(self):
        day_count = self.data["day_count"]

        category_totals = {category: 0 for category in self.data["categories"]}
        weekly_total = 0

        for i in range(day_count - week_size + 1, day_count + 1):
            if i <= 0:
                continue
            day_expense = self.data["expenses"][f"Day {i}"]
            print(f"Your Daily Expenses for Day {i}: {day_expense}")

            for category, amount in day_expense.items():
                category_totals[category] += amount

            weekly_total = sum(category_totals.values())

        highest_category_weekly = max(category_totals, key=category_totals.get)

        if weekly_total > self.data["limits"]["weekly"]:
            print(f"You have exceeded your weekly limit of {self.data['limits']['weekly']}. Your total expense for the week is {weekly_total}.")
        else:
            print(f"You are within your weekly limit of {self.data['limits']['weekly']}. Your total expense for the week is {weekly_total}.")

        print(f"Your highest spending category for the week is {highest_category_weekly} with a total of {category_totals[highest_category_weekly]}.")

    def monthly_report(self):
        day_count = self.data["day_count"]

        category_totals = {category: 0 for category in self.data["categories"]}
        monthly_total = 0

        for i in range(day_count - month_size + 1, day_count + 1):
            if i <= 0:
                continue
            day_expense = self.data["expenses"][f"Day {i}"]
            print(f"Your Daily Expenses for Day {i}: {day_expense}")

            for category, amount in day_expense.items():
                category_totals[category] += amount

            monthly_total = sum(category_totals.values())

        highest_category_monthly = max(category_totals, key=category_totals.get)

        if monthly_total > self.data["limits"]["monthly"]:
            print(f"You have exceeded your monthly limit of {self.data['limits']['monthly']}. Your total expense for the month is {monthly_total}.")
        else:
            print(f"You are within your monthly limit of {self.data['limits']['monthly']}. Your total expense for the month is {monthly_total}.")

        print(f"Your highest spending category for the month is {highest_category_monthly} with a total of {category_totals[highest_category_monthly]}.")

    def __str__(self):
        return (f"Hi Today is Day {self.data['day_count']}. Your daily limit is {self.data['limits']['daily']}, your weekly limit is {self.data['limits']['weekly']}, and your monthly limit is {self.data['limits']['monthly']}.\n And your categories of expeses are {self.data['categories']}.")

    def __len__(self):
        return len(self.data['expenses'])


def main():
    tracker = ExpenseTracker()
    print(tracker)

    if tracker.is_first_run():
        tracker.setup()

    tracker.enter_daily_expenses()
    tracker.check_daily_limit()

    if tracker.data["day_count"] % week_size == 0:
        tracker.weekly_report()
    if tracker.data["day_count"] % month_size == 0:
        tracker.monthly_report()



if __name__ == "__main__":
    main()