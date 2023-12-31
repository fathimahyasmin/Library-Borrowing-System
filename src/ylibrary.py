# IMPORT DEPENDENCIES
# --------------------------------------------------------------------------
from datetime import datetime, timedelta
import pyinputplus as pyip
import tabulate
import csv
import os

# LOGIN & REGISTRATION
# --------------------------------------------------------------------------
def registration(memberdbase):
    """Register a new library member.

    Args:
        memberdbase (dict): A dictionary containing member information with member IDs as keys.

    Returns:
        None
    """ 
    while True: 
        # input new member data
        name = pyip.inputStr('\nEnter your username: ')
        name = name.lower()
        email = pyip.inputEmail('Enter your email address: ')
        email = email.lower()
        phone_num = pyip.inputInt('Enter your phone number: ')
        hold = 0
        # initialize a variable to check for duplicates
        duplicate = False 
        # check for duplicates in the member database
        for data in memberdbase.values():
            if data[1].lower() == name:
                print('This username is already registered.')
                duplicate = True
                break
            elif data[2] == phone_num:
                print('This phone number is already registered.')
                duplicate = True
                break
            elif data[3].lower() == email: 
                print('This email is already registered')
                duplicate = True

        if not duplicate:
            # generate a unique member ID
            member_id = generate_id(memberdbase, code='M')
            # create default password based on the member ID
            true_pass = '123456' + member_id[1:]
            data = [member_id, name.capitalize(), phone_num, email, hold]
            memberdbase.update({f'{member_id}': data})
            # append the new member's information to a CSV file
            with open('ylibrary\data\member.csv', mode='a', newline='') as file:
                    writer = csv.writer(file, delimiter = ';')
                    writer.writerow(data)

            clear_screen() 
            # display a registration sucess
            print('\nCONGRATULATION!')
            print('Your registration is successful')
            print(f'>>>  Your member ID is : {member_id}')
            print(f'>>>  Your password is : {true_pass}')

            stay()
            break

def generate_id(memberdbase, code):
    """Generate a unique member ID

    Args:
        memberdbase (dict)
        code (str): A prefix code for the member ID

    Returns:
        str: a unique member ID
    """    
    max_id = 0

    for i in memberdbase.keys():
        num_part = i[1:]
        if num_part.isdigit():
            max_id = max(max_id, int(num_part))
    
    new_id = f'{code.capitalize()}{max_id + 1}'
    return new_id

def admin_login():
    """
    Perform admin login
    """    
    while True:
        true_pass = 'abcdefg'
        password = pyip.inputPassword("Enter your password: ").lower()
        if true_pass.lower() != password:
            print('Invalid password')
            print('Please try again')
        else: 
            identity = 'admin'
            id = None
            return identity, id
        
def member_login(memberdbase):
    """
    Perform member login
    """   
    while True:
        found = False

        member_id = pyip.inputStr("Enter your member ID: ").lower()
        password = pyip.inputPassword("Enter your password: ")
        true_pass = '123456' + member_id[1:]

        for member in memberdbase.values():
            if member[0].lower() == member_id and password == true_pass:
                found = True

        if not found:
            print('Invalid member ID or password')
            print('Please try again')
        else:
            identity = 'member'
            id = member_id.capitalize()
            return identity, id

def log_or_reg(memberdbase):
    while True:
        clear_screen()
        print('-------- WELCOME TO Y-LIBRARY --------')
        log_or_reg = pyip.inputStr('''  
To login, please choose the menu: 
                                
1. Login as member
2. Login as admin
3. New member registration
                               
Enter the number: ''')
        
        if log_or_reg == '1':
            identity, id = member_login(memberdbase)
            return identity, id
        elif log_or_reg == '2':
            identity, id = admin_login()
            return identity, id
        elif log_or_reg == '3':
            registration(memberdbase)

# CLEAR SCREEN 
# --------------------------------------------------------------------------
def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def stay():
    back = pyip.inputYesNo(prompt="\nEnter 'y' or 'yes' to go back to the main menu: ")
    if back == 'yes':
        return
    else:
        print("Invalid input. Please enter 'y' or 'yes'.")

# SHOW DATA & ALL DATABASE
# --------------------------------------------------------------------------

