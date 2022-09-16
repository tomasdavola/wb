from wb import create_app

app = create_app()
import sqlite3

#
# add_column('site.db', 'user', 'date', 'DateTime')
if __name__== '__main__':

  app.run(host="0.0.0.0", debug=False)




