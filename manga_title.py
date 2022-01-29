import time
from database import db


class MangaTitle:
    def __init__(self, title_name):
        self.decomposed_name = title_name.split()
        self.chapter_number = self.decomposed_name[len(self.decomposed_name) - 1]
        self.chapter = self.decomposed_name[len(self.decomposed_name) - 2]

        result = ''
        for word in self.decomposed_name:
            if word in (self.chapter, self.chapter_number):
                continue
            else:
                result += word
                result += ' '

        self.manga_name = result.strip()

        if not db.already_in_db(self.manga_name):
            db.insert_title(self.manga_name,
                            float(self.chapter_number),
                            float(self.chapter_number) + 1)

    def is_the_latest(self) -> bool:
        next_volume = db.get_next_chapter_number(self.manga_name)
        current_volume = float(self.chapter_number)

        if current_volume == next_volume:
            return True
        else:
            return False

    def check_for_latest(self):
        if self.is_the_latest():
            db.update_chapter_number(float(self.chapter_number), self.manga_name)
        else:
            print('not the latest!')
            time.sleep(10)
            self.check_for_latest()
