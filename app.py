# import required libraries 
from __future__ import print_function 
# # import Image from wand.image module 
# from wand.image import Image # do i need this? 

import os
from dotenv import load_dotenv
import sqlite3
from sqlite3 import Error
from flask import Flask, request, render_template, redirect, session, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

load_dotenv()
app = Flask(__name__)
app.secret_key = 'ewdsdasasdfas'

app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'png']

# Create a function that converts a digital file into binary
def convert_into_binary(file_path):
  print("[INFO] : converting into binary data rn")
  with open(file_path, 'rb') as file:
    binary = file.read()
  return binary

# i do not need this shit 
# def write_to_file(binary_code, file_name):
#   # Convert binary to a proper file and store in memory
#   print("[INFO] : writing to file rn")
#   with open(file_name, 'wb') as file:
#     file.write(binary_code)
#   print(f'Created file with name: {file_name}')

# code above copied from another article

# fuck yeah this function works and writes to file 
def writeTofile(binarydata, filename):
  # Convert binary data to proper format and write it on Hard Disk
  with open(filename, 'wb') as file:
    file.write(binarydata)
  print("[DATA] : Stored blob data into: ", filename, "\n")

def readBlobData(entryID):
  try:
    conn = sqlite3.connect('app.db')
    cur = conn.cursor()
    print("Connected to SQLite to readBlobData")

    sql_fetch_blob_query = """SELECT * from uploads where id = ?"""
    cur.execute(sql_fetch_blob_query, (entryID,))
    record = cur.fetchall()
    for row in record:
      print("[DATA] : row = ", row)
      print("Id = ", row[0])
      photo_binarycode  = row[1]
      dud_file_name = "random file name hereee"

      # write to file???? 
      writeTofile(photo_binarycode, dud_file_name)
    print("[DATA] : Storing employee image and resume on disk \n")
    cur.close()
  except sqlite3.Error as error:
    print("Failed to read blob data from sqlite table", error)
  finally:
    if conn:
        conn.close()


# code below is my attempt 

@app.route('/', methods=['GET', 'POST'])
def upload_file():
  # TypeError: can only concatenate str (not "bytes") to str
  filepathname = "/Users/diane/Desktop/myvmk/Screen Shot 2021-01-11 at 10.46.01 PM.png"
  filename_blob = convert_into_binary(filepathname)
  print("[INFO] : the last 100 characters of blob = ", filename_blob[:100]) 
  try:
    conn = sqlite3.connect('app.db')
    print("Successful connection!")
    cur = conn.cursor()
    insert_file = '''INSERT INTO uploads(file_names)
      VALUES(?)'''
    cur = conn.cursor()
    cur.execute(insert_file, (filename_blob,))
    conn.commit()
    print("[INFO] : the blob for ", filepathname, " is inside uploadfolder") 
    return render_template('success.html')
  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()
    else:
      error = "Please upload a valid file."
  return "your VMK file was supposed to be uploaded. hope it did. "

@app.route('/viewfiles', methods = ['GET', 'POST'])
def see_files():
  try:
    conn = sqlite3.connect('app.db')
    print("Successful connection!")
    cur = conn.cursor()
    # time to retrieve file 
    user_id = 1
    sql_retrieve_file_query = f"""SELECT * FROM uploads WHERE id = ?"""   
    cur.execute(sql_retrieve_file_query, (user_id,))
    record = cur.fetchone()
    record_blob = record[1]
    print("[INFO] : the last 100 of record_blob =  ", record_blob[:100]) 
    
    print("[INFO] : reading blobdata of 1 now")
    readBlobData(1)

  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()
    else:
      error = "how tf did u get here."
  return "lets display your vmk pic here "

