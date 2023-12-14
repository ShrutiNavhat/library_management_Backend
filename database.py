from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from marshmallow import Schema, fields
from flask_cors import CORS
from datetime import datetime, date

app = Flask(__name__)
CORS(app)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "navgurukul"
app.config["MYSQL_DB"] = "library_data"

mysql = MySQL(app)


class BookSchema(Schema):
    Book_Id = fields.Integer()
    Title = fields.String()
    Author = fields.String()
    Isbn_No = fields.String()
    Quantity = fields.Integer()
    Publish_date = fields.Date()


user_schema = BookSchema(many=True)


@app.route("/books/data", methods=["GET"])
def get_books():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books")
        all_data = cur.fetchall()
        cur.close()

        data_dicts = [dict(zip(user_schema.fields.keys(), row)) for row in all_data]

        result = user_schema.dump(data_dicts)
        return jsonify({"data": result})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})


@app.route("/books/detail/<id>", methods=["GET"])
def detail_books(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books WHERE Book_Id = %s", (id,))
        book = cur.fetchone()
        cur.close()

        if book:
            book_dict = dict(zip(user_schema.fields.keys(), book))
            return jsonify({"data": book_dict})
        else:
            return jsonify({"message": "Book not found"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})


@app.route("/books/update/<id>", methods=["PUT"])
def update_books(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books WHERE Book_Id = %s", (id,))
        book = cur.fetchone()

        if not book:
            return jsonify({"message": "Book not found"})

        data = request.get_json()

        Book_Id = data.get("Book_Id", book[0])
        Title = data.get("Title", book[1])
        Author = data.get("Author", book[2])
        Isbn_No = data.get("Isbn_No", book[3])
        Quantity = data.get("Quantity", book[4])
        Publish_date = data.get("Publish_date", book[5])

        cur.execute("UPDATE books SET Book_Id=%s, Title=%s, Author=%s, Isbn_No=%s, Quantity=%s, Publish_date=%s WHERE Book_Id=%s",
                    (Book_Id, Title, Author, Isbn_No, Quantity, Publish_date, id))

        mysql.connection.commit()

        cur.execute("SELECT * FROM books WHERE Book_Id = %s", (id,))
        updated_book = cur.fetchone()

        cur.close()

        return jsonify({"data": dict(zip(user_schema.fields.keys(), updated_book))})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})


@app.route("/books/delete/<id>", methods=["DELETE"])
def delete_books(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books WHERE Book_Id = %s", (id,))
        deleted_book = cur.fetchone()

        cur.execute("DELETE FROM books WHERE Book_Id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        if deleted_book:
            return jsonify({"data": dict(zip(user_schema.fields.keys(), deleted_book)),
                            "message": "Book deleted successfully"})
        else:
            return jsonify({"message": "Book not found"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})


@app.route("/books/add", methods=["POST"])
def add_books():
    try:
        data = request.get_json()
        Book_Id = data["Book_Id"]
        Title = data["Title"]
        Author = data["Author"]
        Isbn_No = data["Isbn_No"]
        Quantity = data["Quantity"]
        Publish_date = data.get("Publish_date")
        if Publish_date and isinstance(Publish_date, date):
            Publish_date = Publish_date.strftime("%Y-%m-%d")

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO books(Book_Id, Title, Author, Isbn_No, Quantity,Publish_date) VALUES (%s, %s, %s, %s, %s,%s)",
                    (Book_Id, Title, Author, Isbn_No, Quantity, Publish_date))

        mysql.connection.commit()
        cur.execute("SELECT * FROM books WHERE Book_Id = %s", (Book_Id,))
        inserted_data = cur.fetchone()
        cur.close()

        if inserted_data:
            return jsonify({"data": dict(zip(user_schema.fields.keys(), inserted_data))})
        else:
            return jsonify({"message": "Error inserting data"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})

class MemberSchema(Schema):
    Member_Id = fields.Integer()
    Name = fields.String()
    Phone_No = fields.Integer()


Member_schema = MemberSchema(many=True)


@app.route("/Members/data", methods=["GET"])
def get_members():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Members")
        all_data1 = cur.fetchall()
        cur.close()

        member_dicts = [dict(zip(Member_schema.fields.keys(), row)) for row in all_data1]

        result = Member_schema.dump(member_dicts)
        return jsonify({"data": result})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})


