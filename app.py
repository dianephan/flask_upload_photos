import os
from dotenv import load_dotenv
import sqlite3
from sqlite3 import Error
from flask import Flask, request, render_template, redirect, session, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

load_dotenv()
app = Flask(__name__)
app.secret_key = 'dsfdsd'

app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'png']

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']

def convertToBinaryData(filename):
    print("[INF0] : about to convert to binary data")
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

# dont need to do this if i dont have to??
def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def readBlobData(entryID):
    try:
        conn = sqlite3.connect('app.db')
        cur = conn.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from uploads where id = ?"""
        cur.execute(sql_fetch_blob_query, (entryID,))
        record = cur.fetchall()
        for row in record:
            print("Id = ", row[0])
            photo  = row[1]
        print("Storing employee image and resume on disk \n")


        # photoPath = "E:\pynative\Python\photos\db_data\\" + name + ".jpg"
        photoPath = "/Users/diane/Desktop/pythonfiles" + photo + ".jpg"
        print("[INFO] : photopath = ", photoPath)
        writeTofile(photo, photoPath)
        cur.close()
    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if conn:
            conn.close()




@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # print("[INFO] : reading blobdata for 3")
    # readBlobData(3)
    # TypeError: can only concatenate str (not "bytes") to str

    print("[INFO] : reading blobdata for 4")
    readBlobData(4)
    # TypeError: can only concatenate str (not "bytes") to str
    # filepathname = "/Users/diane/Desktop/myvmk/Screen Shot 2021-01-11 at 10.46.01 PM.png"
        
    # filename_blob = convertToBinaryData(filepathname)
    # # filename_blob = convertToBinaryData(f.filename)
    # print("[INFO] : the blob = ", filename_blob) 
    # try:
    #     conn = sqlite3.connect('app.db')
    #     print("Successful connection!")
    #     cur = conn.cursor()
    #     insert_file = '''INSERT INTO uploads(file_names)
    #         VALUES(?)'''
    #     cur = conn.cursor()
    #     cur.execute(insert_file, (filename_blob,))
    #     conn.commit()
    #     print("[INFO] : the blob for ", filepathname, " is inside uploadfolder") 
    #     return render_template('success.html')
    # except Error as e:
    #     print(e)
    # finally:
    #     if conn:
    #         conn.close()
    #     else:
    #         error = "Please upload a valid file."
    # return render_template('index.html', error=error)

    # use the line below for end project 
#    return render_template('index.html')




@app.route('/uploader', methods = ['GET', 'POST'])
def submitted_file():
   if request.method == 'POST':
      f = request.files['file']
    #   print("[INFO] : the file = ", ) 

      if f and allowed_file(f.filename):  
        # f.save(secure_filename(f.filename))       # do not do this otherwise it saves on your proj directory
        print("[INFO] : f.filename = ", f.filename)
        # if you pass f.filename into converBD, it doesnt work bc u need the entire path name

        filename_blob = convertToBinaryData(f.filename)
        try:
          conn = sqlite3.connect('app.db')
          print("Successful connection!")
          cur = conn.cursor()
          insert_file = '''INSERT INTO uploads(file_names)
              VALUES(?)'''
          cur = conn.cursor()
          cur.execute(insert_file, (filename_blob,))
          conn.commit()
          print("[INFO] : the blob for ", f.filename, " is inside uploadfolder") 
          return render_template('success.html')
        except Error as e:
          print(e)
        finally:
          if conn:
            conn.close()
      else:
        error = "Please upload a valid file."
        return render_template('index.html', error=error)

# probably wont do this if i don't have to 
@app.route('/uploads', methods=['GET', 'POST'])
def show_files():
   return render_template('uploads.html')

