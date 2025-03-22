from PIL import Image

# Charger l'image originale
image_path = "image/player/soldier_walking.png"  # Remplace par le chemin de ton fichier
image = Image.open(image_path)

# Définir le nombre de sprites
nombre_sprites = 5  # Change ce nombre si besoin

# Calculer la largeur d'un sprite (si les sprites sont alignés horizontalement)
sprite_width = image.width // nombre_sprites
sprite_height = image.height  # Si les sprites sont sur une seule ligne

# Boucle pour découper et enregistrer chaque sprite
for i in range(nombre_sprites):
    left = i * sprite_width
    right = left + sprite_width
    sprite = image.crop((left, 0, right, sprite_height))

    sprite_filename = f"sprite_{i + 6}.png"
    sprite.save(sprite_filename)
    print(f"Sprite {i + 6} enregistré sous {sprite_filename}")
