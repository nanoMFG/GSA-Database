from grdb.server import app

if __name__ == "__main__":
    application = app.create_app()
    host = application.config['HOST']
    port = application.config['PORT']
    application.run(debug=True, host=host, port=port)
