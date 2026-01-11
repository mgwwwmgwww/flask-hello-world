from flask import Flask, request
import requests
from urllib.parse import urljoin
app = Flask(__name__)

REMOTE_BASE_URL = 'https://mgwww.pythonanywhere.com/static'

@app.route('/<path:filename>')
def get_file(filename):
    remote_url = urljoin(REMOTE_BASE_URL, filename)
    
    try:
        response = requests.get(remote_url, timeout=10)
        
        if response.status_code != 200:
            return f"Error: {response.status_code}", 404
        
        if len(response.content) > 1024:
            return "Error: file too large", 413
        
        try:
            text_content = response.content.decode('utf-8')
        except UnicodeDecodeError:
            return "Error: file is not text file (UTF-8)", 400
        
        return text_content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
        
    except requests.exceptions.Timeout:
        return "Error: Timeout while connecting to remote host", 504
        
    except requests.exceptions.ConnectionError:
        return "Error: cant connect to remote host", 502
        
    except Exception as e:
        return f"Error exception: {str(e)}", 500

@app.route('/')
def index():
    return "Use with /file.txt to get file.txt from remote server"
