from flask import Flask, request, jsonify

app = Flask(__name__)
movies = []


#Server ON
@app.route('/')
def index():
    return "API CINEGUATEMALA", 200

# Ruta para agregar una nueva película
@app.route('/new-movie', methods=['POST'])
def registrar_pelicula():

    new_movie = request.get_json()
    
    #Verifico que no tenga un json valido
    if not new_movie:
        return jsonify({'msg': 'Solicitud JSON no válida'}), 400

    #Se obtienen los datos de la pelicula
    movie_id = new_movie.get("movieId")
    name = new_movie.get("name")
    genre = new_movie.get("genre")
    
    #Se verifica que los datos no esten vacios
    if movie_id is None or name is None or genre is None:
        return jsonify({'msg': 'Faltan Datos De la Película'}), 400

    #Se recorre la lista de peliculas para verificar que no exista el id o el nombre
    for movie in movies:
        if movie["movieId"] == movie_id:
            return jsonify({'msg': 'El movieId ya está en uso'}), 400
        if movie["name"] == name:
            return jsonify({'msg': 'El nombre de la película ya está registrado'}), 400
    
    #Se agrega la pelicula a la lista
    movies.append(new_movie)
    return jsonify({'msg': 'Película creada con éxito'}), 201


# Ruta para buscar x Genero
@app.route('/all-movies-by-genre/<string:genre>', methods=['GET'])
def buscar_por_genero(genre):

    #Se recorre la lista de peliculas para verificar que exista el genero
    genero_peliculas = [pelicula for pelicula in movies if pelicula["genre"] == genre]
    
    #Se verifica si la pelicula existe en el genero
    if not genero_peliculas:
        return jsonify({'msg': f'No se encontraron películas para el genero {genre}'}), 404

    #Si no, se retorna la lista de peliculas con el genero buscado
    return jsonify(genero_peliculas), 200

# Ruta para actualizar pelicula x Id
@app.route('/update-movie/<int:movie_id>', methods=['PUT'])
def actualizar_pelicula(movie_id):

    pelicula_actualizada = request.get_json()
    
    #Verifico que no tenga un json valido
    if not pelicula_actualizada:
        return jsonify({'msg': 'Solicitud JSON no valida'}), 400

    #Se recorre la lista de peliculas
    for inicio, pelicula in enumerate(movies):
        #Se verifica que el id de la pelicula exista
        if pelicula['movieId'] == movie_id:
            movies[inicio] = pelicula_actualizada
            return jsonify({'msg': 'Pelicula actualizada con exito'}), 200

    #Se retorna un mensaje de error si no se encuentra el ID la pelicula
    return jsonify({'msg': 'No se encontro una pelicula con el movieId proporcionado'}), 404


# Método que inicia la aplicación
if __name__ == '__main__':
    app.run(debug=True)
