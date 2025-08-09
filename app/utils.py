
def write_message(email : str, message : str):
    with open("log.txt", 'w') as log:
        log.write(f"Notification from email:{email} -> {message}")

