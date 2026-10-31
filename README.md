# Yapay Zeka (OCR) Destekli Akıllı Harcama ve Fiş Yönetim Sistemi

Bu proje, fiş veya fatura görsellerinden OCR kullanarak harcama bilgilerini
otomatik çıkaran, bilgileri SQLite veritabanında saklayan ve Streamlit
üzerinden raporlayan bir Python uygulamasıdır.

## Proje kapsamı

- Kullanıcı fiş/fatura görseli yükler.
- OCR katmanı görseldeki metni okur.
- Ayrıştırma katmanı tarih, toplam tutar ve kategori bilgisini çıkarır.
- Sistem bilgileri SQLite veritabanına kaydeder.
- Streamlit arayüzü kayıtları ve harcama grafiklerini gösterir.
- Tarih, tutar veya kategori için manuel veri giriş formu bulunmaz.

## Dört sprintlik Agile plan

### Sprint 1 - Analiz ve temel proje yapısı

- Gereksinimleri ve kullanıcı senaryolarını netleştirme
- Katmanlı mimariyi belirleme
- Proje klasör yapısını oluşturma
- Git deposunu ve `.gitignore` dosyasını hazırlama

**Kabul ölçütü:** Proje iskeleti açılabiliyor ve katmanların sorumlulukları
belgelenmiş durumda.

### Sprint 2 - OCR ve veri katmanı

- Tesseract/Pytesseract ile görselden metin okuma
- Tarih ve toplam tutar ayrıştırma
- Kategori belirleme kuralının uygulanması
- SQLite şeması ve kayıt işlemleri

**Kabul ölçütü:** Örnek bir fiş görselinden çıkarılan veriler SQLite'a
kaydedilebiliyor.

### Sprint 3 - Streamlit arayüzü

- Fiş yükleme ekranı
- OCR sonucunun kullanıcıya gösterilmesi
- Otomatik kayıt akışı
- Harcama listesi ve temel grafikler

**Kabul ölçütü:** Kullanıcı yalnızca görsel yükleyerek yeni bir harcama
kaydını oluşturabiliyor.

### Sprint 4 - Doğrulama ve teslim

- OCR ayrıştırma birim testleri
- SQLite repository birim testleri
- Hata mesajları ve geçersiz görsel kontrolleri
- Kullanıcı kabul testi ve proje dokümantasyonu

**Kabul ölçütü:** Testler başarılı ve uygulama ders sunumunda çalıştırılabilir
durumda.

## Mimari

Uygulama basit bir katmanlı mimari kullanır:

```text
Streamlit UI
    |
Service Layer
    |
OCR / Parser Layer
    |
Repository / Data Access Layer
    |
SQLite
```

- `app.py`: Uygulama giriş noktası ve Streamlit ekranı
- `src/ocr`: Görselden metin okuma ve alan ayrıştırma
- `src/services`: Uygulama iş akışları
- `src/database`: SQLite bağlantısı ve kayıt sorguları
- `src/models`: Harcama veri modelleri
- `src/config`: Uygulama ayarları
- `tests`: Birim testleri

## Geliştirme sırası

1. Proje iskeleti ve Git kurulumu
2. OCR prototipi
3. SQLite veri katmanı
4. OCR-servis-veritabanı entegrasyonu
5. Streamlit arayüzü
6. Testler ve son düzenlemeler

## Sprint 2 çalışma notları

OCR için Python tarafında `pytesseract` ve görüntü açmak için Pillow kullanılır.
`pytesseract` yalnızca Python aracıdır; bilgisayarda Tesseract OCR motorunun da
kurulu olması gerekir. Türkçe fişler için Tesseract'ın `tur` dil veri dosyası
kurulmalıdır.

Bağımlılıkları proje klasöründe şu komutla kurabilirsiniz:

```powershell
python -m pip install -r requirements.txt
```

Sprint 2 bileşenleri:

- `src/ocr/reader.py`: Görsel dosyasını Tesseract'a gönderir.
- `src/ocr/parser.py`: Tarih, toplam tutar ve anahtar kelime tabanlı kategori çıkarır.
- `src/database/connection.py`: SQLite veritabanını ve `expenses` tablosunu oluşturur.
- `src/database/repository.py`: OCR sonucu oluşan harcama kayıtlarını ekler ve listeler.
- `src/services/expense_service.py`: OCR, ayrıştırma ve veritabanı kayıt akışını birleştirir.
- `run.py`: Sprint 2 için komut satırından çalıştırılabilir giriş noktasıdır.

### Sprint 2'yi çalıştırma

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py "uploads\ornek-fis.jpg"
```

Komut; görseli OCR ile okur, tarih/tutar/kategori alanlarını çıkarır ve
`data/expenses.sqlite` dosyasına kaydeder. Tesseract OCR ve `tur` dil verisi
kurulu olmalıdır. Kurulum yolu standart Windows yolu değilse
`src/config/settings.py` içindeki `TESSERACT_COMMAND` değeri güncellenebilir.
