from Website import create_app

app = create_app()
app.app_context().push()

if __name__ == "__main__":
    app.run(debug=False, port=8080)