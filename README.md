# 🤖 NLP ile Otomatik Test Senaryosu Üretimi

Bu proje, yazılım gereksinim dokümanlarından otomatik olarak test senaryoları üreten bir NLP tabanlı sistemdir. Google Gemini AI modellerini kullanarak, gereksinim metinlerini analiz eder ve kapsamlı test senaryoları oluşturur.

## 📋 İçindekiler

- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Sistem Mimarisi](#sistem-mimarisi)
- [Performans Metrikleri](#performans-metrikleri)
- [Test ve Değerlendirme](#test-ve-değerlendirme)
- [Dokümantasyon](#dokümantasyon)

## ✨ Özellikler

- ✅ **Çoklu Format Desteği**: PDF, DOCX, DOC ve TXT dosyalarından metin çıkarma
- ✅ **AI Destekli Test Üretimi**: Google Gemini modelleri ile otomatik test senaryosu oluşturma
- ✅ **Performans Ölçümü**: Detaylı metrikler ve istatistikler
- ✅ **Kalite Değerlendirmesi**: Üretilen test senaryolarının otomatik değerlendirmesi
- ✅ **Karşılaştırma Analizi**: Manuel vs otomatik test üretimi karşılaştırması
- ✅ **Görselleştirme**: Grafikler ve tablolar ile sonuç görselleştirme
- ✅ **İndirme**: JSON formatında sonuç indirme

## 🚀 Kurulum

### Gereksinimler

- Python 3.8+
- Google Generative AI API anahtarı

### Adım 1: Projeyi Klonlayın

```bash
git clone https://github.com/cemresude/test_projesi.git
cd test_projesi
```

### Adım 2: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 3: API Anahtarı Alın

1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
2. API anahtarınızı oluşturun
3. Anahtarı kopyalayın (uygulamada kullanılacak)

### Adım 4: Uygulamayı Çalıştırın

```bash
streamlit run test_generate.py
```

Tarayıcınızda `http://localhost:8501` adresinde uygulama açılacaktır.

## 📖 Kullanım

### Temel Kullanım

1. **Dosya Yükleme**: Sol menüden gereksinim dokümanınızı yükleyin (.txt, .pdf, .doc, .docx)
2. **Model Seçimi**: Kullanmak istediğiniz AI modelini seçin
3. **API Anahtarı**: Google API anahtarınızı girin
4. **Test Üretimi**: "Test Senaryolarını Otomatik Oluştur" butonuna tıklayın
5. **Sonuçları İncele**: Üretilen test senaryolarını ve metrikleri inceleyin
6. **İndirme**: Sonuçları JSON formatında indirin

### Sekmeler

- **🏠 Ana Sayfa**: Test senaryosu üretimi
- **📊 Performans Metrikleri**: Detaylı performans analizleri
- **⚖️ Karşılaştırma**: Manuel vs otomatik karşılaştırma
- **📖 Dokümantasyon**: Sistem dokümantasyonu

## 🏗️ Sistem Mimarisi

### Ana Bileşenler

```
test_projesi/
├── test_generate.py      # Ana Streamlit uygulaması
├── parser.py             # Dosya parsing modülü
├── metrics.py            # Performans ölçümü ve değerlendirme
├── comparison.py         # Karşılaştırma modülü
└── requirements.txt      # Python bağımlılıkları
```

### Modül Açıklamaları

#### 1. parser.py
- PDF, DOCX, DOC ve TXT dosyalarından metin çıkarma
- Çeşitli formatları destekleme
- Metin temizleme ve işleme

#### 2. metrics.py
- Performans ölçümleri (zaman, süre, vb.)
- Test senaryosu kalite değerlendirmesi
- İstatistiksel analizler
- Metrik geçmişi yönetimi

#### 3. comparison.py
- Manuel vs otomatik test üretimi karşılaştırması
- Verimlilik analizleri
- Kapsam karşılaştırması

#### 4. test_generate.py
- Streamlit tabanlı kullanıcı arayüzü
- AI model entegrasyonu
- Sonuç görselleştirme
- İndirme özellikleri

## 📊 Performans Metrikleri

Sistem aşağıdaki metrikleri ölçer ve kaydeder:

### Zaman Metrikleri
- **İşlem Süresi**: Toplam işlem süresi (saniye)
- **Parsing Süresi**: Dosya parsing süresi (saniye)
- **AI Süresi**: AI model yanıt süresi (saniye)

### Kalite Metrikleri
- **Kalite Skoru**: Test senaryolarının genel kalite skoru (%)
- **Geçerli Yapı**: Standart yapıya uygun test senaryoları yüzdesi
- **Kapsam**: Ön koşul, adımlar ve beklenen sonuç varlığı
- **Test Sayısı**: Üretilen toplam test senaryosu sayısı

### Değerlendirme Kriterleri
- Test senaryosu yapısı (id, başlık, ön koşul, adımlar, beklenen sonuç)
- İçerik bütünlüğü
- Detay düzeyi

## 🧪 Test ve Değerlendirme

### Test Senaryosu Formatı

Üretilen test senaryoları şu formatta JSON dosyası olarak kaydedilir:

```json
[
  {
    "id": "TC001",
    "baslik": "Test Senaryosu Başlığı",
    "on_kosul": "Ön koşullar",
    "adimlar": "Test adımları",
    "beklenen_sonuc": "Beklenen sonuç"
  }
]
```

### Örnek Kullanım Senaryoları

1. **Basit Gereksinim Dokümanı**: Kısa metin içeren gereksinim dokümanları
2. **Kapsamlı SRS**: Detaylı yazılım gereksinim spesifikasyonları
3. **Use Case Dokümanları**: Kullanım senaryosu açıklamaları
4. **Teknik Dokümantasyon**: Teknik özellikler ve gereksinimler

### Karşılaştırma Yöntemi

1. Manuel olarak hazırlanmış test senaryolarını JSON formatında yükleyin
2. Otomatik üretilen test senaryolarını kullanın
3. Sistem karşılaştırma analizi yapar:
   - Test sayısı karşılaştırması
   - Detay düzeyi analizi
   - Kapsam karşılaştırması
   - Verimlilik metrikleri

## 📈 Sonuçlar ve Loglar

### Çıktı Dosyaları

- `test_senaryolari.json`: Üretilen test senaryoları
- `metrics.json`: Performans metrikleri geçmişi
- `comparisons.json`: Karşılaştırma sonuçları

### Görselleştirmeler

- İşlem süresi grafikleri
- Test sayısı grafikleri
- Kalite skoru trendleri
- Karşılaştırma sonuçları

## 🔧 Gelişmiş Özellikler

### Model Seçimi

Farklı Gemini modelleri arasında seçim yapabilirsiniz:
- `gemini-2.5-flash`: Hızlı yanıt süresi
- `gemini-2.5-pro`: Daha detaylı analiz
- `gemini-2.0-flash`: Deneysel özellikler

### Metrik Kaydı

Performans metriklerini kaydetme özelliği açık/kapalı yapılabilir. Metrikler `metrics.json` dosyasına kaydedilir.

## 📝 Örnek Test Senaryoları

Proje klasöründe örnek gereksinim dokümanları bulunmaktadır:
- `cikti.txt`: Örnek çıktı metni
- `SRSSample.doc`: Örnek SRS dokümanı
- `final_report.pdf`: Örnek PDF dokümanı

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📄 Lisans

Bu proje test amaçlı geliştirilmiştir.

## 👥 Yazarlar

- Proje Ekibi

## 🙏 Teşekkürler

- Google Gemini AI
- Streamlit ekibi
- Açık kaynak topluluğu

## 📞 İletişim

Sorularınız için issue açabilirsiniz.

---

**Not**: Bu proje, yazılım kalite güvencesi ve testi dersi kapsamında geliştirilmiştir.