@app.route("/Members/detail/<id>", methods=["GET"])
def detail_members(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Members WHERE Member_Id = %s", (id,))
        member = cur.fetchone()
        cur.close()

        if member:
            member_dict = dict(zip(Member_schema.fields.keys(), member))
            return jsonify({"data": member_dict})
        else:
            return jsonify({"message": "Member not found"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})




@app.route("/Members/delete/<id>", methods=["DELETE"])
def delete_members(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Members WHERE Member_Id = %s", (id,))
        deleted_member = cur.fetchone()

        cur.execute("DELETE FROM Members WHERE Member_Id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        if deleted_member:
            return jsonify({"data": dict(zip(Member_schema.fields.keys(), deleted_member)),
                            "message": "Book deleted successfully"})
        else:
            return jsonify({"message": "Book not found"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})


@app.route("/Members/add", methods=["POST"])
def add_members():
    try:
        data1 = request.get_json()
        Member_Id = data1["Member_Id"]
        Name = data1["Name"]
        Phone_No = data1["Phone_No"]

        
        if Member_Id is not None and str(Member_Id).isdigit():
            Member_Id = int(Member_Id)  
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Members(Member_Id, Name, Phone_No) VALUES (%s, %s, %s)",
                        (Member_Id, Name, Phone_No))

            mysql.connection.commit()
            cur.execute("SELECT * FROM Members WHERE Member_Id = %s", (Member_Id,))
            inserted_data = cur.fetchone()
            cur.close()

            if inserted_data:
                return jsonify({"data": inserted_data})
            else:
                return jsonify({"message": "Error inserting data"})
        else:
            return jsonify({"error": "Invalid Member_Id"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})


class TransactionSchema(Schema):
    Id = fields.Integer()
    Amount_paid = fields.Integer()
    Return_date = fields.Date()
    Issue_date = fields.Date()
    Book_Id=fields.Integer()
    Member_Id=fields.Integer()


transaction_schema = TransactionSchema(many=True)
@app.route("/transactions/data", methods=["GET"])
def get_transaction():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM transactions")
        all_data = cur.fetchall()
        cur.close()

        transaction_dicts = [dict(zip(user_schema.fields.keys(), row)) for row in all_data]

        result = user_schema.dump(transaction_dicts)
        return jsonify({"data": result})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})



@app.route("/transactions/detail/<id>", methods=["GET"])
def detail_transaction(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM transactions WHERE Id = %s", (id,))
        transaction = cur.fetchone()
        cur.close()

        if transaction:
            transaction_dict = dict(zip(user_schema.fields.keys(), transaction))
            return jsonify({"data": transaction_dict})
        else:
            return jsonify({"message": "Book not found"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})



@app.route("/transactions/update/<id>", methods=["PUT"])
def update_transaction(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM transactions WHERE Id = %s", (id,))
        transaction= cur.fetchone()

        if not transaction:
            return jsonify({"message": "Book not found"})

        data = request.get_json()

        Id = data.get("Id", transaction[0])
        Book_Id = data.get("Book_Id", transaction[1])
        Member_Id = data.get("Member_Id", transaction[2])
        Amount_paid = data.get("Amount_paid", transaction[3])
        Return_date = data.get("Return_date", transaction[4])
        Issue_date = data.get("Issue_date", transaction[5])

        cur.execute("UPDATE transactions SET Id=%s, Book_Id=%s, Member_Id=%s, Amount_paid=%s, Return_date=%s, Issue_date=%s WHERE Id=%s",
            (Id, Book_Id, Member_Id, Amount_paid, Return_date, Issue_date, id))
        mysql.connection.commit()

        
        
        cur.execute("SELECT * FROM  transactions WHERE Id = %s", (id,))
        updated_transaction = cur.fetchone()
        
        cur.close()

        return jsonify({"data": dict(zip(user_schema.fields.keys(), updated_transaction))})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})
    

@app.route("/transactions/delete/<id>", methods=["DELETE"])
def delete_transaction(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM transactions WHERE Book_Id = %s", (id,))
        deleted_transaction = cur.fetchone()

        cur.execute("DELETE FROM transactions WHERE Book_Id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        if deleted_transaction:
            return jsonify({"data": dict(zip(user_schema.fields.keys(), deleted_transaction)),
                            "message": "Book deleted successfully"})
        else:
            return jsonify({"message": "Book not found"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})


@app.route("/transactions/add", methods=["POST"])
def add_transaction():
    try:
        transactions_data = request.get_json()

        required_fields = ["Id", "Book_Id", "Member_Id", "Amount_paid", "Return_date", "Issue_date"]
        for field in required_fields:
            if field not in transactions_data:
                return jsonify({"error": f"Field '{field}' is missing from the request data"})

        
        Id = transactions_data["Id"]
        Book_Id= transactions_data["Book_Id"]
        Member_Id = transactions_data["Member_Id"]
        Amount_paid=transactions_data["Amount_paid"]
        Return_date=transactions_data["Return_date"]
        Issue_date=transactions_data["Issue_date"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO transactions(Id, Book_Id, Member_Id,Amount_paid,Return_date,Issue_date) VALUES (%s, %s, %s, %s, %s, %s)",
                    (Id, Book_Id,Member_Id,Amount_paid,Return_date, Issue_date))

        mysql.connection.commit()
        cur.execute("SELECT * FROM transactions WHERE Id = %s", (Id,))
        inserted_data = cur.fetchone()
        cur.close()

        if inserted_data:
            return jsonify({"data": inserted_data})
        else:
            return jsonify({"message": "Error inserting data"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})
    



if __name__ == '__main__':
    app.run(debug=True, port=9090)








