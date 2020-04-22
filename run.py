from film_aggregator import app, imdb_dbase


if __name__ == '__main__':
    imdb_dbase.create_table("C:\\Users\\GORNOSTAEVKK\\PycharmProjects\\onkin\\film_aggregator\\imdb")
    app.run(debug=True)

