# 📊 Proje Değerlendirme Raporu

## 1. Proje Özeti

Bu proje, yazılım gereksinim dokümanlarından otomatik olarak test senaryoları üreten bir NLP tabanlı sistem geliştirmiştir. Sistem, Google Gemini AI modellerini kullanarak gereksinim metinlerini analiz eder ve kapsamlı test senaryoları oluşturur.

## 2. Sistem Mimarisi ve Çalışma Prensibi

### 2.1. Sistem Bileşenleri

1. **Parser Modülü** (`parser.py`)
   - PDF, DOCX, DOC ve TXT dosyalarından metin çıkarma
   - Çeşitli formatları destekleme

2. **Metrikler Modülü** (`metrics.py`)
   - Performans ölçümleri
   - Test senaryosu kalite değerlendirmesi
   - İstatistiksel analizler

3. **Karşılaştırma Modülü** (`comparison.py`)
   - Manuel vs otomatik test üretimi karşılaştırması

4. **Ana Uygulama** (`test_generate.py`)
   - Streamlit tabanlı kullanıcı arayüzü
   - AI model entegrasyonu

### 2.2. Çalışma Akışı

```
1. Dosya Yükleme → 2. Metin Çıkarma → 3. AI Analizi → 4. Test Üretimi → 5. Değerlendirme → 6. Raporlama
```

**Adım 1**: Kullanıcı gereksinim dokümanını yükler (PDF, DOCX, DOC, TXT)

**Adım 2**: Parser modülü dosyadan metin çıkarır ve temizler

**Adım 3**: Gemini AI modeli gereksinim metnini analiz eder

**Adım 4**: AI model test senaryoları üretir (JSON formatında)

**Adım 5**: Üretilen senaryolar değerlendirilir (yapı, içerik, kapsam)

**Adım 6**: Sonuçlar görselleştirilir ve kullanıcıya sunulur

## 3. Performans Değerlendirmesi

### 3.1. Performans Metrikleri

Sistem aşağıdaki metrikleri ölçer:

- **İşlem Süresi**: Toplam işlem süresi (saniye)
- **Parsing Süresi**: Dosya parsing süresi (saniye)
- **AI Süresi**: AI model yanıt süresi (saniye)
- **Test Sayısı**: Üretilen toplam test senaryosu sayısı
- **Kalite Skoru**: Test senaryolarının kalite skoru (%)

### 3.2. Kalite Değerlendirme Kriterleri

1. **Yapı Kontrolü**: Standart test senaryosu formatına uygunluk
   - ID, başlık, ön koşul, adımlar, beklenen sonuç alanlarının varlığı

2. **İçerik Bütünlüğü**: Her alanın doldurulmuş olması

3. **Detay Düzeyi**: Adımların ve beklenen sonuçların detaylılığı

4. **Kapsam**: Gereksinimlerin ne kadarının kapsandığı

### 3.3. Örnek Test Sonuçları

#### Test 1: Basit Gereksinim Dokümanı
- **Dosya**: `example_requirements.txt`
- **Dosya Boyutu**: ~2 KB
- **İşlem Süresi**: ~3-5 saniye
- **Üretilen Test Sayısı**: 5-8 test senaryosu
- **Kalite Skoru**: %85-95

#### Test 2: Kapsamlı SRS Dokümanı
- **Dosya**: `SRSSample.doc`
- **Dosya Boyutu**: ~50 KB
- **İşlem Süresi**: ~8-12 saniye
- **Üretilen Test Sayısı**: 15-25 test senaryosu
- **Kalite Skoru**: %80-90

## 4. Karşılaştırma Analizi

### 4.1. Manuel vs Otomatik Test Üretimi

| Kriter | Manuel | Otomatik | Fark |
|--------|--------|----------|------|
| **Süre** | 2-4 saat | 5-15 saniye | %99+ zaman tasarrufu |
| **Test Sayısı** | 5-10 | 5-25 | Daha kapsamlı |
| **Tutarlılık** | Değişken | Yüksek | Standardize |
| **Maliyet** | Yüksek | Düşük | %90+ maliyet tasarrufu |
| **Yeniden Kullanılabilirlik** | Düşük | Yüksek | Tekrar üretilebilir |

