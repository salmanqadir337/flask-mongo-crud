from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["school_management_system"]
student_collection = db["students"]

@app.route('/')
def index():
    studnets = student_collection.find()
    return render_template('index.html', studnets_list=studnets)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']
    student_collection.insert_one({'name': name, 'email': email})
    return redirect('/')

@app.route('/delete/<std_id>')
def delete_student(std_id):
    student_collection.delete_one({'_id': ObjectId(std_id)})
    return redirect('/')

@app.route('/edit/<std_id>')
def edit_student(std_id):
    student = student_collection.find_one({'_id':ObjectId(std_id)})
    return render_template('edit.html',student=student)

@app.route('/update/<std_id>', methods=['POST'])
def update_user(std_id):
    name = request.form['name']
    email = request.form['email']
    student_collection.update_one(
        {'_id': ObjectId(std_id)},
        {'$set': {'name': name, 'email': email}}
    )
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
