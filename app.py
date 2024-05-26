from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
'''
Student DB FastAPI App written by 
Paul E. Coke (c)2024

'''
try:
    mydb = mysql.connector.connect(

        host="localhost",
        user="root",
        password="",
        database="studentDB"

    )
      
except Exception as e: 
    print(e)


#Instanatiate FastAPI app
app = FastAPI() 


#Define Pydantic student model 
class Student(BaseModel):
    name: str
    age: int


#CREATE STUDENT
@app.post("/students")
async def create_student(student:Student): 
    cursor = mydb.cursor()
    sql = "INSERT INTO students(name, age) VALUES(%s, %s)"
    val = (student.name, student.age)
    cursor.execute(sql, val)
    mydb.commit()
    return {"Message": "Record successfully added"}


#READ ALL STUDENTS
@app.get("/students")
async def allstudents(): 
    cursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM students"
    cursor.execute(sql)
    students = cursor.fetchall()
    return students


#READ STUDENT
@app.get("/students/{student_id}")
async def read_student(student_id: int): 
    cursor = mydb.cursor() 
    cursor.execute("SELECT * FROM students WHERE id = %s",(student_id,))
    student = cursor.fetchone()
    if not student: 
        raise Exception('Error: Student not found')
    return student


#UPDATE STUDENT
@app.put("/students/{student_id}")
async def update_student(student_id: int, student:Student): 
    cursor = mydb.cursor() 
    sql = "UPDATE students SET name=%s, age=%s WHERE id = %s"
    val = (student.name, student.age, student_id)
    cursor.execute(sql, val)
    mydb.commit()
    return {"message": "Record successfully updated"}


#DELETE STUDENT
@app.delete("/students/{student_id}")
async def delete_student(student_id: int): 
    cursor = mydb.cursor() 
    cursor.execute("DELETE FROM students WHERE id = %s",(student_id,))
    mydb.commit()
    return {"message": "Record successfully deleted"}




    




