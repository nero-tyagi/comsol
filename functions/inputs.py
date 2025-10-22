# Input functions

def getYOrN(question):
    while True:
        answer = input(question).lower()
        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            return False
        else:
            print("Please enter yes or no.")