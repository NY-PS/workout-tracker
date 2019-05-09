from workout_tracker import create_app

app = create_app()
current_app = app


if __name__ == '__main__':
    app.run()
