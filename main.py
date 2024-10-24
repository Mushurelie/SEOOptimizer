import requests
from bs4 import BeautifulSoup
from termcolor import colored
import random
import os
import time
import pyfiglet

def print_rainbow_text(text):
    """Affiche le texte en arc-en-ciel avec des effets de chargement"""
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    for char in text:
        print(colored(char, random.choice(colors)), end='', flush=True)
        time.sleep(0.05)  # Effet de chargement
    print()
    save_to_log(text)  # Enregistre le texte dans le log

def print_loading():
    """Simule un effet de chargement"""
    loading_text = "Chargement en cours"
    for i in range(3):
        print_rainbow_text(loading_text + "." * (i + 1))
        time.sleep(0.5)

def get_website_content(url):
    """Récupère le contenu HTML du site"""
    print_loading()
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            error_message = f"Erreur lors de la requête HTTP: {response.status_code}"
            print(error_message)
            save_to_log(error_message)  # Enregistre l'erreur dans le log
            return None
    except requests.exceptions.RequestException as e:
        error_message = f"Erreur de connexion: {e}"
        print(error_message)
        save_to_log(error_message)  # Enregistre l'erreur dans le log
        return None

def check_title_and_description(soup):
    """Vérifie la balise title et la balise meta description"""
    title = soup.find('title')
    description = soup.find('meta', attrs={'name': 'description'})
    
    if title:
        print_rainbow_text(f"Titre trouvé : {title.string}")
    else:
        print("Balise title manquante.")
        save_to_log("Balise title manquante.")

    if description:
        print_rainbow_text(f"Description trouvée : {description['content']}")
    else:
        print("Balise meta description manquante.")
        save_to_log("Balise meta description manquante.")

def check_open_graph_tags(soup):
    """Vérifie la présence des balises Open Graph"""
    og_title = soup.find('meta', property='og:title')
    og_description = soup.find('meta', property='og:description')
    if og_title and og_description:
        print_rainbow_text(f"Open Graph trouvé : Titre: {og_title['content']}, Description: {og_description['content']}")
    else:
        print("Balises Open Graph manquantes (utile pour le partage sur les réseaux sociaux)")
        save_to_log("Balises Open Graph manquantes.")

def check_twitter_cards(soup):
    """Vérifie la présence des balises Twitter Cards"""
    twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
    twitter_description = soup.find('meta', attrs={'name': 'twitter:description'})
    if twitter_title and twitter_description:
        print_rainbow_text(f"Twitter Cards trouvées : Titre: {twitter_title['content']}, Description: {twitter_description['content']}")
    else:
        print("Balises Twitter Cards manquantes")
        save_to_log("Balises Twitter Cards manquantes.")

def check_links(soup):
    """Analyse des liens internes et externes"""
    internal_links = []
    external_links = []
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith("http"):
            external_links.append(href)
        else:
            internal_links.append(href)
    
    print(f"Liens internes trouvés : {len(internal_links)}")
    print(f"Liens externes trouvés : {len(external_links)}")
    save_to_log(f"Liens internes trouvés : {len(internal_links)}")
    save_to_log(f"Liens externes trouvés : {len(external_links)}")

    if len(external_links) < 5:
        print("Ajoutez plus de liens externes vers des sites de qualité pour améliorer votre référencement")
        save_to_log("Ajoutez plus de liens externes vers des sites de qualité pour améliorer votre référencement")

def generate_sitemap(url):
    """Génère un fichier sitemap.xml basique"""
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>{url}</loc>
            <priority>1.00</priority>
        </url>
    </urlset>
    """
    with open("sitemap.xml", "w") as file:
        file.write(sitemap_content)
    print_rainbow_text("Fichier sitemap.xml généré avec succès !")

def check_https(url):
    """Vérifie si le site utilise HTTPS"""
    if url.startswith("https"):
        print_rainbow_text("Le site utilise HTTPS, ce qui est bon pour le SEO.")
    else:
        print("Le site n'utilise pas HTTPS. Il est recommandé de passer à HTTPS pour améliorer la sécurité et le SEO.")
        save_to_log("Le site n'utilise pas HTTPS. Il est recommandé de passer à HTTPS.")

def ping_search_engines(url):
    """Envoie des pings à Google et Bing pour accélérer l'indexation"""
    google_ping = f"http://www.google.com/ping?sitemap={url}/sitemap.xml"
    bing_ping = f"http://www.bing.com/ping?sitemap={url}/sitemap.xml"

    try:
        requests.get(google_ping)
        print_rainbow_text("Ping envoyé à Google avec succès !")
        requests.get(bing_ping)
        print_rainbow_text("Ping envoyé à Bing avec succès !")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi des pings : {e}")
        save_to_log(f"Erreur lors de l'envoi des pings : {e}")

def check_files(url):
    """Vérifie la présence des fichiers robots.txt et favicon.ico"""
    robots_url = url + "/robots.txt"
    favicon_url = url + "/favicon.ico"
    
    try:
        robots_response = requests.get(robots_url)
        if robots_response.status_code == 200:
            print_rainbow_text("Fichier robots.txt trouvé")
        else:
            print("Fichier robots.txt manquant")
            save_to_log("Fichier robots.txt manquant.")

        favicon_response = requests.get(favicon_url)
        if favicon_response.status_code == 200:
            print_rainbow_text("Favicon trouvé")
        else:
            print("Favicon manquant")
            save_to_log("Favicon manquant.")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la vérification des fichiers : {e}")
        save_to_log(f"Erreur lors de la vérification des fichiers : {e}")

def generate_htaccess():
    """Génère un fichier .htaccess avec des optimisations SEO"""
    htaccess_content = """
    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteCond %{HTTPS} !=on
        RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
    </IfModule>
    
    <IfModule mod_expires.c>
        ExpiresActive On
        ExpiresByType image/jpg "access plus 1 year"
        ExpiresByType image/jpeg "access plus 1 year"
        ExpiresByType image/gif "access plus 1 year"
        ExpiresByType image/png "access plus 1 year"
    </IfModule>
    """
    with open(".htaccess", "w") as file:
        file.write(htaccess_content)
    print_rainbow_text("Fichier .htaccess généré avec succès !")
    print_rainbow_text("Assurez-vous de placer ce fichier à la racine de votre serveur web pour qu'il soit pris en compte.")

def save_to_log(text):
    """Sauvegarde le texte dans un fichier log"""
    with open("seo_log.txt", "a") as log_file:
        log_file.write(text + "\n")

def display_ascii_name():
    """Affiche le nom en ASCII"""
    ascii_name = pyfiglet.figlet_format("Mushurelie")
    print(ascii_name)
    save_to_log(ascii_name.strip())  # Enregistre le nom dans le log

def analyze_seo(url):
    """Analyse SEO du site"""
    content = get_website_content(url)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')

    # Affiche le nom en ASCII
    display_ascii_name()

    # Vérifier la balise title et description
    check_title_and_description(soup)
    check_https(url)
    check_open_graph_tags(soup)
    check_twitter_cards(soup)
    check_links(soup)
    check_files(url)

        # Générer le sitemap
    generate_sitemap(url)

    # Envoyer des pings aux moteurs de recherche
    ping_search_engines(url)

    # Générer le fichier .htaccess
    generate_htaccess()

if __name__ == "__main__":
    url = input("Entrez l'URL du site à analyser : ")
    analyze_seo(url)
