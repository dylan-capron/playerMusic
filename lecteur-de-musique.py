import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pygame
import random
from ttkthemes import ThemedStyle

pygame.mixer.init()

class LecteurAudio:
    def __init__(self, master):
        self.master = master
        master.title("Lecteur Audio")

        # Utilisation du thème "plastik" pour les widgets ttk
        style = ThemedStyle(master)
        style.set_theme("plastik")

        self.playlist = []
        self.current_track = 0
        self.paused = False

        self.label = ttk.Label(master, text="Lecteur Audio", font=('Helvetica', 16, 'bold'))
        self.label.pack()

        self.listbox = tk.Listbox(master, selectmode=tk.SINGLE, font=('Helvetica', 12))
        self.listbox.pack()

        self.load_button = ttk.Button(master, text="Choisir une piste", command=self.load_track)
        self.load_button.pack()

        self.play_button = ttk.Button(master, text="Lancer la lecture", command=self.play_track)
        self.play_button.pack()

        self.pause_button = ttk.Button(master, text="Mettre en pause", command=self.pause_track)
        self.pause_button.pack()

        self.stop_button = ttk.Button(master, text="Arrêter la lecture", command=self.stop_track)
        self.stop_button.pack()

        self.next_button = ttk.Button(master, text="Musique suivante", command=self.next_track)
        self.next_button.pack()

        self.random_button = ttk.Button(master, text="Sélection aléatoire", command=self.random_track)
        self.random_button.pack()

        self.volume_label = ttk.Label(master, text="Volume:")
        self.volume_label.pack()

        self.volume_slider = ttk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.set(50)
        self.volume_slider.pack()

        self.loop_var = tk.BooleanVar()
        self.loop_checkbox = ttk.Checkbutton(master, text="Lire en boucle", variable=self.loop_var)
        self.loop_checkbox.pack()

        self.add_button = ttk.Button(master, text="Ajouter une piste", command=self.add_track)
        self.add_button.pack()

        self.remove_button = ttk.Button(master, text="Supprimer la piste sélectionnée", command=self.remove_track)
        self.remove_button.pack()

        self.progress_bar = ttk.Progressbar(master, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress_bar.pack()

        self.image_label = tk.Label(master)
        self.image_label.pack()

        # Ajout de la liaison (binding) pour mettre à jour la musique lors du déplacement de la barre de progression
        self.progress_bar.bind("<Button-1>", self.set_music_position)

        self.update_progress()

    def load_track(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers audio", "*.mp3;*.wav")])
        if file_path:
            self.playlist.append(file_path)
            self.listbox.insert(tk.END, os.path.basename(file_path))
            self.load_thumbnail(file_path)
            
            # Redémarrez le mélangeur de sons pour prendre en compte la nouvelle piste
            pygame.mixer.init()

            self.update_progress()

    def play_track(self):
        if self.playlist:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            track = self.playlist[self.current_track]
            pygame.mixer.music.load(track)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(self.volume_slider.get() / 100)
            self.update_progress()

    def pause_track(self):
        if pygame.mixer.music.get_busy():
            if not self.paused:
                pygame.mixer.music.pause()
                self.paused = True
            else:
                pygame.mixer.music.unpause()
                self.paused = False

    def stop_track(self):
        pygame.mixer.music.stop()
        self.update_progress()

    def set_volume(self, val):
        volume = float(val) / 100
        pygame.mixer.music.set_volume(volume)

    def add_track(self):
        self.load_track()

    def remove_track(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.playlist[index]
            self.listbox.delete(index)
            self.update_progress()

    def next_track(self):
        if self.playlist:
            self.current_track = (self.current_track + 1) % len(self.playlist)
            self.play_track()

    def random_track(self):
        if self.playlist:
            self.current_track = random.randint(0, len(self.playlist) - 1)
            self.play_track()

    def set_music_position(self, event):
        # Réglage de la position de la musique en fonction de la position de la barre de progression
        if self.playlist:
            position = event.x / self.progress_bar.winfo_width()
            track_length = pygame.mixer.Sound(self.playlist[self.current_track]).get_length()
            new_position = int(position * track_length)
            pygame.mixer.music.set_pos(new_position)
            self.update_progress()

    def update_progress(self):
        # Met à jour la barre de progression en fonction du temps écoulé de la piste
        if pygame.mixer.music.get_busy():
            elapsed_time = pygame.mixer.music.get_pos() / 1000  # en secondes
            track_length = pygame.mixer.Sound(self.playlist[self.current_track]).get_length()
            progress_percentage = (elapsed_time / track_length) * 100
            self.progress_bar['value'] = progress_percentage
            self.master.after(1000, self.update_progress)  # Met à jour la barre de progression toutes les 1000 ms
        else:
            self.progress_bar['value'] = 0

    def load_thumbnail(self, file_path):
        # Placeholder pour la fonction de chargement de la miniature
        # Remplacez ceci par votre propre logique pour charger la miniature
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = LecteurAudio(root)
    root.mainloop()
