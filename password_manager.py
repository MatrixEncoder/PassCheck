import json

class PasswordVault:
    def __init__(self, filename='passwords.txt'):
        self.filename = filename
        self.load_my_passwords()

    def load_my_passwords(self):
        try:
            with open(self.filename, 'r') as file:
                self.saved_passwords = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.saved_passwords = {}

    def save_my_passwords(self):
        with open(self.filename, 'w') as file:
            json.dump(self.saved_passwords, file)

    def check_password_quality(self, user_password):
        length_criteria = len(user_password) >= 8
        upper_criteria = any(char.isupper() for char in user_password)
        lower_criteria = any(char.islower() for char in user_password)
        number_criteria = any(char.isdigit() for char in user_password)
        special_criteria = any(char in '!@#$%^&*()_+' for char in user_password)

        password_strength = sum([length_criteria, upper_criteria, lower_criteria, number_criteria, special_criteria])

        if password_strength == 5:
            return 'Strong'
        elif password_strength >= 3:
            return 'Moderate'
        else:
            return 'Weak'

    def store_password(self, account_name, user_password):
        if account_name in self.saved_passwords:
            print('Duplicate service password is not allowed. Please use a different service name.')
            return
        password_strength = self.check_password_quality(user_password)
        print(f'Password strength for {account_name}: {password_strength}')
        if password_strength == 'Weak':
            user_confirmation = input('Password is weak. Are you sure you want to add it? (yes/no): ').strip().lower()
            if user_confirmation != 'yes':
                print('Password not added.')
                return
        self.saved_passwords[account_name] = user_password
        self.save_my_passwords()
        print('Password added.')

    def retrieve_password(self, account_name):
        return self.saved_passwords.get(account_name, 'Service not found.')

    def remove_password(self, account_name):
        if account_name in self.saved_passwords:
            del self.saved_passwords[account_name]
            self.save_my_passwords()
            return 'PASSWORD SUCCESSFULLY DELETED!'
        else:
            return 'Service not found.'

if __name__ == '__main__':
    manager = PasswordVault()
    while True:
        user_choice = int(input('Choose an action: 1-add, 2-get, 3-delete, 0-exit: '))
        if user_choice == 1:
            account_name = input('Enter the service name: ')
            user_password = input('Enter the password: ')
            manager.store_password(account_name, user_password)
        elif user_choice == 2:
            account_name = input('Enter the service name: ')
            print('Password:', manager.retrieve_password(account_name))
        elif user_choice == 3:
            account_name = input('Enter the service name: ')
            result = manager.remove_password(account_name)
            if result is None:
                print('Password deleted successfully!')
            else:
                print(result)
        elif user_choice == 0:
            print('THANK YOU FOR USING MY TOOL :)')
            print('It was a pleasure helping you manage your passwords!')
            break
