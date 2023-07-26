import sqlite3


class Database:
    #SELECT * FROM doc_fts WHERE doc_fts MATCH 'user_1?@gmail' ORDER BY rank;
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        print('self.conn = sqlite3.connect(db)')
        self.cur = self.conn.cursor()
        print('self.cur = self.conn.cursor()')

    def search_doc_by_text(self, text, section):
        self.cur.execute(
            "SELECT rowid,snippet(doc_fts, 0,'<b>', '</b>','...',64),snippet(doc_fts, 1,'<b>', '</b>','...',64) FROM doc_fts WHERE section LIKE ? AND doc_fts MATCH ?",
            (section, text))
        # SELECT snippet(text_table_fts4) AS text FROM text_table_fts4 WHERE text MATCH :pattern || '*')
        # ORDER BY bm25(text)
        # SELECT * FROM posts WHERE posts MATCH 'learn SQLite';
        # SELECT highlight(posts, 0, '<b>', '</b>') title, highlight(posts, 1, '<b>', '</b>') body FROM posts WHERE posts MATCH 'SQLite' ORDER BY rank;

        return self.cur.fetchall()

    def search_doc_without_text(self, section):
        self.cur.execute(
            "SELECT rowid,name, non_format_text FROM doc_fts WHERE section LIKE ? ",
            (section, ))
        return self.cur.fetchall()

    def search_doc_by_id(self, rowid):
        self.cur.execute("SELECT format_text FROM doc WHERE id  = ? ", (rowid,))
        return self.cur.fetchall()

    def get_sections(self):
        self.cur.execute("SELECT DISTINCT section FROM Section;")
        return self.cur.fetchall()

    def add_new_doc(self, data):
        """
        Add a new book into the books table
        :param self:
        :param data: list with book details
        :return: book id
        """
        sql = '''INSERT OR REPLACE INTO doc (
                    name, 
                    section,
                    non_format_text,
                    format_text,
                    links
                    ) VALUES (?,?,?,?,?)'''
        self.cur.execute(sql, data)
        self.conn.commit()
        print('self.conn.commit()')
        return self.cur.lastrowid

    def add_section(self, data):
        """
        Add a new book into the books table
        :param self:
        :param data: list with book details
        :return: book id
        """
        #INSERT INTO test.Content (title) VALUES ('1st Street') ON DUPLICATE KEY UPDATE title='2st Street';
        sql = '''INSERT OR REPLACE INTO Section(section)
              VALUES(?) '''
        self.cur.execute(sql, (data,))
        self.conn.commit()
        print('self.conn.commit()')
        return self.cur.lastrowid
    # ---------------------------------

    def delete_doc(self, book_id):
        """
        Delete a book by book id
        :param self:
        :param book_id: id of book
        :return error or deleted
        """
        try:
            sql = 'DELETE FROM books WHERE book_id=?'
            self.cur.execute(sql, (book_id,))
            self.conn.commit()
            return "deleted"
        except:
            return "error"

    def view_doc_list(self):
        """
        Query all book rows in the books table
        :param self:
        :return: all book list
        """
        self.cur.execute("SELECT * FROM books WHERE status = ? or status = ?", ('available', 'issued'))
        return self.cur.fetchall()

    def issue_book(self, data):
        """
        Issue a new book into the issued_book table
        :param self:
        :param data: list with issue book details
        :return: book id
        """
        sql = '''INSERT INTO issued_book (book_id,issued_to,issued_on,expired_on)
            VALUES(?,?,?,?) '''
        self.cur.execute(sql, data)
        self.conn.commit()
        return self.cur.lastrowid

    def delete_issued_book(self):
        try:
            sql = 'DELETE FROM issued_book'
            self.cur.execute(sql)
            self.conn.commit()
            return "deleted"
        except:
            return "error"

    def all_issued_book_id(self):
        """
        Query all issued book id in the issued book table
        :param self:
        :return: all issued book id list
        """
        self.cur.execute("SELECT book_id FROM issued_book WHERE is_miscellaneous = ?", (0,))
        return self.cur.fetchall()

    def return_book(self, book_id):
        """
        Return the book which issued by id
        :param self:
        :param book_id: id of book
        :return error or returned
        """
        try:
            sql = 'DELETE FROM issued_book WHERE book_id=?'
            self.cur.execute(sql, (book_id,))
            self.conn.commit()
            return "returned"
        except:
            return "error"

    def update_book_status(self, book_id, status):
        """
        update book status of a book
        :param conn:
        :param book_id: id of book
        :param status: status of book
        :return:
        """
        sql = '''UPDATE books SET status = ? WHERE book_id = ?'''
        self.cur.execute(sql, (status, book_id,))
        self.conn.commit()

    def select_book_status(self, book_id):
        """
        Query book status by book_id
        :param self:
        :param book_id:
        :return: book status
        """
        self.cur.execute("SELECT status FROM books WHERE book_id=?", (book_id,))
        return self.cur.fetchone()

    def select_issued_book_det(self, book_id):
        self.cur.execute("SELECT * FROM issued_book WHERE book_id=?", (book_id,))
        return self.cur.fetchone()

    def select_book_detail(self, book_id):
        self.cur.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
        return self.cur.fetchone()

    def all_available_book(self):
        sql = "SELECT book_id, book_name, book_author, book_edition, book_price FROM books WHERE status = 'available'"
        return (sql, self.conn)

    def all_issued_book(self):
        sql = "SELECT book_id, book_name, book_author, book_edition, book_price FROM books WHERE status = 'issued'"
        return (sql, self.conn)

    def all_books(self):
        sql = "SELECT book_id, book_name, book_author, book_edition, book_price FROM books WHERE status = 'available' or status = 'issued'"
        return (sql, self.conn)

    def fine_detail(self):
        sql = "SELECT * FROM fine_details"
        return (sql, self.conn)

    def move_to_miscellaneous(self, id):
        sql = '''UPDATE issued_book SET is_miscellaneous = ? WHERE book_id = ?'''
        self.cur.execute(sql, (1, id,))
        self.conn.commit()

    def update_book_details(self, data):
        sql = '''UPDATE books SET book_id = ?,book_name = ?,book_author = ?,book_edition = ?,book_price = ?,date_of_purchase = ? WHERE book_id = ?'''
        self.cur.execute(sql, data)
        self.conn.commit()

    def save_fine_detail(self, data):
        sql = '''INSERT INTO fine_details(book_id,student_id,issued_on,returned_date,total_fine,no_of_day)
            VALUES(?,?,?,?,?,?)'''
        self.cur.execute(sql, data)
        self.conn.commit()
        return self.cur.lastrowid