def show(database):
    attributes = []
    header = database['column']

    for id, attribute in database.items():
        if id == 'column':
            pass
        else:
            attributes.append(attribute)
    
    print(tabulate.tabulate(attributes, header, tablefmt='grid'))

def partial_show(part, database):
    header = database['column']
    print('Search result: ')
    print(tabulate.tabulate(part, header, tablefmt='grid'))
    
# MAIN MENUS
# --------------------------------------------------------------------------
# Search()
# --------------------------------------------------------------------------
def search(database):
    while True:
        clear_screen()
        print('---------- BOOK SEARCH ----------')
        searchOpts = pyip.inputInt(lessThan=8, prompt='''
Let's find your book!. 
Here's some searching options:
                           
1.  By Book ID
2.  By Title
3.  By Author
4.  By Category
5.  By ISBN               
6.  See all books
7.  Back to main menu                         
                           
Enter the menu number: ''')
        
        found = False
        attributes = []

        if searchOpts == 1:
            book_id = pyip.inputStr('Enter the book_id: ').lower()
            for id, attribute in database.items():
                if book_id == database[id][0].lower():
                    attributes.append(attribute)
                    found = True
            if not found:
                print(f'Sorry, {book_id.capitalize()} was not found in our database')
            else:
                partial_show(attributes, database)
                stay()
    
        elif searchOpts == 2:
            title = pyip.inputStr('Enter the title: ').lower()
            for id, attribute in database.items():
                if title == database[id][1].lower():
                    attributes.append(attribute)
                    found = True
            if not found:
                print(f'Sorry, {title.title()} was not found in our database')
            else:
                partial_show(attributes, database)
                stay()

        elif searchOpts == 3:
            author = pyip.inputStr('Enter the author name: ').lower()
            for id, attribute in database.items():
                if author == database[id][2].lower():
                    attributes.append(attribute)
                    found = True
            if not found:
                print(f'Sorry, {author.title()} was not found in our database')
            else:
                partial_show(attributes, database)
                stay()

        elif searchOpts == 4:
            category = pyip.inputStr('Enter the category: ').lower()
            for id, attribute in database.items():
                if category == database[id][3].lower():
                    attributes.append(attribute)
                    found = True
            if not found:
                print(f'Sorry, {category} was not found in our database')
            else:
                partial_show(attributes, database)
                stay()

        elif searchOpts == 5:
            isbn = pyip.inputStr('Enter the ISBN number: ')
            for id, attribute in database.items():
                if isbn == database[id][4]:
                    attributes.append(attribute)
                    found = True
            if not found:
                print(f'Sorry, {isbn} was not found in our database')
            else:
                partial_show(attributes, database)

        elif searchOpts == 6:
            show(database)
            stay()

        elif searchOpts == 7:
            break
# Borrow()
# --------------------------------------------------------------------------

