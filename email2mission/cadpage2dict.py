EXAMPLE_EMAIL = '''
                CALL: CAR CRASH
                PLACE: Wendys
                ADDR: 123 HUCKLEBERRY LN
                CITY: BREMERTON
                ID: Some identifier for this alarm (123456) 
                PRI: Internal priority level (HIGH, A, 123, etc)
                DATE: CAD date (10/17/2012)
                TIME: CAD time 
                MAP: Map page or number: 123-456: Page 5, etc::
                UNIT: UNIT1, UNIT2, etc::
                INFO: Notes, data: other information
                '''
REQUIRED_KEYS = {'CALL', 'PLACE', 'ADDR', 'CITY', 'INFO'}

def parse_email(email: str):
    """Converts email body of value pairs into dictionary 

    Args:
        email (str): email body in the Cadpage format
    """
    result = email.splitlines()
    result = [line for line in result if ':' in line]
    result = [line.split(':') for line in result]
    # the fanciness with the join is in case the message has colons in it
    result = {line[0].strip(): ':'.join(line[1:]).strip() for line in result}
    # make sure the required keys exist so the format is correct
    assert REQUIRED_KEYS.issubset(result.keys())
    return result


if __name__ == "__main__":
    print(parse_email(EXAMPLE_EMAIL))