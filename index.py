#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import cgi
import unicodedata
import codecs
import sys
def force_to_unicode(text):
    "If text is unicode, it is returned as is. If it's str, convert it to Unicode using UTF-8 encoding"
    return text if isinstance(text, unicode) else text.decode('utf-8')
def index(req):
    start = """\
    <!DOCTYPE html>
    <html>
    <title>zad8</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <body>

    <h1>Zadanie 8</h1>
    <div class="container">
	<h1>Naša olympijská história</h1>
	<table class="data-table">
    <thead>
    <tr>
    <th>Meno</th>
    <th>Priezvisko</th>
    <th>Rok</th>
    <th>Miesto</th>
    <th>Typ OH</th>
    <th>Disciplína</th>
    </tr>
    </thead>
    <tbody>
    """
    db = MySQLdb.connect(host="localhost",
                         user="xpruzinsky",
                         passwd="tyrellsux",
                         db="prvadb")
    db.set_character_set('utf8')
    cur = db.cursor()
    body = ""
    try:
        cur.execute("SELECT * FROM osoby JOIN umiestnenia ON osoby.id_person=umiestnenia.id_person JOIN oh ON umiestnenia.id_oh=oh.id_oh")
        results = cur.fetchall()
       	for row in results:
        	body = body + "\n<tr><td>"+str(row[1])+"</td><td>"+str(row[2])+"</td><td>"+str(row[16])+"</td><td>"+str(row[18])+", "+str(row[19])+"</td><td>"+str(row[15])+"</td><td>"+str(row[13])+"</td></tr>"
    except Exception as err:
        body = err
    db.close
    end = """\
    </tbody>
    </table>
    <button type="button" onclick="location.href = './addperson';">Pridanie osoby</button>
    </div>
    </body>
    </html>
    """
    whole = start + body + end
    return whole
def addperson(req):
    start = """\
    <!DOCTYPE html>
    <html>
    <title>zad8</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <body>
    <h1>Zadanie 8</h1>
    <div class="container">
	<h1>Pridanie záznamu</h1>
	<form method="get" action="./addpersondone">
	<p>Meno: <input type="text" name="firstname">
	Priezvisko: <input type="text" name="surname">
	Rok: <input type="text" name="year">
	Typ OH: <input type="text" name="typeOH">
	Disciplína: <input type="text" name="discipline">
	<input type="submit" value="submit"</p>
	</form>
    </div>
    </body>
    </html>
    """
    return start
def addpersondone(req):
    firstname = req.form.getfirst('firstname', '')
    surname = req.form.getfirst('surname', '')
    year = req.form.getfirst('year', '')
    typeOH = req.form.getfirst('typeOH', '')
    discipline = req.form.getfirst('discipline', '')
    
    firstname = cgi.escape(firstname)
    surname = cgi.escape(surname)
    year = cgi.escape(year)
    typeOH = cgi.escape(typeOH)
    discipline = cgi.escape(discipline)
    s = """\
    <!DOCTYPE html>
    <html>
    <title>zad8</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <body>
    <h1>Zadanie 8</h1>
    <div class="container">
	<h1>Výsledok</h1>
	"""
    db = MySQLdb.connect(host="localhost",
                         user="xpruzinsky",
                         passwd="tyrellsux",
                         db="prvadb")
    db.set_character_set('utf8')
    cur = db.cursor()
    try:
        cur.execute("""INSERT INTO osoby(firstname, surname) VALUES (%s, %s)""",(firstname.decode('utf-8'), surname.decode('utf-8')))
        db.commit()
        cur.execute("SELECT LAST_INSERT_ID()")
        db.commit()
        id_person = cur.fetchone()
        cur.execute("""SELECT id_OH FROM oh WHERE year=%s AND type=%s """, (year, typeOH))
        db.commit()
        id_OH = cur.fetchone()
        cur.execute("""INSERT INTO umiestnenia(id_person, id_OH, place, discipline) VALUES (%s, %s, %s, %s)""",(id_person, id_OH , "1", discipline.decode('utf-8')))
        db.commit()
    except Exception as err:
        return err
    db.close
    e = """\
    <p> Záznam bol uložený </p>
    </div>
    </body>
    </html>
    """
    whole = s + e
    return whole
