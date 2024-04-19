from server import app

# This is the production entry point for our app.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)