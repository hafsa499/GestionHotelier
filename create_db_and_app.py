import streamlit as st
import sqlite3
from datetime import date

# ---------- CSS GLOBAL + NAVBAR + STYLE + FOOTER ----------
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

<style>
html, body {
    margin: 0;
    padding: 0;
    overflow-x: hidden;
    font-family: 'Segoe UI', sans-serif;
    height: 100%;
    background-color: #f0f0f0;
}

body {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

header {
    visibility: hidden;
}

/* CONTAINER GLOBAL FIXE CENTRÉ */
.container {
    width: 100%;
    display: flex;
    justify-content: center;
}

.content {
    width: 1200px;
    max-width: 95%;
    box-sizing: border-box;
}

/* NAVBAR */
#navbar {
    background-color: #111;
    padding: 15px 30px;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    color: white;
    font-weight: bold;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999;
}
#navbar a {
    color: white;
    text-decoration: none;
    margin-left: 20px;
}
#navbar a:hover {
    color: #FFD700;
    text-decoration: underline;
}

/* SECTIONS */
.section {
    padding: 140px 0 80px 0;
    box-sizing: border-box;
}

/* ACCUEIL BLEU */
#accueil {
    background: linear-gradient(to right, #001F3F, #0074D9);
    color: white;
}

/* AUTRES SECTIONS */
#reservations, #clients, #chambres, #apropos, #services {
    background-color: #ffffff;
    color: #111;
}

/* RESPONSIVE NAVBAR */
@media screen and (max-width: 768px) {
    #navbar {
        flex-direction: column;
        align-items: flex-start;
    }
    #navbar a {
        margin: 5px 0;
    }
}

/* FOOTER FIXÉ EN BAS */
footer {
    background-color: #111;
    color: white;
    text-align: center;
    padding: 15px;
    font-size: 0.9em;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
}
</style>




<div id="navbar">
    <div><span style="font-size:1.5em; color:#00BFFF;"><b><i class="fa-solid fa-hotel"></i> HotelDB</b></span></div>
    <div>
        <a href="#accueil">Accueil</a>
        <a href="#reservations">Réservations</a>
        <a href="#clients">Clients</a>
        <a href="#chambres">Chambres</a>
        <a href="#apropos">À propos</a>
        <a href="#services">Services</a>
    </div>
</div>

<div id="accueil" class="section">
    <h1><i class="fa-solid fa-house-chimney"></i> Bienvenue dans le système de gestion hôtelière</h1>
    <p style='font-size: 1.3em;'>Simplifiez la gestion des clients, des chambres et des réservations.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Connexion SQLite ----------
conn = sqlite3.connect("HotelDB2025.db", check_same_thread=False)
cursor = conn.cursor()
DATE_REFERENCE = date(2025, 5, 10)

# ---------- SECTION RÉSERVATIONS ----------
st.markdown("<div id='reservations' class='section'></div>", unsafe_allow_html=True)
st.header("📆 Réservations")
cursor.execute("""
    SELECT R.Id_Reservation, R.Date_Arr, R.Date_Dep, R.Nom_Complet, H.Ville_H
    FROM Reservation R
    JOIN Client_Hotel C ON R.Nom_Complet = C.Nom_Complet
    JOIN Concerner Co ON R.Id_Reservation = Co.Id_Reservation
    JOIN Type_Chambre T ON Co.Id_Type = T.Id_Type
    JOIN Chambre CH ON T.Id_Type = CH.Id_Type
    JOIN Hotel H ON CH.Id_Hotel = H.Id_Hotel
    GROUP BY R.Id_Reservation
""")
for row in cursor.fetchall():
    st.write(f"🛏 Réservation {row[0]} — Client: {row[3]} — Hôtel: {row[4]} — Du {row[1]} au {row[2]}")

