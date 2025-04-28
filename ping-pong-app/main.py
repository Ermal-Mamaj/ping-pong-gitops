from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

pong_count = 0

@app.route('/ping', methods=['GET'])
def ping():
    global pong_count
    pong_count += 1
    return f"Ping / Pongs: {pong_count}"

@app.route('/pongs', methods=['GET'])
def get_pongs():
    return jsonify({"pongs": pong_count})

@app.route('/healthz')
def healthz():
    try:
        with psycopg2.connect(
            host="postgres",  
            database="postgres",  
            user="postgres",  
            password="postgres", 
            connect_timeout=3 
        ) as conn:
            return jsonify({"status": "healthy"}), 200  
    except psycopg2.OperationalError as e:
       
        print(f"Error connecting to the database: {e}")
        return jsonify({"status": "unhealthy", "error": "Database connection failed", "details": str(e)}), 500
    except Exception as e:
       
        print(f"Error: {e}")
        return jsonify({"status": "unhealthy", "error": "Unknown error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
