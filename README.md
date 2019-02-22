# Tugas_URO_Day_3

## Anggota
- Reinard R.      16718135
- Naufal Dean A.  16518160
- Annisa Ayu P.   16518046
- Tommy Wiranata  16918167

## Strategi
Pertama, untuk 10 turn pertama, kita fokus pada ekspansi wilayah, pod yang ada dibagi menjadi 2 tiap turnnya (dengan minimum pod yang digerakkan adalah 1). Setelah turn 10, jumlah pergerakan podnya sedikit diubah (menjadi (pod * 3 // 2) + 1).

Kedua, untuk arah pergerakan, kita gunakan suatu decision weight, sehingga pod akan cenderung bergerak menuju lokasi dengan value yang lebih tinggi, sesuai decision weight yang ada pada zona tersebut.

Ketiga, kita arahkan pod yang baru spawn ke perbatasan terluar zona yang telah kita kuasai. Hal ini dilakukan agar tidak terjadi penumpukan pod di sekitar HQ di mid-late game akibat decision weight yang cenderung sama, mengingat zona sekitar HQ cukup homogen dan mayoritas telah kita kuasai.

Keempat, jika arah yang kita tuju ternyata merupakan jalan buntu (dead end), kita beri kecenderungan pod lainnya untuk mengarah ke tempat lain.

Kelima, salah satu faktor pada decision weight yang cukup penting adalah kita buat pod milik kita mengejar pod musuh yang berada di zona yang bersambung dengan lokasi pod kita.