# ---------- SECTION CLIENTS ----------
st.markdown("<div id='clients' class='section'></div>", unsafe_allow_html=True)
st.header("👥 Clients")
cursor.execute("SELECT * FROM Client_Hotel")
for c in cursor.fetchall():
    st.write(f"{c[0]} — {c[1]}, {c[2]} ({c[3]}) — {c[4]} — {c[5]}")

# ---------- SECTION CHAMBRES DISPONIBLES ----------
st.markdown("<div id='chambres' class='section'></div>", unsafe_allow_html=True)
st.header("🏨 Disponibilité des chambres")
cursor.execute("SELECT Id_Chambre FROM Chambre ORDER BY Id_Chambre")
chambres = [row[0] for row in cursor.fetchall()]
for chambre in chambres:
    cursor.execute("""
        SELECT MAX(R.Date_Dep)
        FROM Chambre CH
        JOIN Concerner Co ON CH.Id_Type = Co.Id_Type
        JOIN Reservation R ON Co.Id_Reservation = R.Id_Reservation
        WHERE CH.Id_Chambre = ? AND R.Date_Dep > ?
    """, (chambre, DATE_REFERENCE))
    date_dep = cursor.fetchone()[0]
    if date_dep:
        dispo_str = date.fromisoformat(date_dep).strftime("%d/%m/%Y")
        st.write(f"✅ Chambre {chambre} — disponible à partir du {dispo_str}")
    else:
        st.write(f"✅ Chambre {chambre} — disponible")

# ---------- SECTION À PROPOS ----------
st.markdown("<div id='apropos' class='section'></div>", unsafe_allow_html=True)
st.header("ℹ À propos")
st.markdown("Cette application a été réalisée pour la *Gestion Hôtelière*. Elle vous permet de gérer les clients, chambres, réservations et services hôteliers de façon efficace.")

# ---------- SECTION SERVICES ----------
st.markdown("<div id='services' class='section'></div>", unsafe_allow_html=True)
st.header("⚙ Services ")

# --- Ajouter client ---
st.subheader("➕ Ajouter un client")
nom = st.text_input("Nom complet")
adresse = st.text_input("Adresse")
ville = st.text_input("Ville")
code_postal = st.number_input("Code postal", min_value=1000, max_value=99999)
email = st.text_input("Email")
tel = st.number_input("Téléphone", min_value=100000000, max_value=999999999)

if st.button("Ajouter le client"):
    try:
        cursor.execute("INSERT INTO Client_Hotel VALUES (?, ?, ?, ?, ?, ?)",
                       (nom, adresse, ville, code_postal, email, tel))
        conn.commit()
        st.success("✅ Client ajouté avec succès")
        st.experimental_rerun()
    except Exception as e:
        st.error(f"❌ Erreur : {e}")

# --- Ajouter réservation ---
st.subheader("📝 Ajouter une réservation")
cursor.execute("SELECT Nom_Complet FROM Client_Hotel")
clients = [r[0] for r in cursor.fetchall()]
cursor.execute("SELECT Id_Type FROM Type_Chambre")
types = [r[0] for r in cursor.fetchall()]
id_resa = st.text_input("ID Réservation")
client = st.selectbox("Client", clients)
type_ch = st.selectbox("Type de chambre", types)
date_arr = st.date_input("Date d'arrivée", date(2025, 6, 1))
date_dep = st.date_input("Date de départ", date(2025, 6, 5))

if st.button("Ajouter la réservation"):
    try:
        cursor.execute("INSERT INTO Reservation VALUES (?, ?, ?, ?)", (id_resa, date_arr, date_dep, client))
        cursor.execute("INSERT INTO Concerner VALUES (?, ?)", (id_resa, type_ch))
        conn.commit()
        st.success("✅ Réservation ajoutée avec succès")
        st.experimental_rerun()
    except Exception as e:
        st.error(f"❌ Erreur : {e}")

# ---------- FOOTER ----------
st.markdown("""
<footer>
    <p>&copy; 2025 HotelDB | Réalisé à la FSSM. Tous droits réservés.</p>
</footer>
""", unsafe_allow_html=True)




