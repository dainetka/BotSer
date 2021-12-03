from Website import create_app

app = create_app()
app.app_context().push()

if __name__ == "__main__":
    app.run(host='185.154.14.236', pro)