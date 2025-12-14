# INIT PYGAME
import pygame
import os
pygame.init()
pygame.mixer.init()

# NODE SONG (DLL)
class Song:
    def __init__(self, title, artist, genre, file_path):
        self.title = title
        self.artist = artist
        self.genre = genre
        self.file_path = file_path
        self.prev = None
        self.next = None

# MUSIC LIBRARY (DLL)
class MusicLibrary:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_song(self, title, artist, genre, file_path):
        new_song = Song(title, artist, genre, file_path)

        if not self.head:
            self.head = self.tail = new_song
        else:
            self.tail.next = new_song
            new_song.prev = self.tail
            self.tail = new_song

        return new_song

    def delete_song(self, title):
        curr = self.head
        while curr:
            if curr.title.lower() == title.lower():

                if curr.prev:
                    curr.prev.next = curr.next
                else:
                    self.head = curr.next

                if curr.next:
                    curr.next.prev = curr.prev
                else:
                    self.tail = curr.prev

                return curr
            curr = curr.next
        return None

    def update_song(self, old_title, new_title=None, new_artist=None, new_genre=None, new_path=None):
        curr = self.head
        while curr:
            if curr.title.lower() == old_title.lower():

                # Update data jika user mengisi nilai baru
                if new_title:
                    curr.title = new_title
                if new_artist:
                    curr.artist = new_artist
                if new_genre:
                    curr.genre = new_genre
                if new_path:
                    curr.file_path = new_path

                return curr
            curr = curr.next
        return None

    def show_library(self):
        curr = self.head
        if not curr:
            print("Library kosong.")
            return

        print("\n=== LIST LAGU ===")
        while curr:
            print(f"{curr.title} - {curr.artist} ({curr.genre})")
            curr = curr.next

# PLAYLIST (DLL)
class Playlist:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, song):
        if not song:
            return False

        # 🔑 CLONE NODE (BIAR TIDAK MERUSAK LIBRARY)
        new_song = Song(
            song.title,
            song.artist,
            song.genre,
            song.file_path
        )

        if not self.head:
            self.head = self.tail = new_song
        else:
            self.tail.next = new_song
            new_song.prev = self.tail
            self.tail = new_song

        return True

    def remove(self, title):
        curr = self.head
        while curr:
            if curr.title.lower() == title.lower():
                if curr.prev:
                    curr.prev.next = curr.next
                else:
                    self.head = curr.next

                if curr.next:
                    curr.next.prev = curr.prev
                else:
                    self.tail = curr.prev

                curr.next = curr.prev = None
                return curr
            curr = curr.next
        return None

    def show(self):
        curr = self.head
        if not curr:
            print("Playlist kosong.")
            return
        print("\n=== PLAYLIST ===")
        while curr:
            print(f"{curr.title} - {curr.artist}")
            curr = curr.next


# BST FOR SONG SEARCH
class BSTNode:
    def __init__(self, key, song_node):
        self.key = key
        self.song = song_node
        self.left = None
        self.right = None

class SongBST:
    def __init__(self):
        self.root = None

    def insert(self, key, song_node):
        self.root = self._insert(self.root, key.lower(), song_node)

    def _insert(self, node, key, song_node):
        if not node:
            return BSTNode(key, song_node)
        if key < node.key:
            node.left = self._insert(node.left, key, song_node)
        elif key > node.key:
            node.right = self._insert(node.right, key, song_node)
        return node

    def search(self, key):
        return self._search(self.root, key.lower())

    def _search(self, node, key):
        if not node:
            return None
        if key == node.key:
            return node.song
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    # HAPUS NODE BST
    def delete(self, key):
        self.root = self._delete(self.root, key.lower())

    def _delete(self, node, key):
        if not node:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left

            succ = self._min_value_node(node.right)
            node.key = succ.key
            node.song = succ.song
            node.right = self._delete(node.right, succ.key)

        return node

    def _min_value_node(self, node):
        curr = node
        while curr.left:
            curr = curr.left
        return curr

