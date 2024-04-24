'''
user_cli.py
Hange Zhang CS5001 Spring 2024 Final Project
This module handles user interactions for the data dashboard program.
'''


def display_menu():
    print("\nMenu:")
    print("1. Show the bikeways recommendation with detailed information")
    print("2. Find nearest washrooms to a specific bikeway")
    print("3. Exit")
    return input("Enter your choice (1-3): ")


def get_bikeway_name():
    return input("Enter the name of the bikeway: ")
