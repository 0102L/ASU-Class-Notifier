from time import time, sleep
from datetime import datetime
from class_search import ASUSearch

def main():
    """
    Main def that runs the script.
    """
    # Take user input
    dept_code = input("Enter course subject: ")
    course_code = input("Enter course number: ")
    
    api = ASUSearch(dept_code, course_code)
    # Start timed course check
    print("\nSearching for course sections...")
    sections = api.__str__()
    if sections != "Error":
        print("\nFound the following sections: ")
        print("Section\tSeats\tInstructor")
        print(sections)
        start = time()
        # Loop until an open section is found.
        while True:
            # Create a new search to refresh data
            api = ASUSearch(dept_code, course_code)
            space_avail = api.any_space()
            if space_avail:
                open_sections = api.open_sections()
                print("[" + datetime.now().isoformat(sep=' ', timespec='seconds') + "] " + "Space available for the following section(s): ")
                print("Section\tSeats\tInstructor")
                for section in open_sections:
                    print(section)
                input("Press any key to exit.")
                break
            else:
                print("[" + datetime.now().isoformat(sep=' ', timespec='seconds') + "] " + "Sorry, all sections are full.")
            
            # Runs check exactly once every 60s regardless of execution time
            t = int(60 - ((time() - start) % 60))
            while t >= 0:
                mins, secs = divmod(t, 60)
                timer = '{:02d}:{:02d}'.format(int(mins), int(secs))
                print("Next update in: " + timer, end="\r")
                sleep(1)
                t -= 1
    else:
        input("\nThere are currently no classes offered that match your criteria.\nPress any key to exit.")


# Used to run script
if __name__ == "__main__":
    main()