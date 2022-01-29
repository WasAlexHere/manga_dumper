import sqlite3

db_connect = sqlite3.connect('manga_list.db')

c = db_connect.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS manga_list (
            title text,
            last_chapter integer,
            next_chapter integer
            )""")


def already_in_db(manga_name):
    duplicates = c.execute("SELECT COUNT(title) "
                           "FROM manga_list "
                           "WHERE title = ?", (manga_name,))
    number = duplicates.fetchone()
    if number[0] > 0:
        print('already in db')
        return True
    else:
        print('not in db')
        return False


def insert_title(manga_name, last_chapter, next_chapter):
    c.execute("INSERT INTO manga_list VALUES (?, ?, ?)",
              (manga_name, last_chapter, next_chapter))
    db_connect.commit()


def get_next_chapter_number(manga_name):
    c.execute("SELECT next_chapter FROM manga_list WHERE title = ?",
              (manga_name,))
    number = c.fetchone()
    return int(number[0])


def update_chapter_number(chapter_number, manga_name):
    new = chapter_number + 1
    c.execute("UPDATE manga_list "
              "SET last_chapter = ? , next_chapter = ? "
              "WHERE title=?", (chapter_number, new, manga_name))
    db_connect.commit()

# db_connect.commit()
# db_connect.close()
