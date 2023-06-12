import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title("Uji Hipotesis Rata-rata Dua Populasi")
    
    # Masukkan data dari pengguna
    st.subheader("Masukkan Data Populasi Pertama:")
    data_pop1 = st.text_area("Masukkan data populasi pertama, dipisahkan dengan koma (misal: 1,2,3,4)")
    
    st.subheader("Masukkan Data Populasi Kedua:")
    data_pop2 = st.text_area("Masukkan data populasi kedua, dipisahkan dengan koma (misal: 1,2,3,4)")
    
    # Mengonversi data menjadi array numpy
    try:
        pop1 = np.array([float(x.strip()) for x in data_pop1.split(",")])
        pop2 = np.array([float(x.strip()) for x in data_pop2.split(",")])
    except:
        st.error("Terjadi kesalahan dalam memproses data. Pastikan format input benar.")
        return
    
    # Menampilkan data
    st.subheader("Data Populasi Pertama:")
    st.write(pop1)
    
    st.subheader("Data Populasi Kedua:")
    st.write(pop2)

    show_boxplot = st.checkbox("Tampilkan Boxplot")

    if show_boxplot:
        fig, ax = plt.subplots()
        ax.boxplot([pop1, pop2])

        ax.set_title('Boxplot Data Populasi')
        ax.set_xlabel('Populasi')
        ax.set_ylabel('Nilai')

        st.pyplot(fig)

    
    # Menghitung statistik uji
    mean1 = np.mean(pop1)
    mean2 = np.mean(pop2)
    std1 = np.std(pop1, ddof=1)
    std2 = np.std(pop2, ddof=1)
    n1 = len(pop1)
    n2 = len(pop2)
    
    # Menghitung perbedaan rata-rata dan kesalahan standar perbedaan rata-rata
    diff_mean = mean1 - mean2
    se_diff = np.sqrt((std1**2 / n1) + (std2**2 / n2))
    
    # Menghitung z-score
    z_score = diff_mean / se_diff
    
    # Menghitung p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
    
    # Menampilkan hasil uji hipotesis
    st.subheader("Hasil Uji Hipotesis:")
    st.write("Rata-rata Populasi Pertama:", mean1)
    st.write("Rata-rata Populasi Kedua:", mean2)
    st.write("Perbedaan Rata-rata:", diff_mean)
    st.write("Kesalahan Standar Perbedaan Rata-rata:", se_diff)
    st.write("Z-Score:", z_score)

    show_graph = st.checkbox("Tampilkan Grafik Z")

    if show_graph:
        x = np.linspace(-3.59, 3.59, 100)
        dist = stats.norm(loc=0, scale=se_diff)

        plt.plot(x, dist.pdf(x), label='Distribusi Normal')
        plt.fill_between(x, dist.pdf(x), where= (x >= 1.96), color='grey', alpha=0.5)
        plt.fill_between(x, dist.pdf(x), where= (x <= -1.96), color='grey', alpha=0.5)
        plt.axvline(x=z_score, color='red', linestyle='--', label='Z-Score')
        plt.xlabel("Z-Score")
        plt.ylabel("Density")
        plt.legend()
        st.pyplot()


    st.write("Nilai p-value:", p_value)
    
if __name__ == "__main__":
    main()