def borrow(database, memberdbase, borrowdb, identity, user_id):

    if identity != 'member':
        print('This menu is for member only.')
        stay()
        return
    
    while True:
        clear_screen()
        print('-------- BOOK BORROWING --------')
        print('''
Choose the menu:
1. Borrow Books
2. Read Borrowing Policy
3. Check Borrowing History
4. Exit''')
        sub_choice = pyip.inputInt('Enter the number: ', lessThan=5)

        clear_screen()
             
        if sub_choice == 1:
            print('\nBorrowing Quota Status: ')
            print('-----------------------------')
            # check hold
            hold = memberdbase[user_id][4]
            remain = 3 - hold
    
            if remain == 0:
                print('Sorry, you\'ve reached the borrowing limit')
                print('You can borrow another book next time!')
                print('-----------------------------')
                break
            else:
                print(f'Your available borrowing quota is : {remain}')
                print('-----------------------------')


            while True: 
                book_id = pyip.inputStr('\nEnter the book ID you want to borrow: ').capitalize()
                if book_id not in database:
                    print(f'\n!!! Book ID {book_id} not found in database. !!!')
                else: 
                    #cek stock
                    data = database[book_id]
                    stock = data[6]
                    if stock == 0:
                        print('\nSorry, your book isn\'t available')
                        print(f'The book stock is {stock}')

                    else: 
                        print('\nYey! Your book is available')
                        print(f'The remaining stock is {stock}')

                        confirm_save = pyip.inputYesNo('\nDo you want to continue borrowing? (yes/no)') 
                        if confirm_save == 'yes':
                            data[6] -= 1
                            memberdbase[user_id][4] += 1

                            with open('ylibrary\data\libdata.csv', 'w', newline='') as file:
                                writer = csv.writer(file, delimiter=';')
                                writer.writerows(database.values())

                            with open('ylibrary\data\member.csv', 'w', newline='') as file:
                                writer = csv.writer(file, delimiter=';')
                                writer.writerows(memberdbase.values())

                            borrow_date = datetime.now()
                            return_date = borrow_date + timedelta(days=7)
                            entry_num = generate_id(borrowdb, code='C')

                            cart = [entry_num, user_id, book_id, borrow_date, return_date]

                            with open('ylibrary\data\databorrow.csv', 'a', newline='') as file:
                                writer = csv.writer(file, delimiter = ';')
                                writer.writerow(cart)
                            
                            print('\nYey! Borrowing successful!')
                            print('Check the borrowing status in "Check Borrowing History" menu')
                            stay()
                            break
                        else: 
                            break
        
        elif sub_choice == 2:
            clear_screen()
            with open('ylibrary\libpolicy.txt', 'r') as file:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                
                content = file.read()
                print(content)
                
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            stay()
        elif sub_choice == 3:
            print('-------------------- BORROWING HISTORY --------------------')
            
            data = []
            header = ['Member ID', 'Name', 'Book Title', 'Borrow Date', 'Return Date']

            for j in borrowdb.values():
                if j[1] == user_id:
                    name = memberdbase[j[1]][1]
                    title = database[j[2]][1]
                    borrowdate = j[3][:10]
                    returndate = j[4][:10]
                    compile = [user_id, name, title, borrowdate, returndate]
                    data.append(compile)
            print(tabulate.tabulate(data, header, tablefmt='grid'))
            stay()
        elif sub_choice == 4:
            break     
# --------------------------------------------------------------------------
# DATABASE MANAGEMENT
# --------------------------------------------------------------------------
def database_management(database, memberdbase, identity, borrowdb):

    if identity != 'admin':
        print('This menu is for admin only.')
        stay()
        return
    
    while True: 
        clear_screen()
        print('-------- DATABASE MANAGEMENT SYSTEM --------')
        print('''          
Menu:
1. Search book data
2. Add book data
3. Update book data
4. Delete book data
5. Check member data
6. Update member data
7. Delete member data
8. Check borrowing data            
9. Exit
        ''')
        choice = pyip.inputInt('Enter the number: ', lessThan=10)

        if choice == 1:
            search(database)
        elif choice == 2:
            add(database)
        elif choice == 3:
            update(database)
        elif choice == 4:
            delete(database)
        elif choice == 5:
            search_member(memberdbase)
        elif choice == 6:
            update_member(memberdbase)
        elif choice == 7:
            delete_member(memberdbase)
        elif choice == 8:
            show_borrowdb(borrowdb)
        elif choice == 9:
            break

# Add()
# --------------------------------------------------------------------------
def add(database):
    while True:
        clear_screen()
        print('-------- INPUT DATABASE ---------')
        print('''
Choose the menu:
1. Add Book
2. Exit
        ''')
        addOpts = pyip.inputInt('Enter the number: ', lessThan=3)
        
        if addOpts == 1:
            book_id = generate_id(database, code='B')
            #book_id = pyip.inputStr('Enter book ID: ')
            title = pyip.inputStr('Enter title: ')
            authors = pyip.inputStr('Enter authors: ')
            category = pyip.inputStr('Enter category: ')
            isbn = pyip.inputInt(prompt='Enter ISBN number (13 digit): ')
            publisher = pyip.inputStr('Enter publisher: ')
            stock = pyip.inputInt('Enter stock: ')

            data = [book_id, title.title(), authors.title(), category, isbn, publisher.title(), stock]

            clear_screen()

            save = pyip.inputYesNo("Do you want to save this data? (yes/no): ")
            if save == 'yes':
                with open('ylibrary\data\libdata.csv', mode='a', newline='\n') as file:
                    writer = csv.writer(file, delimiter = ';')
                    writer.writerow(data)
                print("\nThe input was successful.")
                stay()
            else:
                print("\nThe input was not saved.")
                stay()
        
        elif addOpts == 2:
            break

