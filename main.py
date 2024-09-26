import os, json
import grabber, scrape, process

def prompt(prompt_str: str, choices: list[str], error_message: str):
    while True:
        choice = input(prompt_str)

        if choice not in choices:
            print(error_message)
            continue

        return choice

def prompt_type(prompt_str: str, choices_type: type, error_message: str):
    while True:
        choice = input(prompt_str)
        
        try: return choices_type(choice)
        except: print(error_message)

def write_token(token: str):
    with open("token", "w") as f:
        f.write(token)

def set_token():
    while True:
        print("Token options")
        print("1. Input token manually\n2. Get token from Discord App (token never leaves device)\n3. Go back")
        choice = prompt("> ", ["1", "2", "3"], "ERROR: Please select a valid option")
        print()

        match int(choice):
            case 1:
                write_token(input("Input your token > "))
                print("Wrote token to `./token`\n")

                break
            
            case 2:
                tokens = grabber.get_tokens()
                
                print(f"Found {len(tokens)} tokens:")
                
                if not tokens:
                    break

                for i, token in enumerate(tokens):
                    print(f"{i + 1}. {token[:6]}{len(token[6:-6]) // 2 * '*'}{token[-6:]}")

                print("\nDo you want to check the validity of found tokens?")
                choice = prompt("Y or n > ", ["Y", "n"], "ERROR: Please select a valid option")
                print()
                
                if choice == "Y":
                    print(f"Checking {len(tokens)} tokens:")

                    for i, token in enumerate(tokens.copy()):
                        print(f"{i + 1}. {token[:6]}{len(token[6:-6]) // 2 * '*'}{token[-6:]}: ", end = "")
                                
                        valid = grabber.is_valid(token)

                        if valid:
                            print(f"Valid! Username is \"{valid['username']}\".")

                        
                        else:
                            tokens.pop(i)
                            print("Invalid. Removed from list.")

                    print()
                
                print("Please choose a token to use...")

                for i, token in enumerate(tokens):
                    print(f"{i + 1}. {token[:6]}{len(token[6:-6]) // 2 * '*'}{token[-6:]}")

                print(f"{i + 2}. Go back")

                choice = int(prompt("> ", [str(i + 1) for i in range(len(tokens) + 1)], "ERROR: Please select a valid option"))

                if choice == i + 2:
                    print()
                    break

                write_token(tokens[choice - 1])
                print(f"Wrote token #{choice} to `./token`\n")

                break

            case 3:
                break

def do_scrape():
    print("Scraping options")
    print("Enter the output file name (`.json` will be appended).")
    file_name = prompt_type("> ", str, "ERROR: Please select a valid option") + ".json"
    print()

    print("Enter Discord channel ID to scrape from.")
    channel_id = int(prompt_type("> ", int, "ERROR: Please select a valid option"))
    print()

    print("Enter number of messages to scrape.")
    number_messages = int(prompt_type("> ", int, "ERROR: Please select a valid option"))
    print()
    
    with open("token", "r") as f:
        token = f.read()

    print(f"Scraping {number_messages} messages from {channel_id}.")

    data = scrape.scrape(token, channel_id, number_messages, lambda x, y: print(f"Done with loop {x + 1} of {y}", end = "\r"))

    if not os.path.exists("output/scraper"):
        os.makedirs("output/scraper")

    with open(f"output/scraper/{file_name}", "w") as f:
        json.dump(data, f, indent = 4)

    print(f"\n\nDone! Saved output to \"output/scraper/{file_name}\"\n")

def do_process():
    print("Processing options")
    print("Enter the input file name (`.json` will be appended).")
    input_file = prompt_type("> ", str, "ERROR: Please select a valid option") + ".json"
    print()

    print("Enter the output file name (`.json` will be appended).")
    output_file = prompt_type("> ", str, "ERROR: Please select a valid option") + ".json"
    print()

    print("Update UTC timestamps to local timezone human readable?")
    update_timestamps = prompt("Y or n > ", ["Y", "n"], "ERROR: Please select a valid option") == "Y"
    print()

    print("Replace ID mentions with usernames?")
    update_mentions = prompt("Y or n > ", ["Y", "n"], "ERROR: Please select a valid option") == "Y"
    print()

    processor = process.Processor(input_file, output_file)
    processor.read()

    if update_timestamps:
        processor.replace_timestamp()

    if update_mentions:
        processor.replace_mentions()

    if update_timestamps or update_mentions:
        processor.save()

    print(f"Updated {int(update_timestamps) + int(update_mentions)} things.\n")

print("Discord Message Scraper v2 by BWP09\n")

while True:
    print("Options\n1. Set token\n2. Scrape messages\n3. Process scraped messages\n4. Exit")
    choice = prompt("> ", ["1", "2", "3", "4"], "ERROR: Please select a valid option")
    print()

    match int(choice):
        case 1:
            set_token()
        
        case 2:
            do_scrape()

        case 3:
            do_process()
        
        case 4:
            break