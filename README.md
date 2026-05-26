# 🍌 Nanobanana - Bot untuk Menghasilkan Gambar

Bot Telegram untuk menghasilkan gambar berdasarkan deskripsi teks.

## 🚀 Fitur

- Menghasilkan gambar berdasarkan deskripsi teks
- Dukungan berbagai API untuk menghasilkan gambar:
  - **Google Gemini Nano Banana** (default) - menghasilkan gambar dengan cepat
  - OpenAI DALL-E
  - Stability AI
  - Replicate
- Antarmuka sederhana dan intuitif
- Mode Placeholder untuk pengujian tanpa kunci API

## 📋 Persyaratan

- Python 3.8+
- Token Bot Telegram (dapatkan dari [@BotFather](https://t.me/BotFather))
- (Opsional) Kunci API untuk layanan penghasil gambar pilihan

## 🛠️ Instalasi

1. Kloning repositori atau buat proyek:
```bash
cd nanobanana
```

2. Buat lingkungan virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # Di Windows: venv\Scripts\activate
```

3. Instal ketergantungan:
```bash
pip install -r requirements.txt
```

4. Atur variabel lingkungan:
```bash
cp .env.example .env
```

Edit file `.env` dan tentukan:
- `TELEGRAM_BOT_TOKEN` - token bot Telegram Anda
- `IMAGE_API_TYPE` - jenis API (nanobanana, gemini, openai, stability, replicate, placeholder)
- `GEMINI_API_KEY` - kunci API untuk Gemini/Nano Banana (jika digunakan)
- `IMAGE_API_KEY` - kunci API untuk layanan lain (jika diperlukan)

## 🎯 Penggunaan

1. Jalankan bot:
```bash
python src/bot.py
```

2. Cari bot Anda di Telegram dan kirim perintah `/start`

3. Kirim deskripsi teks gambar yang ingin Anda buat

## 🔧 Konfigurasi API

### Google Imagen 4.0 (direkomendasikan)
1. Dapatkan kunci API di [Google AI Studio](https://aistudio.google.com/apikey)
2. Tetapkan di `.env`:
   - `IMAGE_API_TYPE=nanobanana` (atau `gemini`)
   - `GEMINI_API_KEY=your_gemini_api_key`
3. Menggunakan model `imagen-4.0-generate-001` untuk menghasilkan gambar berkualitas tinggi

### Mode Placeholder
Membuat gambar sederhana dengan teks. Tidak memerlukan kunci API. Cocok untuk pengujian.

### OpenAI DALL-E
1. Instal perpustakaan: `pip install openai`
2. Dapatkan kunci API di [platform.openai.com](https://platform.openai.com)
3. Tetapkan di `.env`:
   - `IMAGE_API_TYPE=openai`
   - `IMAGE_API_KEY=your_openai_api_key`

### Stability AI
1. Instal perpustakaan: `pip install stability-sdk`
2. Dapatkan kunci API di [platform.stability.ai](https://platform.stability.ai)
3. Tetapkan di `.env`:
   - `IMAGE_API_TYPE=stability`
   - `IMAGE_API_KEY=your_stability_api_key`

### Replicate
1. Instal perpustakaan: `pip install replicate`
2. Dapatkan token API di [replicate.com](https://replicate.com)
3. Tetapkan di `.env`:
   - `IMAGE_API_TYPE=replicate`
   - `IMAGE_API_KEY=your_replicate_token`

## 📁 Struktur Proyek

```
nanobanana/
├── src/
│   ├── bot.py              # File utama bot
│   └── image_generator.py  # Modul penghasil gambar
├── images/                 # Direktori untuk gambar yang dihasilkan
├── logs/                   # Direktori untuk log
├── config/                 # File konfigurasi
├── .env.example           # Contoh file dengan variabel lingkungan
├── .gitignore             # File Git ignore
├── requirements.txt       # Dependensi proyek
└── README.md              # Dokumentasi
```

## 🐛 Pemecahan Masalah

- **Bot tidak merespons**: Periksa kebenaran token di `.env`
- **Kesalahan penggabungan**: Pastikan kunci API ditentukan dengan benar dan Anda memiliki akses ke layanan pilihan
- **Kesalahan impor**: Pastikan semua dependensi terinstal (`pip install -r requirements.txt`)

## 📝 Lisensi

MIT

## 🤝 Kontribusi

Semua peningkatan dan saran diterima dengan baik!
