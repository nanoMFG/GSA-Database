import server

if __name__ == "__main__":
    app = server.create_app()
    app.run(debug=True)
