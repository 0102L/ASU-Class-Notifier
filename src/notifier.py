from time import time, sleep
from datetime import datetime
from class_avail import seat_check, class_list, open_sections

def main():
    # Take user input
    dept_code = input("Enter course subject: ")
    course_code = input("Enter course number: ")
    
    # Start timed course check
    print("\nSearching for course sections...")
    sections = class_list(dept_code, course_code)
    if sections != "Error. No response.":
        print("\nFound the following sections: ")
        print("Section\tSeats\tProfessor")
        print(sections)
        start = time()
        while True:
            space_avail = seat_check(dept_code, course_code)
            if space_avail:
                open_courses = open_sections(dept_code, course_code)
                
                print("[" + datetime.now().isoformat(sep=' ', timespec='seconds') + "] " + "Space available for the following sections: ")
                print("Section\tSeats\tProfessor")
                print(open_courses)
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

if __name__ == "__main__":
    main()