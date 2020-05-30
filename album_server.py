from bottle import route,request
from bottle import run
from bottle import HTTPError

import find_albums


# Get запрос---------------------------------------
@route("/albums/<artist>")
def albums(artist):
    albums_list = find_albums.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Количество альбомов {} равно {} <br>".format(artist,len(album_names))
        result += "<br>".join(album_names)
    return result
# Post запрос------------------------------------------------------
@route("/albums", method='POST')
def albums():
    new_album=find_albums.Album(
        year=request.forms.get("year"),
        artist= request.forms.get("artist"),
        genre=request.forms.get("genre"),
        album=request.forms.get("album")
    )

    try:
        year = int(new_album.year)
    except ValueError:
        textErrYear = "Указан некорректный год альбома:  {}".format(str(new_album.year))
        return HTTPError(400, textErrYear)

    try:
        assert (find_albums.find_new(new_album.artist, new_album.album))
    except AssertionError:
        textErrNewAlbum = "Альбом {} исполнителя {} в базе уже существует! ".format(new_album.album, new_album.artist)
        return HTTPError(409, textErrNewAlbum)
    else:
        session = find_albums.connect_db()
        session.add(new_album)
        session.commit()
        print("Альбом успешно сохранен")


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)


# Строка для тестирования неверно введен год
# http -f POST http://localhost:8080/albums artist="New Artist1" genre="Rock" album="SuperClass" year="2kk00"
# добавить новый альбом
# http -f POST http://localhost:8080/albums artist="New Artist1" genre="Rock" album="SuperClass" year="2000"
#  добавить существующий  альбом
# http -f POST http://localhost:8080/albums artist="New Artist1" genre="Rock" album="SuperClass" year="2000"