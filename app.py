import csv
import streamlit as st

# --- Fungsi untuk load data ---
def load_news(filename):
    """Baca file news_data.csv ke list of dict"""
    # TODO: buka file CSV (filename) dan baca dengan csv.DictReader
    # kembalikan hasilnya dalam bentuk list
    with open(filename, 'r', newline='', encoding='utf-8') as datafile:
        reader = csv.DictReader(datafile)
        news = []
        for row in reader:
            row['idBerita'] = int(row['idBerita'])
            row['Headline'] = row.get('Headline', '')
            row['content'] = row.get('content', '')  # pastikan konten ada
            news.append(row)
        return news

def load_comments(filename):
    """Baca file comment_news.csv ke list of dict"""
    # TODO: sama seperti load_news tapi untuk file komentar
    with open(filename, 'r', newline='', encoding='utf-8') as datafile:
        reader = csv.DictReader(datafile)
        comments = []
        for row in reader:
            row['idKomentar'] = int(row['idKomentar'])
            row['idBerita'] = int(row['idBerita'])
            row['Rating'] = int(row['Rating'])
            comments.append(row)
        return comments

# --- Fungsi untuk memproses data ---
def process_data(news_list, comments_list):
    """
    Gabungkan berita dan komentar,
    hitung jumlah komentar & rata-rata rating.
    Hasilnya list of dict.
    """
    # TODO: Buat dictionary untuk kumpulkan komentar per idBerita
    comments_per_news = {}
    for c in comments_list:
        idb = c['idBerita']
        if idb not in comments_per_news:
            comments_per_news[idb] = {'ratings': [], 'count': 0}
        comments_per_news[idb]['ratings'].append(c['Rating'])
        comments_per_news[idb]['count'] += 1

    # TODO: isi comments_per_news dari comments_list
    # hint: per idBerita simpan ratings (list) dan count

    # TODO: Buat list hasil gabungan
    result = []
    for n in news_list:
        idb = n['idBerita']
        headline = n.get('Headline', '')
        content = n.get('content', '')  # ambil konten jika ada
        # TODO: cek apakah idb ada di comments_per_news,
        # hitung rata-rata rating dan jumlah komentar
        if idb in comments_per_news:
            ratings = comments_per_news[idb]['ratings']
            jumlah = comments_per_news[idb]['count']
            rata = sum(ratings) / jumlah if jumlah > 0 else 0
        else:
            jumlah = 0
            rata = 0
        result.append({
            'ID Berita': idb,
            'Headline': headline,
            'Konten': content,
            'Rata-rata Rating': round(rata, 2),
            'Jumlah Komentar': jumlah
        })

    # --- Urutkan berdasarkan rating pakai fungsi biasa ---
    def ambil_rating(item):
        return item['Rata-rata Rating']

    # TODO: urutkan result berdasarkan ambil_rating reverse=True
    result = sorted(result, key=ambil_rating, reverse=True)
    return result

# --- Fungsi untuk tampilkan di Streamlit ---
def main():
    st.title("Analisis Sentimen & Popularitas Berita")
    st.write("Menampilkan ID, Headline, Konten, Rata-rata Rating, dan Jumlah Komentar, diurutkan dari rating tertinggi.")

    # TODO: baca data CSV
    news_data = load_news('news_data.csv') 
    comment_data = load_comments('comment_news.csv')

    # TODO: proses data
    hasil = process_data(news_data, comment_data) # ganti dengan pemanggilan process_data

    # TODO: tampilkan tabel di Streamlit
    # hint: gunakan st.table(hasil)
    st.table(hasil)

if __name__ == '__main__':
    main()
