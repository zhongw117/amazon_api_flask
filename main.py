import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from werkzeug import generate_password_hash, check_password_hash
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# @app.route('/add', methods=['POST'])
# def add_goods():
# 	try:
# 		_json = request.json
# 		_goods_title = _json['goods_title']
# 		_goods_title_ch = _json['goods_title_ch']
# 		_goods_category = _json['goods_category']
#         _goods_id = _json['goods_id']
# 		_goods_saleprice = _json['goods_saleprice']
# 		_goods_oriprice = _json['goods_oriprice']
#         _discount_perc = _json['discount_perc']
# 		_ends_time = _json['ends_time']
		
# 		# validate the received values
# 		if _goods_category and _goods_title and request.method == 'POST':
# 			#do not save password as a plain text
# 			# _hashed_password = generate_password_hash(_password)
# 			# save edits
# 			sql = "INSERT IGNORE INTO amazontodaydeal (goods_id, goods_title, goods_title_ch, goods_category, goods_saleprice, goods_oriprice,\
#             discount_perc, ends_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
# 			data = (_goods_id, _goods_title, _goods_title_ch, _goods_category, _goods_saleprice, _goods_oriprice, _discount_perc, _ends_time)
# 			conn = mysql.connect()
# 			cursor = conn.cursor()
# 			cursor.execute(sql, data)
# 			conn.commit()
# 			resp = jsonify('User added successfully!')
# 			resp.status_code = 200
# 			return resp
# 		else:
# 			return not_found()
# 	except Exception as e:
# 		print(e)
# 	finally:
# 		cursor.close() 
# 		conn.close()
		
@app.route('/goods')
def goods():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM amazontodaydeal")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/goods/<id>')
def single_goods(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM amazontodaydeal WHERE id=%s", id)
        # print(id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

# @app.route('/update', methods=['POST'])
# def update_user():
# 	try:
# 		_json = request.json
# 		_id = _json['id']
# 		_name = _json['name']
# 		_email = _json['email']
# 		_password = _json['pwd']		
# 		# validate the received values
# 		if _name and _email and _password and _id and request.method == 'POST':
# 			#do not save password as a plain text
# 			_hashed_password = generate_password_hash(_password)
# 			# save edits
# 			sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
# 			data = (_name, _email, _hashed_password, _id,)
# 			conn = mysql.connect()
# 			cursor = conn.cursor()
# 			cursor.execute(sql, data)
# 			conn.commit()
# 			resp = jsonify('User updated successfully!')
# 			resp.status_code = 200
# 			return resp
# 		else:
# 			return not_found()
# 	except Exception as e:
# 		print(e)
# 	finally:
# 		cursor.close() 
# 		conn.close()
		
@app.route('/delete/<id>')
def delete_item(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM amazontodaydeal WHERE id=%s", (id,))
		conn.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
		
if __name__ == "__main__":
    app.run()