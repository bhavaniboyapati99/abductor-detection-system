from threading import Timer
import webbrowser

from app import create_app

app = create_app()

def open_browser():
    chrome_path = "open -a 'Google Chrome' %s"
    webbrowser.get(chrome_path).open("http://127.0.0.1:5001/")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(host="0.0.0.0", port=5001, debug=True)