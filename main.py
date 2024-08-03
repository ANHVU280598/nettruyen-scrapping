from scrap_homepage import scrap_homepage
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor

def process_page(i):
    driver = Driver(uc=True)
    try:
        page_index = "" if i == 1 else f"?page={i}"
        url = f"https://nettruyenfull.com{page_index}"
        scrap_homepage(driver, url, i)
        print(f"Data Stored for Page {i}")
    finally:
        driver.quit()

def display_menu():
    print("Main Menu")
    print("1. Update All Manga Home Page")
    print("2. Update All Info Of Manga in Existing Database")
    print("3. Fully Update All News And Current Comics.")
    print("4. Exit")

def option1():
    print("Update All Manga Home Page")
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(process_page, i) for i in range(1, 314)]
        for future in futures:
            future.result()

def option2():
    print("Update All Info Of Manga in Existing Database")
    # Implement option 2 functionality here

def option3():
    print("Fully Update All News And Current Comics.")
    # Implement option 3 functionality here

def main():
    choice = ''
    while choice != '4':
        display_menu()
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            option1()
        elif choice == '2':
            option2()
        elif choice == '3':
            option3()
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # main()
    option1()