# Update()
# --------------------------------------------------------------------------
def update(database):
    while True:
        clear_screen()
        print('-------- UPDATE DATABASE --------')
        print('''
Choose the menu:
1. Update Book Data
2. Exit
        ''')
        sub_choice = pyip.inputInt('Enter the number: ', lessThan=3)
        if sub_choice == 1:
            while True: 
                book_id = pyip.inputStr('\nEnter the book ID to update: ').capitalize()
                
                if book_id not in database:
                    print(f'Book ID {book_id} not found in database.')
                else: 
                    data = database[book_id]
                    print(tabulate.tabulate([data], headers=database['column'], tablefmt='grid'))
                    break
            
            while True:
                confirm = pyip.inputYesNo("Do you want to continue update? (yes/no): ")

                if confirm == 'no':
                    break
                else: 
                    print('''
Select which data you want to update: 
1. Title
2. Author
3. Category
4. ISBN
5. Publisher
6. Stock
        ''')
                updateOpts = pyip.inputStr('Enter the number: ')
        
                if updateOpts == '1':
                    new = pyip.inputStr('\nEnter new title: ')
                    new = new.title()
                elif updateOpts == '2':
                    new = pyip.inputStr('\nEnter new Author: ')
                    new = new.title()
                elif updateOpts == '3':
                    new = pyip.inputStr('\nEnter new Category: ')
                elif updateOpts == '4':
                    new = pyip.inputInt('\nEnter new ISBN (13 digits): ')
                elif updateOpts == '5':
                    new = pyip.inputStr('\nEnter new Publisher: ')
                    new = new.title()
                elif updateOpts == '6':
                    new = pyip.inputInt('\nEnter new stock: ')
                    
                clear_screen()
                confirm_save = pyip.inputYesNo('Do you want to save this update? (yes/no): ')
                
                if confirm_save == 'yes':
                    data[int(updateOpts)] = new
                    with open('ylibrary\data\libdata.csv', 'w', newline='') as file:
                        writer = csv.writer(file, delimiter=';')
                        writer.writerows(database.values())
                    print('\nChange saved successfully')
                    print(tabulate.tabulate([data], headers=database['column'], tablefmt='grid'))
                    stay()
                    break
                else: 
                    print("\nThe update was not saved.")
                    stay()
                    break
        elif sub_choice == 2:
            break

# delete()
# --------------------------------------------------------------------------
def delete(database):

    while True:
        clear_screen()
        print('-------- DELETE DATABASE --------')
        print('''
Choose the menu:
1. Delete Book Data
2. Exit
        ''')
        sub_choice = pyip.inputInt('Enter the number: ', lessThan=3)
        
        if sub_choice == 1:
            while True: 
                book_id = pyip.inputStr('\nEnter the book ID you want to delete: ').capitalize()
                if book_id not in database:
                    print(f'Book ID {book_id} not found in database.')
                else: 
                    data = database[book_id]
                    print(tabulate.tabulate([data], headers=database['column'], tablefmt='grid'))
                    break
            
            while True:
                confirm = pyip.inputYesNo("Do you want to continue delete? (yes/no): ")
                if confirm == 'yes': 
                    del database[book_id]
                    print('\nData successfully deleted')
                    with open('ylibrary\data\libdata.csv', 'w', newline='') as file:
                        writer = csv.writer(file, delimiter=';')
                        writer.writerows(database.values())
                    stay()
                    break
                else:
                    print("\nDeletion cancelled. No changes were made.")
                    stay()
                    break

        elif sub_choice == 2:
            break

# search_member()
# --------------------------------------------------------------------------
def search_member(memberdbase):
    while True: 
        clear_screen()
        print('---------- MEMBER DATA SEARCH ----------')
        searchOpts = pyip.inputInt(lessThan=4, prompt='''
Search options:                                                          
1.  Search Member ID
2.  Show All
3.  Exit                         
                           
Enter the menu number: ''')
        
        found = False
        attributes = []
        
        if searchOpts == 1:
            user_id = pyip.inputStr('Enter the member id: ').lower()
            for id, attribute in memberdbase.items():
                if user_id == memberdbase[id][0].lower():
                    attributes.append(attribute)
                    found = True

            if not found:
                print(f'{user_id.capitalize()} was not found in database')
            else:
                partial_show(attributes, memberdbase)
                stay()

        elif searchOpts == 2:
            show(memberdbase)
            stay()
        elif searchOpts == 3:
            break

