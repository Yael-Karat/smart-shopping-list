import sys

print(sys.path)

from app import app

if __name__ == "__main__":
    app.run(debug=True)
