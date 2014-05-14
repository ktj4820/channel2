def startswith(value, s):
    """
    returns if value starts with s, used for menu highlighting
    """

    if not value: return False
    return value.find(s) == 0
