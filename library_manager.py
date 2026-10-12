import sqlite3

# Checks whether an entry exists in the books table
def entry_exists(cursor, i):
    f = cursor.execute("SELECT EXISTS(SELECT 1 from books WHERE ROWID = ?)", (i,))
    if f.fetchone()[0] == 1:
        return True
    else:
        return False

con = sqlite3.connect("library.db")

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS books(name, author, genre, publication_date)");

print("Welcome to my library manager!")
print("This software is meant to showcase my knowledge of Python and SQL, through the use of the sqlite3 module.")
print("="*20)

while(True):
    print("1 - Display database\n2 - Add entries\n3 - Remove entries\n4 - Update entries\n5 - Search\n6 - Clear database\n0 - Exit")
    print("="*20)
    
    i = input()
    
    match(i):
        case "1":
            print("ID", "Name", "Author", "Genre", "Publication Date", sep=" | ")
            for row in cur.execute("SELECT ROWID, name, author, genre, publication_date FROM books"):
                print(*row, sep=" | ")
                    
        case "2":
            # Operation requires four comma separated fields (name, author, genre, publication date). With exception of the book's name, fields can be left empty.
            print("Enter the book's details as follows:")
            print("name, author, genre, publication date")
            print("e.g. 'Parasite Eve, Hideaki Sena, Horror, 2005-12-01'")
            print("Notes:")
            print("* Enter an empty line to finish.")
            print("* The book's name is required.")
            print("* Publication dates must be entered in YYYY-MM-DD.")
            
            data = []
            
            while(True):
                j = input()
                if len(j) == 0:
                    break
                else:
                    new_book = j.split(", ")

                    if len(new_book) == 4 and new_book[0] != "":
                        data.append(new_book)
                    else:
                        print("Invalid entry, try again.")
                        
            if len(data) == 0:
                print("No entries were added.")
            else:
                cur.executemany("INSERT INTO books VALUES(?, ?, ?, ?)", data)
                con.commit()
                print("Entries added successfully")

            print("Returning to menu...")
            
        case "3":
            print("Enter the book's id.")
            print("Enter an empty line to finish.")

            while(True):
                j = input()

                if len(j) == 0:
                    break
                else:
                    if entry_exists(cur, j):
                        cur.execute("DELETE FROM books WHERE ROWID = ?", (j,))
                        con.commit()
                        print("Entry removed successfully.")
                    else:
                        print("Invalid entry, try again.")
                        
            print("Returning to menu...")
            
        case "4":
            while(True):
                print("Enter the book's id.")
                print("Enter an empty line to finish.")
                
                j = input()

                if len(j) == 0:
                    break
                elif entry_exists(cur, j):
                    print("Enter the column you wish to edit and its new value as such:")
                    print("column, value")

                    while(True):
                        print("Enter an empty line to finish editing this book.")
                        k = input().split(", ")

                        if len(k) == 2 and k[0].lower() in ["name", "author", "genre", "publication_date", "publication date"]:
                            field = k[0].lower()

                            if field == "publication date":
                                field = "publication_date"
                                
                            cur.execute(f"UPDATE books SET {field} = ? WHERE ROWID = ?", (k[1], j))
                            con.commit()
                            print("Book updated successfully")
                        elif len(k[0]) == 0:
                            break
                        else:
                            print("Invalid column, try again.")
                else:
                    print("Invalid entry, try again.")

            print("Returning to menu...")
                    
        case "5":
            print("Filter by:\n1. ID\n2. Name\n3. Author\n4. Genre\n5. Publication Date")
            print("="*20)
            
            j = input()

            match(j):
                case "1":
                    print("Enter the book's id.")
                    k = input()
                    rows = cur.execute("SELECT ROWID, name, author, genre, publication_date FROM books WHERE ROWID = ?", (k,)).fetchall()
                    if len(rows) == 0:
                        print("No results.")
                    else:
                        for row in rows:
                            print(*row, sep=" | ")
                case "2":
                    print("Enter the book's name.")
                    k = input()
                    rows = cur.execute("SELECT ROWID, name, author, genre, publication_date FROM books WHERE name = ?", (k,)).fetchall()
                    if len(rows) == 0:
                        print("No results.")
                    else:
                        for row in rows:
                            print(*row, sep=" | ")
                case "3":
                    print("Enter the book's author.")
                    k = input()
                    rows = cur.execute("SELECT ROWID, name, author, genre, publication_date FROM books WHERE author = ?", (k,)).fetchall()
                    if len(rows) == 0:
                        print("No results.")
                    else:
                        for row in rows:
                            print(*row, sep=" | ")
                case "4":
                    print("Enter the book's genre.")
                    k = input()
                    rows = cur.execute("SELECT ROWID, name, author, genre, publication_date FROM books WHERE genre = ?", (k,)).fetchall()
                    if len(rows) == 0:
                        print("No results.")
                    else:
                        for row in rows:
                            print(*row, sep=" | ")
                case "5":
                    print("-"*20)
                    print("Display:\n1. Books released in this date\n2. Books released before this date\n3. Books released after this date\n4. Books released in this year")
                    print("-"*20)

                    k = input()

                    if k == "4":
                        print("Enter the year (YYYY)")
                        x = input()
                        rows = cur.execute("SELECT ROWID, name, author, genre, publication_date FROM books WHERE strftime('%Y',publication_date) = ?", (x,)).fetchall()
                        
                        if len(rows) == 0:
                            print("No results.")
                        else:
                            for row in rows:
                                print(*row, sep=" | ")
                            
                    elif k in ["1", "2", "3"]:
                        print("Enter the date (YYYY-MM-DD)")
                        x = input()
                        
                        match(k):
                            case "1":
                                rows = cur.execute("SELECT ROWID, name, author, genre, publication_date FROM books WHERE publication_date = ?", (x,)).fetchall()

                                if len(rows) == 0:
                                    print("No results.")
                                else:
                                    for row in rows:
                                        print(*row, sep=" | ")
                            case "2":
                                rows = cur.execute("SELECT ROWID, name, author, genre, publication_date FROM books WHERE publication_date < ?", (x,)).fetchall()

                                if len(rows) == 0:
                                    print("No results.")
                                else:
                                    for row in rows:
                                        print(*row, sep=" | ")
                            case "3":
                                rows = cur.execute("SELECT ROWID, name, author, genre, publication_date FROM books WHERE publication_date > ?", (x,)).fetchall()

                                if len(rows) == 0:
                                    print("No results.")
                                else:
                                    for row in rows:
                                        print(*row, sep=" | ")
                    else:
                        print("Invalid option.")
                case _:
                    print("Invalid option.")
                
        case "6":
            while(True):
                print("Are you certain? Y / N")
                j = input()

                if j.lower() == "y":
                    cur.execute("DELETE FROM books")
                    con.commit()
                    break
                elif j.lower() == "n":
                    break
                else:
                    print("Invalid option.")
                    
            print("Returning to menu...")
            
        case "0":
            print("Exiting the program...")
            con.close()
            break
        
        case _:
            print("Operation not found.")

    print("="*20)
