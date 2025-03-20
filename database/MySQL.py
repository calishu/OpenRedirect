import mysql.connector

class MySQL:
    def __init__(self, host, user, password, database):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def setup(self):
        cursor = self.db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS redirects (route VARCHAR(255), url VARCHAR(255))")
        self.db.commit()

    def create_redirect(self, route: str, url: str):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO redirects (route, url) VALUES (%s, %s)", (route, url))
        self.db.commit()

    def remove_redirect(self, route: str):
        cursor = self.db.cursor()
        cursor.execute(f"DELETE FROM redirects WHERE route = %s", route)
        self.db.commit()

    def edit_redirect(self, to: str, route: str = None, url: str = None):
        cursor = self.db.cursor()
        if route is None: cursor.execute("UPDATE redirects SET url = %s WHERE url = %s", (to, url))
        elif url is None: cursor.execute("UPDATE redirects SET route = %s WHERE route = %s", (to, route))
        self.db.commit()

    def get_url(self, route: str) -> str:
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT url FROM redirects WHERE route = %s", (route,))
            return cursor.fetchone()[0]
        except: return "404"