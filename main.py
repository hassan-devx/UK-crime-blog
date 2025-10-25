from app import create_app, db

app = create_app()

if __name__ == '__main__':
   if __name__ == "__main__":
    from flask_migrate import upgrade
    upgrade()
    app.run(host="0.0.0.0", port=8080)
    app.run(debug=True)

