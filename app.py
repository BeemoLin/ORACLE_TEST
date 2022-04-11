# -*- coding: utf-8 -*-
import pytz
import time
import datetime
import cx_Oracle
from flask import Flask, request, flash, url_for, redirect, render_template
from sqlalchemy import null

timezone = pytz.timezone('Asia/Taipei')

app = Flask(__name__)

## Oracle 連線
cx_Oracle.init_oracle_client(lib_dir="/opt/oracle/instantclient_21_5") # init Oracle instant client 位置
connection = cx_Oracle.connect('Group3', 'Group33', cx_Oracle.makedsn('140.117.69.58', 1521, 'orcl')) # 連線資訊
cursor = connection.cursor()

app.config['SECRET_KEY'] = "group3"

@app.route('/')
def show_all():
    sql = 'SELECT * FROM ROOM'
    cursor.execute(sql)
    room_row = cursor.fetchall()
    room_data = []
    for i in room_row:
        room = {
            'rid': i[0],
            'r_type': i[1],
            'capacity': i[2],
            'manadept': i[3],
        }
        room_data.append(room)
    return render_template('./show_all.html', rooms = room_data )

@app.route('/booking/<string:room_id>', methods = ['GET', 'POST'])
def booking(room_id):
    sql = 'SELECT r.USEID, r.ROOMID, d.DNAME, e.NAME, r.STARTTIME, r.ENDTIME, r.PURPOSE FROM RBOOK r LEFT JOIN EMPLOYEE e ON r.EMPLOYEEID=e.EID LEFT JOIN DEPARTMENT d ON e.DID=d.DID WHERE r.ROOMID = \'{}\''.format(room_id)
    cursor.execute(sql)
    rbook_row = cursor.fetchall()
    rbook_data = []
    for i in rbook_row:
        rbook = {
            'useid': i[0],
            'roomid': i[1],
            'employee': '{}: {}'.format(i[2], i[3]),
            'starttime': i[4],
            'endtime': i[5],
            'purpose': i[6],
        }
        rbook_data.append(rbook)
        
    sql = 'SELECT * FROM EMPLOYEE'
    cursor.execute(sql)
    employee_row = cursor.fetchall()
    employee_data = []
    for i in employee_row:
        employee = {
            'id': i[0],
            'name': i[1],
        }
        employee_data.append(employee)

    if request.method == 'POST':
        if not room_id or not request.form['starttime'] or not request.form['endtime'] or not request.form['employee']:

            flash('請填寫完整表單', 'error')
        else:
            starttime = time.strftime('%Y-%m-%d %H:%M', time.strptime(request.form['starttime'], '%Y-%m-%dT%H:%M'))
            endtime = time.strftime('%Y-%m-%d %H:%M', time.strptime(request.form['endtime'], '%Y-%m-%dT%H:%M'))
            cursor.prepare("INSERT INTO RBOOK (roomid, employeeid, starttime, endtime, purpose) VALUES (:roomid, :employeeid, TO_TIMESTAMP(:starttime, 'YYYY-MM-DD HH24:MI'), TO_TIMESTAMP(:endtime, 'YYYY-MM-DD HH24:MI'), :purpose)")
            cursor.execute(None, {'roomid': room_id, 'employeeid':request.form['employee'], 'starttime':starttime, 'endtime':endtime, 'purpose':request.form['purpose'] })
            connection.commit()
            return redirect(url_for('booking', room_id=room_id))
    return render_template('new.html', rid = room_id, employees=employee_data, rbooks=rbook_data)

@app.route('/edit_booking', methods = ['GET', 'POST'])
def edit_booking():
    if request.method == 'GET':
        use_id = request.args.get('use_id')

        sql = 'SELECT r.USEID, r.ROOMID, d.DNAME, e.NAME, r.STARTTIME, r.ENDTIME, r.PURPOSE FROM RBOOK r LEFT JOIN EMPLOYEE e ON r.EMPLOYEEID=e.EID LEFT JOIN DEPARTMENT d ON e.DID=d.DID WHERE r.USEID = \'{}\''.format(use_id)
        cursor.execute(sql)
        i = cursor.fetchone()
        rbook = {
            'useid': i[0],
            'roomid': i[1],
            'employee': '{}: {}'.format(i[2], i[3]),
            'starttime': i[4].strftime('%Y-%m-%dT%H:%M'),
            'endtime': i[5].strftime('%Y-%m-%dT%H:%M'),
            'purpose': str(i[6]).strip(),
        }

    if request.method == 'POST':
        if not request.form['roomid'] or not request.form['useid'] or not request.form['starttime'] or not request.form['endtime'] or not request.form['purpose']:

            flash('請填寫完整表單', 'error')
        else:
            starttime = time.strftime('%Y-%m-%d %H:%M', time.strptime(request.form['starttime'], '%Y-%m-%dT%H:%M'))
            endtime = time.strftime('%Y-%m-%d %H:%M', time.strptime(request.form['endtime'], '%Y-%m-%dT%H:%M'))
            sql = "UPDATE RBOOK SET STARTTIME=TO_TIMESTAMP(\'{}\', 'YYYY-MM-DD HH24:MI'), ENDTIME=TO_TIMESTAMP(\'{}\', 'YYYY-MM-DD HH24:MI'), PURPOSE=\'{}\' WHERE USEID=TO_NUMBER({})".format(starttime, endtime, request.form['purpose'], request.form['useid'])
            cursor.execute(sql)
            connection.commit()
            return redirect(url_for('booking', room_id=request.form['roomid']))
    return render_template('edit.html', rbook=rbook)

@app.route('/del_booking', methods = ['GET', 'POST'])
def del_booking():
    use_id = request.args.get('use_id')
    room_id = request.args.get('room_id')

    sql = 'DELETE FROM RBOOK r WHERE r.USEID=\'{}\''.format(use_id)
    cursor.execute(sql)
    connection.commit()

    return redirect(url_for('booking', room_id=room_id))

@app.route('/new', methods = ['GET', 'POST'])
def new():
    pass
'''
    if request.method == 'POST':
        if not request.form['rid'] or not request.form['r_type'] or not request.form['capacity']:
            flash('Please enter all the fields', 'error')
        else:
            r = Room(
                rid=request.form['rid'],
                r_type=request.form['r_type'],
                capacity=int(request.form['capacity']),
                manadept=request.form['manadept']
            )
         
            db.session.add(r)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')
'''
if __name__ == '__main__':
    #conStr.cursor()
    app.run(debug = True, host="0.0.0.0")