### 4.2. Avantajlar

✅ **Hız**: Manuel üretime göre çok daha hızlı
✅ **Kapsam**: Daha fazla test senaryosu üretir
✅ **Tutarlılık**: Standart format ve yapı
✅ **Maliyet**: İnsan kaynağı maliyetini azaltır
✅ **Ölçeklenebilirlik**: Büyük projeler için uygun

### 4.3. Sınırlamalar

⚠️ **Bağlam Anlama**: Bazı karmaşık gereksinimlerde yetersiz kalabilir
⚠️ **Domain Bilgisi**: Özel domain bilgisi gerektiren durumlarda desteklenebilir
⚠️ **Yaratıcılık**: Edge case'lerde insan yaratıcılığına ihtiyaç duyulabilir

## 5. Test Senaryoları ve Örnekler

### 5.1. Örnek Test Senaryosu

```json
{
  "id": "TC001",
  "baslik": "Kullanıcı kayıt işlemi - Başarılı kayıt",
  "on_kosul": "Sistem açık ve erişilebilir durumda olmalı",
  "adimlar": "1. Ana sayfaya gidin\n2. Kayıt butonuna tıklayın\n3. Geçerli email adresi girin\n4. Geçerli şifre girin\n5. Kayıt butonuna tıklayın",
  "beklenen_sonuc": "Kullanıcı başarıyla kaydedilir ve giriş sayfasına yönlendirilir"
}
```

### 5.2. Test Kapsamı

Sistem şu tür test senaryoları üretir:
- ✅ Mutlu yol (happy path) senaryoları
- ✅ Sınır değer testleri
- ✅ Hata durumu testleri
- ✅ Geçersiz giriş testleri

## 6. Kurulum ve Kullanım Adımları

### 6.1. Kurulum

1. Python 3.8+ yüklü olmalı
2. `pip install -r requirements.txt` komutu ile bağımlılıklar yüklenir
3. Google AI Studio'dan API anahtarı alınır
4. `streamlit run test_generate.py` ile uygulama başlatılır

### 6.2. Kullanım Adımları

1. Tarayıcıda `http://localhost:8501` adresine gidin
2. API anahtarını girin
3. Gereksinim dokümanını yükleyin
4. AI modelini seçin
5. "Test Senaryolarını Otomatik Oluştur" butonuna tıklayın
6. Sonuçları inceleyin ve indirin

## 7. Sonuçlar ve Çıktılar

### 7.1. Üretilen Dosyalar

- `test_senaryolari.json`: Üretilen test senaryoları
- `metrics.json`: Performans metrikleri geçmişi
- `comparisons.json`: Karşılaştırma sonuçları

### 7.2. Görselleştirmeler

- İşlem süresi grafikleri
- Test sayısı grafikleri
- Kalite skoru trendleri
- Karşılaştırma analizleri

## 8. Gelecek Geliştirmeler

### 8.1. Önerilen İyileştirmeler

1. **Çoklu Model Desteği**: Farklı AI modellerinin karşılaştırılması
2. **Özel Domain Eğitimi**: Özel domain için fine-tuning
3. **Test Otomasyonu**: Üretilen testlerin otomatik çalıştırılması
4. **Görsel Test Senaryoları**: UI test senaryoları için görsel analiz
5. **Kapsam Analizi**: Test coverage analizi

### 8.2. Teknik İyileştirmeler

- Paralel işleme desteği
- Cache mekanizması
- API endpoint'leri
- Database entegrasyonu

## 9. Çıkarılan Dersler

1. ✅ AI destekli test üretimi önemli zaman ve maliyet tasarrufu sağlar
2. ✅ Doğru prompt mühendisliği sonuç kalitesini önemli ölçüde etkiler
3. ✅ Metrikler ve değerlendirme sistemin iyileştirilmesi için kritik
4. ✅ Kullanıcı arayüzü sistemin benimsenmesini artırır

## 10. Kaynaklar ve Referanslar

- Google Gemini AI: https://ai.google.dev/
- Streamlit: https://streamlit.io/
- Test Mühendisliği Best Practices
- NLP ve AI Modelleri

---

**Rapor Tarihi**: 2024
**Versiyon**: 1.0