# FIND SIMILAR SONG (berdasarkan artist atau genre)
# Rename fungsi supaya konsisten
def find_similar_song(current, library):
    if not current:
        return None

    target_artist = current.artist.lower()
    target_genre = current.genre.lower()

    curr = library.head
    best_match = None

    while curr:
        if curr is not current:
            # Prioritas: artist sama, jika tidak ada, genre sama
            if curr.artist.lower() == target_artist:
                return curr
            if not best_match and curr.genre.lower() == target_genre:
                best_match = curr
        curr = curr.next

    return best_match

# PLAYER CONTROL
current_song = None

def play_song(song, playlist_node=None):
    global current_song, current_playlist_node

    if playlist_node and playlist_node.title != song.title:
        raise ValueError("Playlist node dan song tidak konsisten")

    current_song = song
    current_playlist_node = playlist_node

    try:
        pygame.mixer.music.load(song.file_path)
        pygame.mixer.music.play()
        print(f"\nNow Playing: {song.title}")
    except Exception as e:
        print("Gagal memutar lagu:", e)

def stop_song():
    pygame.mixer.music.stop()
    print("Music stopped.")

# MAIN PROGRAM 
library = MusicLibrary()
bst = SongBST()
playlist = Playlist()
current_song = None              # node library
current_playlist_node = None     # node playlist

def load_all_songs():
    folder = "songs"

    if not os.path.exists(folder):
        print("Folder 'songs' tidak ditemukan. Membuat folder 'songs'...")
        os.makedirs(folder)

    for f in os.listdir(folder):
        if f.lower().endswith(".mp3"):
            title = os.path.splitext(f)[0]
            artist = "Unknown"
            genre = "Unknown"
            path = os.path.join(folder, f)

            song = library.add_song(title, artist, genre, path)
            bst.insert(title, song)

    print("Semua lagu berhasil dimuat!\n")

load_all_songs()

# MENU USER
def menu_user():
    global current_song, current_playlist_node

    while True:
        print("""
=== MENU USER ===
1. Cari Lagu
2. Play Lagu
3. Stop Lagu
4. Next
5. Prev
6. Kelola Playlist
7. Kembali
        """)
        pilih = input("Pilih: ").strip()

        # 1. CARI LAGU
        if pilih == "1":
            keyword = input("Masukkan judul/artis/genre: ").lower()

            curr = library.head
            found = False
            while curr:
                if (keyword in curr.title.lower() or
                    keyword in curr.artist.lower() or
                    keyword in curr.genre.lower()):
                    print(f"Ditemukan: {curr.title} - {curr.artist} ({curr.genre})")
                    found = True
                curr = curr.next

            if not found:
                print("Tidak ditemukan.")

        # 2. PLAY
        elif pilih == "2":
            judul = input("Judul lagu yang diputar: ").lower()
            song = bst.search(judul)
            if song:
                play_song(song)     # playlist_node = None
            else:
                print("Lagu tidak ditemukan.")

        # 3. STOP
        elif pilih == "3":
            stop_song()

        # 4. NEXT Lagu
        elif pilih == "4":
            if not current_song:
                print("Belum memutar lagu.")
                continue

            # prioritas playlist
            if current_playlist_node:
                if current_playlist_node.next:
                    current_playlist_node = current_playlist_node.next
                    play_song(current_playlist_node, current_playlist_node)
                else:
                    print("Sudah di akhir playlist.")
            else:
                # mode library (rekomendasi)
                similar = find_similar_song(current_song, library)
                if similar:
                    play_song(similar)
                else:
                    print("Tidak ada lagu serupa.")

        # 5. PREV Lagu
        elif pilih == "5":
            if not current_song:
                print("Belum memutar lagu.")
                continue

            if current_playlist_node:
                if current_playlist_node.prev:
                    current_playlist_node = current_playlist_node.prev
                    play_song(current_playlist_node, current_playlist_node)
                else:
                    print("Sudah di awal playlist.")
            else:
                print("Tidak ada fitur prev untuk lagu serupa.")

        # 6. KELOLA PLAYLIST
        elif pilih == "6":
            while True:
                print("""
=== PLAYLIST MENU ===
1. Tambah Lagu
2. Hapus Lagu
3. Lihat Playlist
4. Kembali
                """)
                p = input("Pilih: ")

                if p == "1":
                    j = input("Judul lagu: ").lower()
                    s = bst.search(j)
                    if s:
                        playlist.add(s)
                        print("Ditambahkan ke playlist!")
                    else:
                        print("Lagu tidak ditemukan.")

                elif p == "2":
                    j = input("Judul lagu: ").lower()
                    h = playlist.remove(j)
                    if h:
                        print("Lagu dihapus dari playlist.")
                    else:
                        print("Tidak ada lagu itu di playlist.")

                elif p == "3":
                    playlist.show()

                elif p == "4":
                    break
                else:
                    print("Pilihan tidak dikenal.")

        elif pilih == "7":
            break
        else:
            print("Pilihan tidak dikenal.")

