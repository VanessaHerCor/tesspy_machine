from flask import Flask, request

app_example = Flask(__name__)

@app_example.route('/')
def home():
    return  {"llave": "valor", "numero": 123, "booleano": True}
            #"<h1 style='color:cyan;'> Hola Mundo </h1>" \
            #"<h2> desde Flask </h2>" \

@app_example.route('/greetings/<string:name>')
def greetings(name):
    return f"<h1 style='color:green;'> Hola, {name} </h1>"

pets =  [{"name": "Firulais", "species": "dog"},
            {"name": "Michifu", "species": "cat"},
            {"name": "Mich", "species": "cat"},
            {"name": "Nemo", "species": "fish"}]

@app_example.route('/pets')
def get_pets():
    species = request.args.get("species")
    print(f"species = {species}")
    ans = pets
    if species != None and species != "":
        ans = list(filter(lambda p: p["species"] == species, pets))
    print(f"ans = {ans}")
    return ans


if __name__ == '__main__':
    app_example.run(debug=True,port=8001)