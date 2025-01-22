import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# Dictionnaire des maladies et leurs R0
maladies = {
    "Rougeole": 12,
    "COVID-19": 2.5,
    "Grippe saisonnière": 1.3,
    "Varicelle": 10,
    "Ebola": 1.8
}

# Fonction de simulation
def population_totale_commune():
    try:
        population_totale = int(entree_population.get())  # Récupère la population
        maladie = maladie_selectionnee.get()  # Récupère la maladie sélectionnée

        if maladie not in maladies:
            raise ValueError("Maladie non trouvée dans la base.")

        r0 = maladies[maladie]
        contamines = 1  # Patient zéro
        jours = 0

        # Réinitialisation de la zone de résultats
        zone_resultats.delete(1.0, tk.END)
        zone_resultats.insert(tk.END, f"Simulation pour '{maladie}' (R0 = {r0}):\n")
        zone_resultats.insert(tk.END, f"Population totale : {population_totale} personnes\n\n")

        # Simulation jour par jour
        while contamines < population_totale:
            nouveaux_cas = int(contamines * r0)  # Nombre de nouvelles infections
            contamines += nouveaux_cas
            jours += 1

            # Limiter à la population totale
            if contamines >= population_totale:
                contamines = population_totale

            # Affichage dans la zone de texte
            zone_resultats.insert(tk.END, f"Jour {jours}: {contamines:,} personnes contaminées\n")

        # Résumé final
        zone_resultats.insert(tk.END, f"\n=== Résultats ===\n")
        zone_resultats.insert(tk.END, f"Population totale contaminée ({population_totale:,} personnes) en {jours} jours.")

        # Charger et afficher l'image de la maladie
        afficher_image(maladie)
    except ValueError as e:
        messagebox.showerror("Erreur", f"Entrée invalide : {e}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur inattendue s'est produite : {e}")

# Fonction pour afficher l'image de la maladie
def afficher_image(maladie):
    try:
        # Charger l'image correspondante
        image_path = f"{maladie.lower().replace(' ', '_')}.png"  # Ex: "rougeole.png"
        image = Image.open(image_path)
        image = image.resize((150, 150), Image.ANTIALIAS)  # Redimensionner l'image
        photo = ImageTk.PhotoImage(image)

        # Mettre à jour l'image affichée
        label_image.configure(image=photo)
        label_image.image = photo
    except FileNotFoundError:
        label_image.configure(image='', text="Image non disponible")
        label_image.image = None

# Fonction pour quitter l'application
def quitter_application():
    fenetre.destroy()

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Simulation de Propagation des Maladies")
fenetre.geometry("600x700")

# Titre
label_titre = tk.Label(fenetre, text="Simulation de Propagation", font=("Arial", 16, "bold"))
label_titre.pack(pady=10)

# Sélection de la maladie
frame_maladie = tk.Frame(fenetre)
frame_maladie.pack(pady=10)

label_maladie = tk.Label(frame_maladie, text="Choisissez une maladie :", font=("Arial", 12))
label_maladie.grid(row=0, column=0, padx=10, pady=5)

maladie_selectionnee = ttk.Combobox(frame_maladie, values=list(maladies.keys()), state="readonly", font=("Arial", 12))
maladie_selectionnee.grid(row=0, column=1, padx=10, pady=5)
maladie_selectionnee.current(0)  # Sélectionner la première maladie par défaut

# Entrée pour la population
frame_population = tk.Frame(fenetre)
frame_population.pack(pady=10)

label_population = tk.Label(frame_population, text="Population totale :", font=("Arial", 12))
label_population.grid(row=0, column=0, padx=10, pady=5)

entree_population = tk.Entry(frame_population, font=("Arial", 12))
entree_population.grid(row=0, column=1, padx=10, pady=5)

# Boutons d'action
frame_boutons = tk.Frame(fenetre)
frame_boutons.pack(pady=20)

btn_simuler = tk.Button(frame_boutons, text="Lancer la simulation", command=population_totale_commune, bg="green", fg="white", font=("Arial", 12))
btn_simuler.grid(row=0, column=0, padx=10)

btn_quitter = tk.Button(frame_boutons, text="Quitter", command=quitter_application, bg="red", fg="white", font=("Arial", 12))
btn_quitter.grid(row=0, column=1, padx=10)

# Zone pour afficher l'image de la maladie
frame_image = tk.Frame(fenetre)
frame_image.pack(pady=10)

label_image = tk.Label(frame_image, text="Aucune image disponible", font=("Arial", 12), width=20, height=10, borderwidth=2, relief="solid")
label_image.pack()

# Zone de résultats
label_resultats = tk.Label(fenetre, text="Résultats de la simulation :", font=("Arial", 12))
label_resultats.pack(pady=10)

zone_resultats = tk.Text(fenetre, width=70, height=20, wrap="word", font=("Arial", 10), borderwidth=2, relief="sunken")
zone_resultats.pack(pady=10)

# Lancer la boucle principale
fenetre.mainloop()
