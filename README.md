# ChartYap V2 - Akıllı Grafik Öneri ve Oluşturma Uygulaması

**ChartYap**, verilerinizi görselleştirmenize yardımcı olan modern bir web uygulamasıdır. CSV formatındaki verilerinizi yükleyerek, yapay zeka destekli analizler sayesinde en uygun grafik türlerini keşfedebilir ve anında görselleştirebilirsiniz.

## 🚀 Özellikler

- **Kolay Veri Yükleme:** Sürükle-bırak yöntemiyle CSV dosyalarını kolayca yükleyin.
- **Akıllı Analiz:** Python destekli backend, verilerinizi analiz eder ve değişken türlerini (sayısal, kategorik, tarihsel vb.) otomatik olarak algılar.
- **Grafik Önerileri:** Veri türlerinize en uygun grafik türlerini (Bar, Line, Scatter, Pie vb.) önerir.
- **Anında Görselleştirme:** Seçtiğiniz grafik türünü interaktif olarak görüntüleyin.
- **Modern Arayüz:** Kullanıcı dostu ve şık "Swiss Design" estetiği.

## 🛠️ Teknolojiler

**Frontend:**
- React (Vite ile)
- TypeScript
- Tailwind CSS (Stil)
- Lucide React (İkonlar)

**Backend:**
- Python
- FastAPI / Uvicorn (Sunucu)
- Pandas (Veri İşleme)

## 📦 Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

### Ön Gereksinimler
- Node.js (Frontend için)
- Python 3.8+ (Backend için)

### 1. Projeyi Klonlayın

```bash
git clone https://github.com/mustafa-karakoyun/ChartYapV2.git
cd ChartYapV2
```

### 2. Otomatik Başlatma (Windows)

En kolay yöntem, ana dizinde bulunan `run_app.bat` dosyasını kullanmaktır. Bu dosya hem backend hem de frontend sunucularını otomatik olarak başlatır.

Çalıştırmak için `run_app.bat` dosyasına çift tıklayın veya terminalden şunu yazın:

```cmd
.\run_app.bat
```

### 3. Manuel Kurulum (Alternatif)

Eğer manuel olarak kurmak isterseniz:

**Backend:**

```bash
cd backend
python -m venv venv
# Windows için:
venv\Scripts\activate
# Mac/Linux için:
# source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**

Yeni bir terminal açın ve:

```bash
cd frontend
npm install
npm run dev
```

## 📝 Kullanım

1.  Uygulama açıldığında (genellikle http://localhost:5173), ana sayfadaki yükleme alanına bir CSV dosyası sürükleyin. (Örnek veriler: `sample_sales_data.csv` veya `sample_pie_data.csv`)
2.  Veri önizlemesini kontrol edin.
3.  Sağ taraftaki panelden önerilen grafik türlerinden birini seçin.
4.  Grafiğiniz anında oluşturulacaktır!

---
*Geliştirici: Mustafa Karakoyun*
