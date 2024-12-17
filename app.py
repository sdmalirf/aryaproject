from flask import Flask, render_template, request
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import pandas as pd
import os

app = Flask(__name__)


# Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
STORY_FILE = os.path.join(DATASETS_DIR, "stories.xlsx")
TRAINING_FILE = os.path.join(DATASETS_DIR, "Bullying Dataset neww.xlsx")

# Path ke file Excel
NEW_EXCEL_FILE = STORY_FILE

@app.route("/")
def home():
    return render_template("home.html")

# Preprocessing fungsi
def preprocess_text(text):
    # Lowercasing
    text = text.lower()
    
    # Tokenisasi kata
    words = word_tokenize(text)
    
    # Menghapus stopwords
    stop_words = set(stopwords.words('indonesian'))
    words = [word for word in words if word not in stop_words]
    
    # Gabungkan kembali kata menjadi string
    return ' '.join(words)

# Membaca dataset dari file Excel (Pastikan path file benar)
data = pd.read_excel(TRAINING_FILE)  # Ganti path jika perlu

# Preprocessing pada kolom "Text"
data['Cleaned Text'] = data['Text'].apply(preprocess_text)

# Feature extraction menggunakan TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['Cleaned Text'])
y = data['Label']

# Melatih model Logistic Regression
model = LogisticRegression()
model.fit(X, y)

# Route untuk halaman utama
@app.route("/tell_my_story", methods=["GET", "POST"])
def tell_my_story():
    if request.method == "POST":
        # Ambil input dari form
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        publish = request.form.get("publish")  # Ambil nilai checkbox 'publish'
        
        # Tentukan apakah cerita akan diterbitkan berdasarkan checkbox 'publish'
        will_publish = publish == "yes"  # Jika checkbox dicentang, akan menghasilkan 'on'

        # Pastikan folder 'datasets' ada, jika belum, buat folder
        if not os.path.exists('datasets'):
            os.makedirs('datasets')

        # Jika file Excel belum ada, buat file baru dengan kolom yang sesuai
        if not os.path.exists(NEW_EXCEL_FILE):
            df = pd.DataFrame(columns=['Name', 'Email', 'Story', 'Category_1', 'Category_1_Prob', 'Category_2', 'Category_2_Prob', 'Publish'])
            df.to_excel(NEW_EXCEL_FILE, index=False)

        # Preprocess cerita dan prediksi kategori
        cleaned_message = preprocess_text(message)
        vectorized_message = vectorizer.transform([cleaned_message])
        predicted_probabilities = model.predict_proba(vectorized_message)
        
        # Mendapatkan dua kategori dengan probabilitas tertinggi
        top_2_indices = predicted_probabilities[0].argsort()[-2:][::-1]
        top_2_categories = [
            (model.classes_[index], round(predicted_probabilities[0][index], 3))  # Round to 1 decimal place
            for index in top_2_indices
        ]

        # Menyimpan data ke dalam file Excel baru
        df = pd.read_excel(NEW_EXCEL_FILE)
        new_data = {
            'Name': name,
            'Email': email,
            'Story': message,
            'Category_1': top_2_categories[0][0],
            'Category_1_Prob': top_2_categories[0][1],
            'Category_2': top_2_categories[1][0],
            'Category_2_Prob': top_2_categories[1][1],
            'Publish': will_publish  # Menyimpan status apakah cerita bisa dipublikasikan
        }
        new_data_df = pd.DataFrame([new_data])

        # Menambahkan data baru ke DataFrame menggunakan pd.concat
        df = pd.concat([df, new_data_df], ignore_index=True)

        # Menyimpan kembali ke file Excel
        df.to_excel(NEW_EXCEL_FILE, index=False)

        # Tampilkan hasil prediksi di halaman result
        return render_template(
            "result.html",
            name=name,
            email=email,
            message=message,
            categories=top_2_categories,
            will_publish=will_publish  # Kirim status publish ke template
        )
    
    return render_template("index.html")

@app.route('/modul', methods=['GET', 'POST'])
def modul():
    if request.method == 'POST':
        pass
    return render_template('modul.html') 

@app.route('/story')
def story():
    # Membaca data dari file Excel
    df = pd.read_excel(NEW_EXCEL_FILE)
    
    # Memfilter cerita yang memiliki status Publish True
    filtered_stories = df[df['Publish'] == True]
    
    # Mengubah DataFrame menjadi list of dictionaries
    stories = filtered_stories.to_dict(orient="records")
    
    # Mengirim data stories yang sudah difilter ke template
    return render_template("story.html", stories=stories)

@app.route('/modulfisik1', methods=['GET', 'POST'])
def modulf1():
    return render_template('modulfisik1.html') 

@app.route('/modulfisik2', methods=['GET', 'POST'])
def modulf2():
    return render_template('modulfisik2.html')

@app.route('/modulfisik3', methods=['GET', 'POST'])
def modulf3():
    return render_template('modulfisik3.html')

@app.route('/modulfisik4', methods=['GET', 'POST'])
def modulf4():
    return render_template('modulfisik4.html')

@app.route('/modulverbal1', methods=['GET', 'POST'])
def modulv1():
    return render_template('modulverbal1.html') 

@app.route('/modulverbal2', methods=['GET', 'POST'])
def modulv2():
    return render_template('modulverbal2.html') 

@app.route('/modulverbal3', methods=['GET', 'POST'])
def modulv3():
    return render_template('modulverbal3.html') 

@app.route('/modulverbal4', methods=['GET', 'POST'])
def modulv4():
    return render_template('modulverbal4.html') 

@app.route('/modulcyber1', methods=['GET', 'POST'])
def modulc1():
    return render_template('modulcyber1.html') 

@app.route('/modulcyber2', methods=['GET', 'POST'])
def modulc2():
    return render_template('modulcyber2.html') 

@app.route('/modulcyber3', methods=['GET', 'POST'])
def modulc3():
    return render_template('modulcyber3.html') 

@app.route('/modulcyber4', methods=['GET', 'POST'])
def modulc4():
    return render_template('modulcyber4.html') 

@app.route('/modulsos1', methods=['GET', 'POST'])
def moduls1():
    return render_template('modulsos1.html') 

@app.route('/modulsos2', methods=['GET', 'POST'])
def moduls2():
    return render_template('modulsos2.html') 

@app.route('/modulsos3', methods=['GET', 'POST'])
def moduls3():
    return render_template('modulsos3.html') 

@app.route('/modulsos4', methods=['GET', 'POST'])
def moduls4():
    return render_template('modulsos4.html') 

if __name__ == "__main__":
    app.run(debug=True)