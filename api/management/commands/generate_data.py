from django.core.management.base import BaseCommand

import random
import string

from faker import Faker

from account.models import Account
from category.models import Category
from transaction.models import Transaction
from user.models import User


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for _ in range(length))
    return password


fake = Faker()


def generate_users(num_users=1):
    if num_users == 0:
        return [User.objects.get(id=1)]

    users = []
    for _ in range(num_users):
        email = fake.email()
        user = User.objects.create(email=email)
        pwd = generate_password()
        user.set_password(pwd)
        users.append(user)
    return users


def generate_accounts(user, num_accounts=1):
    accounts = []
    for _ in range(num_accounts):
        name = fake.word()
        account_type = random.choice(["Checking", "Savings", "Credit Card"])
        balance = random.uniform(100, 10000)
        account = Account.objects.create(
            user=user, name=name, account_type=account_type, balance=balance
        )
        accounts.append(account)
    return accounts


def generate_categories(num_categories=1):
    if Category.objects.all().count() > 1:
        return list(Category.objects.all())

    categories = []
    names = [
        "Kids",
        "Pets",
        "Home Improvement",
        "Taxes",
        "Insurance",
        "Charity",
        "Investments",
        "Gifts",
        "Subscriptions",
        "Utilities",
        "Personal Care",
        "Travel",
        "Education",
        "Healthcare",
        "Housing",
        "Shopping",
        "Entertainment",
        "Utilities",
        "Transportation",
        "Food",
    ]
    descs = [
        "Expenses related to children's activities, education, and childcare",
        "Expenses related to pet care, including food, veterinary bills, and grooming",
        "Expenses related to home renovations, repairs, and improvements",
        "Expenses related to income taxes, property taxes, and other taxes",
        "Expenses related to insurance premiums for health, auto, home, and life insurance",
        "Expenses related to donations and charitable contributions",
        "Expenses related to investment activities such as stocks, bonds, and retirement accounts",
        "Expenses related to gift purchases for birthdays, holidays, and special occasions",
        "Expenses related to subscription services such as streaming platforms, magazines, and memberships",
        "Expenses related to utility bills such as electricity, water, and gas",
        "Expenses related to personal grooming, haircuts, and beauty products",
        "Expenses related to vacations, flights, hotels, and travel insurance",
        "Expenses related to tuition fees, books, school supplies, and educational materials",
        "Expenses related to medical care, health insurance, and prescription medications",
        "Expenses related to rent or mortgage payments, property taxes, and home maintenance",
        "Expenses related to shopping for various items",
        "Expenses related to entertainment and leisure activities",
        "Expenses related to utility bills such as electricity, water, and gas",
        "Expenses related to transportation and commuting",
        "Expenses related to food and dining out",
    ]
    for i in range(len(names)):
        name = names[i]
        description = descs[i]
        category = Category.objects.create(name=name, description=description)
        categories.append(category)
    return categories


def generate_transactions(user, accounts, categories, num_transactions=1):
    transactions = []
    for _ in range(num_transactions):
        account = random.choice(accounts)
        amount = random.uniform(1, 1000)
        transaction_type = random.choice(["income", "expense", "transfer"])
        category = random.choice(categories) if transaction_type != "transfer" else None
        date = fake.date_time_between(start_date="-30d", end_date="now")
        description = fake.sentence()

        transaction = Transaction.objects.create(
            user=user,
            account=account,
            amount=amount,
            type=transaction_type,
            category=category,
            date=date,
            description=description,
        )
        transactions.append(transaction)
    return transactions


class Command(BaseCommand):
    help = "Generate random data for the application"

    def handle(self, *args, **kwargs):
        num_users = 0
        num_accounts = 2
        num_transactions = 20

        users = generate_users(num_users)
        categories = generate_categories()

        for user in users:
            accounts = generate_accounts(user, num_accounts)
            transactions = generate_transactions(
                user, accounts, categories, num_transactions
            )

        print("Data generation complete.")
