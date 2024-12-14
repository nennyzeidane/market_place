from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuration de la base de données MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'marketplace_universitaire'
app.config['MYSQL_USER'] = 'root'  # Changez selon votre configuration MySQL
app.config['MYSQL_PASSWORD'] = ''  # Changez selon votre configuration MySQL

mysql = MySQL(app)

# Route pour la page d'inscription
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        numero_telephone = request.form['numero_telephone']

        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO Etudiant (Non, Prenom, Email, mot_de_passe, Numero_du_telephone)
                          VALUES (%s, %s, %s, %s, %s)''', (nom, prenom, email, mot_de_passe, numero_telephone))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login'))

    return render_template('signup.html')

# Route pour la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM Etudiant WHERE Email = %s AND mot_de_passe = %s''', (email, mot_de_passe))
        etudiant = cursor.fetchone()

        if etudiant:
            session['etudiant_id'] = etudiant[0]  # Enregistrer le Matricule dans la session
            return redirect(url_for('index'))
        else:
            return "Erreur de connexion. Vérifiez vos informations."

    return render_template('login.html')

# Route pour la page principale des annonces
@app.route('/')
@app.route('/index')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM Annonce''')
    annonces = cursor.fetchall()
    cursor.close()
    return render_template('index.html', annonces=annonces)

# Route pour la page d'ajout d'une annonce
@app.route('/add_announcement', methods=['GET', 'POST'])
def add_announcement():
    if 'etudiant_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        prix = request.form['prix']
        date_publication = request.form['date_publication']
        matricule = session['etudiant_id']  # Récupérer l'ID de l'étudiant connecté

        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO Annonce (titre, description, prix, date_publication, Matricule)
                          VALUES (%s, %s, %s, %s, %s)''', (titre, description, prix, date_publication, matricule))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))

    return render_template('add_announcement.html')

# Route pour afficher les détails d'une annonce
@app.route('/annonce/<int:id_annonce>')
def annonce_detail(id_annonce):
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM Annonce WHERE id_annonce = %s''', (id_annonce,))
    annonce = cursor.fetchone()

    cursor.execute('''SELECT * FROM Photo WHERE id_annonce = %s''', (id_annonce,))
    photos = cursor.fetchall()

    cursor.close()
    return render_template('annonce_detail.html', annonce=annonce, photos=photos)

if __name__ == '__main__':
    app.run(debug=True)
