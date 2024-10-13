import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext

# Función para obtener y mostrar las películas
def fetch_movies():
    url = 'https://www.imdb.com/chart/moviemeter/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        movies = soup.find_all('h3', class_='ipc-title__text')
        ratings = soup.find_all('span', class_='ipc-rating-star--rating')
        years = soup.find_all('span', class_='sc-ab348ad5-8 cSWcJI cli-title-metadata-item')

        if not movies:
            output_text.insert(tk.END, "No se encontraron películas. Verifica la estructura HTML.\n")
            return

        movie_titles = [movie.get_text() for movie in movies]
        movie_years = [year.get_text() if year else "N/A" for year in years]
        movie_ratings = [float(rating.get_text()) if rating else 0.0 for rating in ratings]

        movie_data = list(zip(movie_titles, movie_years, movie_ratings))
        sorted_movies = sorted(movie_data, key=lambda x: x[2], reverse=True)

        output_text.delete(1.0, tk.END)  # Limpiar el texto anterior
        output_text.insert(tk.END, "Películas ordenadas por calificación (de mayor a menor):\n")
        for title, year, rating in sorted_movies:
            output_text.insert(tk.END, f"Título: {title}, Año: {year}, Calificación: {rating}\n")
    else:
        output_text.insert(tk.END, f"Error al acceder a IMDb: {response.status_code}\n")

# Crear la ventana principal
window = tk.Tk()
window.title("IMDB Movie Scraper")

# Crear un botón para obtener las películas
fetch_button = tk.Button(window, text="Obtener Películas", command=fetch_movies)
fetch_button.pack(pady=10)

# Crear un área de texto para mostrar los resultados
output_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=20)
output_text.pack(padx=10, pady=10)

# Ejecutar la aplicación
window.mainloop()
