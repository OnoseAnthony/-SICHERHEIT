from hashlib import sha256
import secrets
import string


def get_initial_password():
    """
    This function generates an initial password that is used for the second level hash in the get_password_digest function

    """

    return ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(6))




def get_hexdigest(salt, r_string):
    """

    This function takes in two required parameters: A salt and a random string.
    The function returns an sha256 concatenated string result.
    The concatenated string is first encoded using the utf-8 encoding scheme.

    """

    return sha256((salt + r_string).encode('utf-8')).hexdigest()




def get_password_digest(random_pass_string, application_service):
        """

        This function takes in two required parameters: A random_pass_string and the name of the appliaction for which the user is creating a password for, i.e application_service.
        The random_pass_string is generated from the secrets module.
        The function returns a joined string resulting from three levels of sha256 hashing by making calls to the get_hexdigest function.
        The first level hash returns the first 20 string elements. N:B This is solely based on the developers preference as the whole or any slice of the string can be used.
        The second level hash returns the last 20 string elements. N:B This is solely based on the developers preference as the whole or any slice of the string can be used.
        The third level hash returns all the string elements. N:B This is solely based on the developers preference as any slice of the string can be used.

        """

        # First level hash using the string from secrets module as the salt parameter and the application_service as the random_pass_string
        first_level_hash = get_hexdigest(random_pass_string, application_service)[:20]

        # Second level hash using the string result from first_level_hash as the salt parameter and the result from the get_initial_password as the random_pass_string
        second_level_hash = get_hexdigest(first_level_hash, get_initial_password())[-20:]

        # third level hash using the string result from second_level_hash as the salt parameter and the result from the developer name as the random_pass_string
        third_level_hash = get_hexdigest(second_level_hash, 'Rukkii123##')

        hash_digest = ''.join((first_level_hash, second_level_hash, third_level_hash))

        final_hash_digest = hash_digest[:74]

        return final_hash_digest



def generate_secure_password(application_service_name, length):
    """

    This function is the entry point to the other functions in the password_generator.py file.
    The function takes in two required parameter: the application_service name and the length of the password.
    However if a user does not enter a password then we'll set it to length of 12.
    It makes calls to the get_password_digest function and uses the result to make the final secure password.

    """

    # Get the password digest in hexadecimal and convert into decimal
    password_digest = get_password_digest(secrets.token_hex(16)[:8], application_service_name)
    password_digest_to_decimal = int(password_digest, 16)


    # Create an Alphabet of valid password characters which can be accepted in a password
    # Lowercase_letters, Uppercase_letters, numbers, symbols
    alphabet = ('abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789!@#$%^&*()-_')
    alphabet_length = len(alphabet)

    # We'll store the final password characters in the secure_password list as long as the kength of the list is not more than the length of the required password
    secure_password = []

    while len(secure_password) < length:
        password_digest_to_decimal, i = divmod(password_digest_to_decimal, alphabet_length)
        secure_password.append(alphabet[i])

    return ''.join(secure_password)




def get_passphrase_digest(random_pass_string, username, email_address):
        """

        This function takes in two required parameters: A random_pass_string, username and an emailAddress.
        The function returns a joined string resulting from three levels of sha256 hashing by making calls to the get_hexdigest function.
        The first level hash returns the first 20 string elements. N:B This is solely based on the developers preference as the whole or any slice of the string can be used.
        The second level hash returns the last 20 string elements. N:B This is solely based on the developers preference as the whole or any slice of the string can be used.
        The third level hash returns all the string elements. N:B This is solely based on the developers preference as any slice of the string can be used.

        """

        # First level hash using the string from secrets module as the salt parameter and the application_service as the random_pass_string
        first_level_hash = get_hexdigest(random_pass_string, 'Rukkii123##')[:20]

        # Second level hash using the string result from first_level_hash as the salt parameter and the username parameter as the random_pass_string
        second_level_hash = get_hexdigest(first_level_hash, username)[-20:]

        # third level hash using the string result from second_level_hash as the salt parameter and the email_address parameter
        third_level_hash = get_hexdigest(second_level_hash, email_address)

        hash_digest = ''.join((first_level_hash, second_level_hash, third_level_hash))

        final_hash_digest = hash_digest[:74]

        return final_hash_digest



def register_passphrase(username, emailAddress, length):
    """

    This function creates a passphrase for a first time user

    """

    # Get the password digest in hexadecimal and convert into decimal
    password_digest = get_passphrase_digest(secrets.token_hex(16)[:8], username, emailAddress)
    password_digest_to_decimal = int(password_digest, 16)


    # Create an Alphabet of valid password characters which can be accepted in a password
    # Lowercase_letters, Uppercase_letters, numbers, symbols
    alphabet = ('abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789!@#$%^&*()-_')
    alphabet_length = len(alphabet)

    # We'll store the final password characters in the secure_password list as long as the kength of the list is not more than the length of the required password
    secure_password = []

    while len(secure_password) < length:
        password_digest_to_decimal, i = divmod(password_digest_to_decimal, alphabet_length)
        secure_password.append(alphabet[i])

    return ''.join(secure_password)
