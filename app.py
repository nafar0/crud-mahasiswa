from flask import Flask, request, flash, url_for, render_template
from werkzeug.utils import redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'XXXXXXXXXX' # Secret Key
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'USERNAME'
app.config['MYSQL_PASSWORD'] = 'PASSWORD'
app.config['MYSQL_DB'] = 'NAMA_DATABASE'

mysql = MySQL(app)


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', data=data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data berhasil ditambahkan")
        nim = request.form['nim']
        nama = request.form['nama']
        semester = request.form['semester']
        jurusan = request.form['jurusan']
        alamat = request.form['alamat']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO data (nim, nama, semester, jurusan, alamat) VALUES (%s, %s, %s, %s, %s)", (nim, nama, semester, jurusan, alamat))
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<int:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Data berhasil di hapus")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM data WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))



@app.route('/update/', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        nim = request.form['nim']
        nama = request.form['nama']
        semester = request.form['semester']
        jurusan = request.form['jurusan']
        alamat = request.form['alamat']

        cur = mysql.connection.cursor()
        cur.execute("""UPDATE data SET nim=%s, nama=%s, semester=%s, jurusan=%s, alamat=%s WHERE id=%s
        """, (nim, nama, semester, jurusan, alamat, id_data))
        mysql.connection.commit()
        flash("Data berhasil di ubah")
        return redirect(url_for('Index'))




if __name__ == "__main__":
    app.run(debug=True)
