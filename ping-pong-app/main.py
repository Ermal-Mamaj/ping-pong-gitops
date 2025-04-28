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
        # Using psycopg2.connect() inside a context manager for automatic cleanup
        with psycopg2.connect(
            host="postgres",  # Make sure this matches the actual DB service name
            database="postgres",  # Ensure this is the correct database name
            user="postgres",  # Ensure this is the correct user
            password="postgres",  # Ensure this is the correct password
            connect_timeout=3  # Set a timeout to avoid long waits
        ) as conn:
            return jsonify({"status": "healthy"}), 200  # Connection successful, return 200 OK
    except psycopg2.OperationalError as e:
        # Handle specific database connection errors
        print(f"Error connecting to the database: {e}")
        return jsonify({"status": "unhealthy", "error": "Database connection failed", "details": str(e)}), 500
    except Exception as e:
        # Handle other errors
        print(f"Error: {e}")
        return jsonify({"status": "unhealthy", "error": "Unknown error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