# update_member()
# --------------------------------------------------------------------------
def update_member(memberdbase):

    while True:
        clear_screen()
        print('-------- UPDATE MEMBER DATA --------')
        print('''
Choose the menu:
1. Update Member Data
2. Exit
        ''')
        sub_choice = pyip.inputInt('Enter the number: ', lessThan=3)
        if sub_choice == 1:
            while True: 
                member_id = pyip.inputStr('\nEnter the member ID to update: ').capitalize()
                if member_id not in memberdbase:
                    print(f'Member ID {member_id} not found in database.')
                else: 
                    data = memberdbase[member_id]
                    print(tabulate.tabulate([data], headers=memberdbase['column'], tablefmt='grid'))
                    break
            
            while True:
                confirm = pyip.inputYesNo("Do you want to continue update? (yes/no): ")
                if confirm == 'no':
                    break
                else: 
                    print('''
Select which data you want to update: 
1. Name
2. Phone Number
3. Email
4. Hold
''')
                updateOpts = pyip.inputStr('Enter the number: ')
                
                if updateOpts == '1':
                    new = pyip.inputStr('\nEnter new name: ')
                    new = new.title()
                elif updateOpts == '2':
                    new = pyip.inputInt('\nEnter new phone number: ')  
                elif updateOpts == '3':
                    new = pyip.inputEmail('\nEnter new email: ')
                elif updateOpts == '4':
                    new = pyip.inputInt('\nEnter new hold status: ')
        
                confirm_save = pyip.inputYesNo('Do you want to save this update? (yes/no): ')

                if confirm_save == 'yes':
                    data[int(updateOpts)] = new
                    with open('ylibrary\data\member.csv', 'w', newline='') as file:
                        writer = csv.writer(file, delimiter=';')
                        writer.writerows(memberdbase.values())
                    print('Change saved successfully')
                    print(tabulate.tabulate([data], headers=memberdbase['column'], tablefmt='grid'))
                    stay()
                    break
                elif confirm_save == 'no': 
                    print("The input was not saved.")
                    stay()
                    break
        elif sub_choice == 2:
            break

# delete_member()
# --------------------------------------------------------------------------
def delete_member(memberdbase):
    while True:
        clear_screen()
        print('-------- DELETE MEMBER DATA --------')
        print('''
Choose the menu:
1. Delete Member Data
2. Exit
        ''')
        sub_choice = pyip.inputInt('Enter the number: ', lessThan=3)
        
        if sub_choice == 1:
            while True: 
                member_id = pyip.inputStr('Enter the member ID you want to delete: ').capitalize()
                if member_id not in memberdbase:
                    print(f'Member ID {member_id} not found in database.')
                else: 
                    data = memberdbase[member_id]
                    print(tabulate.tabulate([data], headers=memberdbase['column'], tablefmt='grid'))
                    break

            while True:
                confirm = pyip.inputYesNo("Do you want to continue delete? (yes/no): ")
                if confirm == 'yes': 
                    del memberdbase[member_id]
                    print('Data successfully deleted')
                    with open('ylibrary\data\member.csv', 'w', newline='') as file:
                        writer = csv.writer(file, delimiter=';')
                        writer.writerows(memberdbase.values())
                    stay()
                    break
                else:
                    print("Deletion cancelled. No changes were made.")
                    stay()
                    break

        elif sub_choice == 2:
            break

# show_borrowdb()
# --------------------------------------------------------------------------
def show_borrowdb(borrowdb):
    while True:
        clear_screen()
        print('---------- BORROWING HISTORY ----------')
        searchOpts = pyip.inputInt(lessThan=8, prompt='''
                                                             
1.  Search by member id
2.  Show all
3.  Exit                         
                           
Enter the menu number: ''')
        
        found = False
        attributes = []

        if searchOpts == 1:
            member_id = pyip.inputStr('Enter the member id: ').lower()
            for id, attribute in borrowdb.items():
                if member_id == borrowdb[id][1].lower():
                    attributes.append(attribute)
                    found = True
            if not found:
                print(f'Sorry, {member_id.capitalize()} was not found')
            else:
                partial_show(attributes, borrowdb)
                stay()
        elif searchOpts == 2:
            show(borrowdb)
            stay()
        elif searchOpts == 3:
            break