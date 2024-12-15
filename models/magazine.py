from database.connection import Connection

class Magazine:
    def __init__(self, id, name):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        
        self._id = id  # Directly assign id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = value
    def articles(self):
        query = "SELECT * FROM articles WHERE magazine_id = ?;"
        return Connection.get_db_connection().execute(query, (self.id,)).fetchall()

    def contributors(self):
        query = """
            SELECT DISTINCT authors.* 
            FROM authors 
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?;
        """
        return Connection.get_db_connection().execute(query, (self.id,)).fetchall()

    def article_titles(self):
        query = "SELECT title FROM articles WHERE magazine_id = ?;"
        titles = Connection.get_db_connection().execute(query, (self.id,)).fetchall()
        return [title[0] for title in titles] if titles else None

    def contributing_authors(self):
        query = """
            SELECT authors.*, COUNT(articles.id) AS article_count 
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2;
        """
        return Connection.get_db_connection().execute(query, (self.id,)).fetchall()
