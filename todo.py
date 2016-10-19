import sqlite3
from bottle import route, run, debug, template, request, static_file, error,redirect

import os

# only needed when you run Bottle on mod_wsgi
#from bottle import default_app

DB_FILE = 'todo.sqlite'

@route('/todo')
def todo_list():

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, task,status FROM todo ")
    result = c.fetchall()
    c.close()

    output = template('make_table', rows=result)
    return output


@route('/new', method='GET')
def new_item():

    if request.GET.save:

        new = request.GET.task.strip()
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new, 1))
        new_id = c.lastrowid

        conn.commit()
        c.close()

        #go back to the list
        redirect("/todo")

    else:
        return template('new_task.tpl')



@route('/edit/<no:int>', method='GET')
def edit_item(no):

    if request.GET.save:
        edit = request.GET.task.strip()
        status = request.GET.status.strip()

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id=?", (edit, status, no))
        conn.commit()

        redirect("/todo")
        
    else:
        
        
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id=?", (str(no),))
        cur_data = c.fetchone()
        
        return template('edit_task', old=cur_data, no=no)


@route('/item<item:re:[0-9]+>')
def show_item(item):

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
        result = c.fetchall()
        c.close()

        if not result:
            return 'This item number does not exist!'
        else:
            return 'Task: %s' % result[0]


@route('/help')
def help():

    static_file('help.html', root='.')


@route('/json<json:re:[0-9]+>')
def show_json(json):

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (json,))
    result = c.fetchall()
    c.close()

    if not result:
        return {'task': 'This item number does not exist!'}
    else:
        return {'task': result[0]}


@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

def initDb(fName):
    """ initialize database """
   
    con = sqlite3.connect(fName) # Warning: This file is created in the current directory
    con.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL)")
    con.execute("INSERT INTO todo (task,status) VALUES ('Read A-byte-of-python to get a good introduction into Python',0)")
    con.execute("INSERT INTO todo (task,status) VALUES ('Visit the Python website',1)")
    con.execute("INSERT INTO todo (task,status) VALUES ('Test various editors for and check the syntax highlighting',1)")
    con.execute("INSERT INTO todo (task,status) VALUES ('Choose your favorite WSGI-Framework',0)")
    con.commit()	



if __name__ == "__main__":
	
    if not os.path.exists(DB_FILE):
        initDb(DB_FILE)
    
    debug(True)
    run(reloader=True)
    # remember to remove reloader=True and debug(True) when you move your
    # application from development to a productive environment