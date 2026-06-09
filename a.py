from PIL import Image
chemin_image = "/home/younais/Documents/Gitlab/mediashelf-application-mobile/neonaure-sae/Exemples de grille-20260609/grille1.png"

try:
    img = Image.open(chemin_image)
    img.show()
    print(f"Format: {img.format}, Taille: {img.size}, Mode: {img.mode}")
    
except FileNotFoundError:
    print(f"Erreur : Le fichier est introuvable à l'emplacement : {chemin_image}")
except Exception as e:
    print(f"Une erreur est survenue : {e}")