# MENU ADMIN 
def menu_admin():
    global current_song, current_playlist_node

    while True:
        print("""
=== MENU ADMIN ===
1. Lihat Library
2. Tambah Lagu
3. Hapus Lagu
4. Update Lagu
5. Kembali
        """)
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            library.show_library()

        elif pilih == "2":
            judul = input("Judul: ").strip()
            artis = input("Artis: ").strip()
            genre = input("Genre: ").strip()

            nama_file = input("Nama file (contoh: hello.mp3): ").strip()
            file_path = os.path.join("songs", nama_file)

            if not os.path.exists(file_path):
                print("File tidak ditemukan di folder 'songs'. Pastikan nama file benar.")
                continue

            song = library.add_song(judul, artis, genre, file_path)
            bst.insert(judul, song)
            print("Lagu berhasil ditambahkan!")

        elif pilih == "3":
            judul = input("Judul lagu yang ingin dihapus: ").strip()

            hapus = library.delete_song(judul)
            if hapus:
                bst.delete(judul)
                playlist.remove(judul)  # sinkronisasi playlist

                if current_song and current_song.title.lower() == judul.lower():
                    stop_song()
                    current_song = None

                print(f"Lagu '{judul}' berhasil dihapus.")
            else:
                print("Lagu tidak ditemukan.")

        elif pilih == "4":
            old = input("Judul lagu yang ingin diupdate (exact): ").strip()
            if not bst.search(old.lower()):
                print("Lagu tidak ditemukan.")
                continue

            new_title = input("Judul baru (enter jika tidak): ").strip() or None
            new_artist = input("Artis baru (enter jika tidak): ").strip() or None
            new_genre = input("Genre baru (enter jika tidak): ").strip() or None
            new_path_input = input("Nama file baru di folder songs (enter jika tidak): ").strip() or None

            new_path = None
            if new_path_input:
                candidate = os.path.join("songs", new_path_input)
                if not os.path.exists(candidate):
                    print("File baru tidak ditemukan di folder 'songs'. Update path dibatalkan.")
                    continue
                new_path = candidate

            lagu = library.update_song(
                old,
                new_title=new_title,
                new_artist=new_artist,
                new_genre=new_genre,
                new_path=new_path
            )

            if lagu:
                # jika judul berubah, harus update BST key: delete old key, insert new key
                if new_title:
                    bst.delete(old)
                    bst.insert(lagu.title, lagu)
                print("Data lagu berhasil diupdate.")
            else:
                print("Lagu tidak ditemukan.")

        elif pilih == "5":
            break

        else:
            print("Pilihan tidak dikenal.")

# START
while True:
    print("""
=== SELAMAT DATANG ===
1. ADMIN
2. USER
3. Keluar
    """)
    pilih = input("Pilih: ").strip()

    if pilih == "1":
        menu_admin()
    elif pilih == "2":
        menu_user()
    elif pilih == "3":
        break
    else:
        print("Pilihan tidak dikenal.")
        