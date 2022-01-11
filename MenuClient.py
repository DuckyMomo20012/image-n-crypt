import sys
def mainMenu():
    print("___MENU___")
    print("1. Login")
    print("2. Register")
    print("3. Quit")
    option = int(input("Enter your option: "))
    while option != 0:
        try : 
            if option == 1:
                #login()
                print("Logged in successfully")
                optionLogin()
            elif option == 2:
                #register()
                print("Sign Up Success")
            elif option == 3:
                sys.exit()
            else:
                print("Invalid choise. Enter 1 - 3")
                mainMenu()
        except ValueError:
            print("Invalid choise. Enter 1 - 3")

def optionLogin():
    print("____HOME___")
    print("1. List image")
    print("2. Upload image")
    print("3. Dowload all images")
    print("4. Get User information")
    print("5. Logout")
    print("6. Back")
    option = int(input("Enter your option: "))
    while option != 0:
        try : 
            if option == 1:
                #listImage()
                optionInOptionLogin()
            elif option == 2:
                print()
                optionLogin()
            elif option == 3:
                print()
                optionLogin()
            elif option == 4:
                #getUserInformation()
                print ()
                optionLogin()
            elif option == 5:
                #logout()
                print("Logout successful")
            elif option == 6:
                mainMenu()
            else:
                print("Invalid choise. Enter 1 - 4")
                optionLogin()
        except ValueError:
            print("Invalid choise. Enter 1 - 4")    

def back():
    enter = int(input("Can you back(0.No - 1.Yes)? " ))
    while enter <2:
        if enter == 0:
           sys.exit()
        elif enter == 1:
            optionLogin()

def optionInOptionLogin():
    print("____IMAGE PROCESING___")
    print("1. Dowload image")
    print("2. Delete images")
    print("3. Back")
    option = int(input("Enter your option: "))
    while option != 0:
        try : 
            if option == 1:
                print()
                back()
            elif option == 2:
                #deleteImage()
                back()
            elif option == 3:
                optionLogin()
            else:
                print("Invalid choise. Enter 1 - 3")
                optionInOptionLogin()
        except ValueError:
            print("Invalid choise. Enter 1 - 3")    

if __name__== "__main__":
    mainMenu()