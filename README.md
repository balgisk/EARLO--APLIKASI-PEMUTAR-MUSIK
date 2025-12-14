README.md
# 🎵 EARLO Music Player Console Application

Aplikasi **Music Player berbasis konsol** yang dikembangkan sebagai Tugas Besar Mata Kuliah **Struktur Data**. Aplikasi ini menerapkan **Doubly Linked List (DLL)** dan **Binary Search Tree (BST)** untuk mengelola data lagu, playlist, serta mempercepat proses pencarian.

---

## 📌 Fitur Utama

### 👤 Admin

* Menambahkan lagu ke library (judul, artis, genre, path file)
* Menampilkan seluruh lagu dalam library
* Mengubah data lagu
* Menghapus lagu dari library

### 👥 User

* Mencari lagu menggunakan BST
* Memutar lagu dari library atau playlist
* Navigasi lagu (Next & Previous)
* Membuat dan mengelola playlist

---

## 🧠 Struktur Data yang Digunakan

* **Doubly Linked List (DLL)**
  Digunakan untuk library lagu dan playlist karena mendukung traversal dua arah (next/prev) serta operasi insert dan delete yang efisien.

* **Binary Search Tree (BST)**
  Digunakan untuk pencarian lagu berdasarkan judul agar lebih cepat dibandingkan pencarian linear.

---

## ⚙️ Teknologi

* Bahasa Pemrograman: **Python**
* Library Audio: **pygame (pygame.mixer)**
* Interface: **Command Line Interface (CLI)**

---

## ▶️ Cara Menjalankan Program

1. Pastikan Python sudah terinstall.
2. Install library pygame:

   ```bash
   pip install pygame
   ```
3. Jalankan program utama:

   ```bash
   python main.py
   ```

---

## 📂 Struktur Program (Umum)

```
├── song.py            # Node lagu (DLL)
├── music_library.py  # DLL Library lagu
├── bst.py            # Binary Search Tree pencarian lagu
├── playlist.py       # DLL Playlist
├── main.py           # Program utama
---

## 👨‍💻 Tim Pengembang

* Zahira Kayla Wardhani (103102400022)
* Balgis Khairunnisa Syakira (103102400025)
* Kanaya Putri Prabasa (103102400035)

Program Studi **Sains Data**
Fakultas Informatika
Universitas Telkom Surabaya – 2025

---

✨ Proyek ini dibuat untuk menerapkan konsep struktur data ke dalam studi kasus nyata berupa aplikasi pemutar musik berbasis konsol.
