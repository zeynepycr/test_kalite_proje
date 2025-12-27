import streamlit as st
import google.generativeai as genai
import json
import os
import tempfile
import time
from dotenv import load_dotenv
from parser import extract_text_from_pdf, extract_text_from_docx
from metrics import PerformanceMetrics, TestCaseEvaluator, load_metrics_history, get_aggregate_statistics
from comparison import ManualVsAutomatedComparison
import pandas as pd

# 2. Sayfa Ayarları
st.set_page_config(page_title="Otomatik Test Üretici", layout="wide")
st.title("🤖 NLP ile Gereksinimlerden Test Senaryosu Çıkarma")
st.markdown("Yazılım Kalite Güvencesi ve Testi Projesi")

# Sekmeler (Tabs) oluştur
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Ana Sayfa", "📊 Performans Metrikleri", "⚖️ Karşılaştırma", "📖 Dokümantasyon"])

# 3. Kenar Çubuğu (Sidebar) - Dosya Yükleme
with st.sidebar:
    api_key = st.text_input("Google API Anahtarınızı Girin:", type="password")
    st.header("Veri Girişi")
    uploaded_file = st.file_uploader("Gereksinim dosyasını yükleyin", type=["txt", "pdf", "doc", "docx"])
    
    st.divider()
    st.header("⚙️ Ayarlar")
    # Model Seçimi (Opsiyonel)
    model_type = st.selectbox("Model Seçin", [
        "models/gemini-2.5-flash",
        "models/gemini-2.5-pro",
        "models/gemini-2.0-flash-exp",
        "models/gemini-2.0-flash",
        "models/gemini-2.0-flash-001",
        "models/gemini-2.0-flash-exp-image-generation",
        "models/gemini-2.0-flash-lite-001",
        "models/gemini-2.0-flash-lite",
        "models/gemini-2.0-flash-lite-preview-02-05",
        "models/gemini-2.0-flash-lite-preview",
        "models/gemini-exp-1206",
        "models/gemini-2.5-flash-preview-tts",
        "models/gemini-2.5-pro-preview-tts",
        "models/gemma-3-1b-it",
        "models/gemma-3-4b-it",
        "models/gemma-3-12b-it",
        "models/gemma-3-27b-it",
        "models/gemma-3n-e4b-it",
        "models/gemma-3n-e2b-it",
        "models/gemini-flash-latest",
        "models/gemini-flash-lite-latest",
        "models/gemini-pro-latest",
        "models/gemini-2.5-flash-lite",
        "models/gemini-2.5-flash-image-preview",
        "models/gemini-2.5-flash-image",
        "models/gemini-2.5-flash-preview-09-2025",
        "models/gemini-2.5-flash-lite-preview-09-2025",
        "models/gemini-3-pro-preview",
        "models/gemini-3-flash-preview",
        "models/gemini-3-pro-image-preview",
        "models/nano-banana-pro-preview",
        "models/gemini-robotics-er-1.5-preview",
        "models/gemini-2.5-computer-use-preview-10-2025",
        "models/deep-research-pro-preview-12-2025",
    ])
    
    save_metrics = st.checkbox("📊 Performans metriklerini kaydet", value=True)

# 4. API Anahtarı Kontrolü
if not api_key:
    st.error("⚠️ Lütfen API anahtarınızı sol menüden tanımlayın!")
    st.stop()
else:
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"API anahtarı hatası: {e}")
        st.stop()

# Ana Sekme 1: Test Senaryosu Üretimi
with tab1:
    if uploaded_file is not None:
        # Performans metrikleri başlat
        metrics = PerformanceMetrics()
        file_size = len(uploaded_file.getvalue())
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        # Dosya içeriğini okuma
        try:
            metrics.start_parsing()
            
            if file_extension == '.txt':
                stringio = uploaded_file.getvalue().decode("utf-8")
            elif file_extension == '.pdf':
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                try:
                    stringio = extract_text_from_pdf(tmp_path)
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
            elif file_extension in ['.doc', '.docx']:
                if file_extension == '.doc':
                    st.warning("⚠️ .doc dosyaları tam desteklenmeyebilir. .docx formatını tercih edin.")
                suffix = '.docx' if file_extension == '.docx' else '.doc'
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                try:
                    stringio = extract_text_from_docx(tmp_path)
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
            else:
                st.error(f"Desteklenmeyen dosya formatı: {file_extension}")
                st.stop()
            
            metrics.end_parsing()
            metrics.start_processing(uploaded_file.name, file_extension, file_size, len(stringio))
            
            st.subheader("📄 Yüklenen Gereksinim Dokümanı")
            with st.expander("📖 Doküman İçeriğini Göster/Gizle"):
                st.text_area("Doküman İçeriği", stringio, height=200, label_visibility="collapsed")
            
            st.info(f"📊 Doküman İstatistikleri: {len(stringio)} karakter, {len(stringio.split())} kelime")
            
        except Exception as e:
            st.error(f"❌ Dosya okuma hatası: {str(e)}")
            metrics.end_processing([], False, str(e))
            st.stop()
        
        if st.button("🚀 Test Senaryolarını Otomatik Oluştur", type="primary"):
            with st.spinner("🤖 Yapay zeka gereksinimleri analiz ediyor..."):
                try:
                    metrics.start_ai_generation(model_type)
                    
                    # Gemini'ye Gönderilecek Prompt
                    prompt = f"""
                    Sen uzman bir Yazılım Test Mühendisisin.
                    Aşağıdaki gereksinim metnini analiz et.
                    Tüm olası sınır değerleri, hatalı girişleri ve mutlu yol (happy path) senaryolarını düşün.
                    
                    Gereksinim Metni:
                    "{stringio}"
                    
                    Çıktıyı SADECE aşağıdaki JSON formatında ver, başka bir açıklama yapma:
                    [
                      {{"id": "TC001", "baslik": "...", "on_kosul": "...", "adimlar": "...", "beklenen_sonuc": "..."}},
                      {{"id": "TC002", "baslik": "...", "on_kosul": "...", "adimlar": "...", "beklenen_sonuc": "..."}}
                    ]
                    """
                    
                    # Modeli çağırma
                    model = genai.GenerativeModel(model_type)
                    response = model.generate_content(prompt)
                    
                    metrics.end_ai_generation()
                    
                    # Gelen yanıtı JSON'a çevirip tablo yapma
                    try:
                        cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
                        data = json.loads(cleaned_text)
                        
                        # Metrikleri tamamla
                        metrics.end_processing(data, True)
                        if save_metrics:
                            metrics.save_to_file('metrics.json')
                        
                        # Test senaryolarını değerlendir
                        evaluator = TestCaseEvaluator()
                        evaluation = evaluator.evaluate_test_cases(data)
                        
                        st.success(f"✅ Toplam {len(data)} adet test senaryosu oluşturuldu!")
                        
                        # Performans bilgileri
                        perf_metrics = metrics.get_metrics()
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("⏱️ İşlem Süresi", f"{perf_metrics.get('processing_time', 0):.2f}s")
                        with col2:
                            st.metric("📄 Parsing Süresi", f"{perf_metrics.get('parsing_time', 0):.2f}s")
                        with col3:
                            st.metric("🤖 AI Süresi", f"{perf_metrics.get('ai_generation_time', 0):.2f}s")
                        with col4:
                            st.metric("📊 Kalite Skoru", f"{evaluation['coverage_score']:.1f}%")
                        
                        # Değerlendirme sonuçları
                        st.subheader("📈 Test Senaryosu Değerlendirmesi")
                        eval_col1, eval_col2, eval_col3, eval_col4 = st.columns(4)
                        with eval_col1:
                            st.metric("✅ Geçerli Yapı", f"{evaluation['valid_structure_percent']:.1f}%", f"{evaluation['valid_structure']}/{evaluation['total_count']}")
                        with eval_col2:
                            st.metric("📋 Ön Koşul Var", f"{evaluation['has_prerequisites_percent']:.1f}%", f"{evaluation['has_prerequisites']}/{evaluation['total_count']}")
                        with eval_col3:
                            st.metric("📝 Adımlar Var", f"{evaluation['has_steps_percent']:.1f}%", f"{evaluation['has_steps']}/{evaluation['total_count']}")
                        with eval_col4:
                            st.metric("🎯 Beklenen Sonuç", f"{evaluation['has_expected_result_percent']:.1f}%", f"{evaluation['has_expected_result']}/{evaluation['total_count']}")
                        
                        # Session state'e kaydet (karşılaştırma için)
                        st.session_state.last_generated_tests = data
                        st.session_state.last_requirement_text = stringio
                        
                        # Test senaryoları tablosu
                        st.subheader("📋 Üretilen Test Senaryoları")
                        st.dataframe(data, use_container_width=True)
                        
                        # İndirme butonları
                        col_dl1, col_dl2 = st.columns(2)
                        with col_dl1:
                            st.download_button(
                                label="📥 Testleri JSON Olarak İndir",
                                data=json.dumps(data, indent=4, ensure_ascii=False),
                                file_name="test_senaryolari.json",
                                mime="application/json"
                            )
                        with col_dl2:
                            # Metrikleri de indirebilir
                            metrics_json = json.dumps(perf_metrics, indent=2, ensure_ascii=False)
                            st.download_button(
                                label="📊 Metrikleri İndir",
                                data=metrics_json,
                                file_name=f"metrics_{time.strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json"
                            )
                        
                    except json.JSONDecodeError as e:
                        st.error("❌ Model çıktısı JSON formatında değil!")
                        st.warning("Ham metin çıktısı:")
                        st.code(response.text)
                        metrics.end_processing([], False, f"JSON parse hatası: {str(e)}")
                        if save_metrics:
                            metrics.save_to_file('metrics.json')
                        
                except Exception as e:
                    st.error(f"❌ Bir hata oluştu: {e}")
                    metrics.end_processing([], False, str(e))
                    if save_metrics:
                        metrics.save_to_file('metrics.json')
    else:
        st.info("📁 Lütfen sol menüden bir dosya yükleyin (.txt, .pdf, .doc, .docx formatlarında).")
        st.markdown("""
        ### 📌 Kullanım Adımları:
        1. **Dosya Yükleme**: Sol menüden gereksinim dokümanınızı yükleyin
        2. **Model Seçimi**: Kullanmak istediğiniz AI modelini seçin
        3. **Test Üretimi**: "Test Senaryolarını Otomatik Oluştur" butonuna tıklayın
        4. **Sonuçları İncele**: Üretilen test senaryolarını ve metrikleri inceleyin
        5. **İndirme**: Sonuçları JSON formatında indirin
        """)

# Sekme 2: Performans Metrikleri
with tab2:
    st.header("📊 Performans Metrikleri ve İstatistikler")
    
    metrics_file = 'metrics.json'
    if os.path.exists(metrics_file):
        metrics_history = load_metrics_history(metrics_file)
        
        if metrics_history:
            # Toplu istatistikler
            stats = get_aggregate_statistics(metrics_history)
            st.subheader("📈 Genel İstatistikler")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🔄 Toplam Çalıştırma", stats.get('total_runs', 0))
            with col2:
                st.metric("✅ Başarılı Çalıştırma", stats.get('successful_runs', 0))
            with col3:
                st.metric("⏱️ Ortalama İşlem Süresi", f"{stats.get('avg_processing_time', 0):.2f}s")
            with col4:
                st.metric("📋 Ortalama Test Sayısı", f"{stats.get('avg_test_cases', 0):.1f}")
            
            # Detaylı tablo
            st.subheader("📋 Detaylı Metrik Geçmişi")
            df = pd.DataFrame(metrics_history)
            
            # Sadece başarılı olanları göster
            if 'success' in df.columns:
                df_success = df[df['success'] == True].copy()
            else:
                df_success = df.copy()
            
            if not df_success.empty:
                # Tarih formatını düzelt
                if 'timestamp' in df_success.columns:
                    df_success['timestamp'] = pd.to_datetime(df_success['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # Gösterilecek kolonlar
                display_cols = ['timestamp', 'file_name', 'file_type', 'processing_time', 
                              'total_test_cases', 'model_name']
                available_cols = [col for col in display_cols if col in df_success.columns]
                st.dataframe(df_success[available_cols], use_container_width=True)
                
                # Grafikler
                st.subheader("📊 Grafik Analizleri")
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    if 'processing_time' in df_success.columns:
                        st.bar_chart(df_success.set_index('file_name')['processing_time'])
                        st.caption("📁 Dosya Bazında İşlem Süreleri")
                
                with chart_col2:
                    if 'total_test_cases' in df_success.columns:
                        st.bar_chart(df_success.set_index('file_name')['total_test_cases'])
                        st.caption("📋 Dosya Bazında Üretilen Test Sayıları")
            else:
                st.warning("📭 Başarılı çalıştırma bulunamadı.")
        else:
            st.info("📭 Henüz metrik kaydı yok. Ana sayfadan test senaryosu üretin.")
    else:
        st.info("📭 Henüz metrik dosyası oluşturulmamış. Ana sayfadan test senaryosu üretin.")

# Sekme 3: Karşılaştırma
with tab3:
    st.header("⚖️ Manuel vs Otomatik Test Üretimi Karşılaştırması")
    
    st.markdown("""
    Bu bölümde, manuel olarak hazırlanan test senaryoları ile otomatik üretilen test senaryolarını karşılaştırabilirsiniz.
    """)
    
    comparison_file = st.file_uploader("Manuel hazırlanmış test senaryolarını yükleyin (JSON formatında)", type=["json"])
    
    if comparison_file is not None:
        try:
            manual_data = json.load(comparison_file)
            
            # Otomatik üretilen testleri yükle (session state'den veya dosyadan)
            if 'last_generated_tests' in st.session_state and st.session_state.last_generated_tests:
                automated_data = st.session_state.last_generated_tests
                
                if st.button("🔄 Karşılaştır", type="primary"):
                    comparator = ManualVsAutomatedComparison()
                    comparison_result = comparator.compare(
                        manual_data,
                        automated_data,
                        "Gereksinim Metni",  # Bu gerçek metinle değiştirilebilir
                        f"Karşılaştırma_{time.strftime('%Y%m%d_%H%M%S')}"
                    )
                    
                    # Karşılaştırma sonuçlarını göster
                    st.subheader("📊 Karşılaştırma Sonuçları")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("👤 Manuel Test Sayısı", comparison_result['manual']['count'])
                        st.metric("📏 Ortalama Başlık Uzunluğu", f"{comparison_result['manual']['avg_fields_length']['baslik']:.1f}")
                        st.metric("📝 Ortalama Adımlar Uzunluğu", f"{comparison_result['manual']['avg_fields_length']['adimlar']:.1f}")
                    
                    with col2:
                        st.metric("🤖 Otomatik Test Sayısı", comparison_result['automated']['count'])
                        st.metric("📏 Ortalama Başlık Uzunluğu", f"{comparison_result['automated']['avg_fields_length']['baslik']:.1f}")
                        st.metric("📝 Ortalama Adımlar Uzunluğu", f"{comparison_result['automated']['avg_fields_length']['adimlar']:.1f}")
                    
                    st.subheader("📈 Fark Analizi")
                    diff = comparison_result['differences']
                    st.metric("📊 Test Sayısı Farkı", diff['count_difference'], 
                             f"{diff['count_percent_change']:.1f}%")
                    
                    st.metric("⚡ Verimlilik Artışı", 
                             f"{comparison_result['coverage_analysis']['efficiency_gain']:.1f}%")
                    
                    # Karşılaştırmayı kaydet
                    comparator.save_comparison('comparisons.json')
                    st.success("✅ Karşılaştırma sonuçları kaydedildi!")
                    
            else:
                st.warning("⚠️ Önce ana sayfadan otomatik test senaryoları üretin.")
                
        except json.JSONDecodeError:
            st.error("❌ Geçersiz JSON dosyası!")
    else:
        st.info("📁 Manuel test senaryolarını yüklemek için JSON dosyası seçin.")

# Sekme 4: Dokümantasyon
with tab4:
    st.header("📖 Sistem Dokümantasyonu")
    
    st.markdown("""
    ## 🎯 Proje Açıklaması
    
    Bu proje, yazılım gereksinim dokümanlarından otomatik olarak test senaryoları üreten bir NLP tabanlı sistemdir.
    Google Gemini AI modellerini kullanarak, gereksinim metinlerini analiz eder ve kapsamlı test senaryoları oluşturur.
    
    ## 🚀 Kurulum Adımları
    
    ### 1. Gereksinimlerin Yüklenmesi
    ```bash
    pip install -r requirements.txt
    ```
    
    ### 2. API Anahtarı
    - Google AI Studio'dan API anahtarı alın: https://makersuite.google.com/app/apikey
    - Uygulamada API anahtarını girin
    
    ### 3. Uygulama Çalıştırma
    ```bash
    streamlit run test_generate.py
    ```
    
    ## 📋 Sistem Mimarisi
    
    ### Ana Bileşenler:
    
    1. **Parser Modülü** (`parser.py`)
       - PDF, DOCX, DOC ve TXT dosyalarından metin çıkarır
       - Çeşitli formatları destekler
       
    2. **Metrikler Modülü** (`metrics.py`)
       - Performans ölçümleri yapar
       - Test senaryosu kalite değerlendirmesi yapar
       - İstatistiksel analizler sunar
       
    3. **Karşılaştırma Modülü** (`comparison.py`)
       - Manuel vs otomatik test üretimi karşılaştırması
       - Verimlilik analizleri
       
    4. **Ana Uygulama** (`test_generate.py`)
       - Streamlit tabanlı kullanıcı arayüzü
       - AI model entegrasyonu
       - Sonuç görselleştirme
       
    ## 🔄 Çalışma Akışı
    
    1. **Dosya Yükleme**: Kullanıcı gereksinim dokümanını yükler
    2. **Metin Çıkarma**: Parser modülü dosyadan metin çıkarır
    3. **AI Analizi**: Gemini AI gereksinimleri analiz eder
    4. **Test Üretimi**: AI test senaryoları üretir
    5. **Değerlendirme**: Üretilen senaryolar değerlendirilir
    6. **Raporlama**: Sonuçlar ve metrikler sunulur
    """)
    
    st.subheader("📊 Metrikler Açıklaması")
    st.markdown("""
    - **İşlem Süresi**: Toplam işlem süresi (saniye)
    - **Parsing Süresi**: Dosya parsing süresi (saniye)
    - **AI Süresi**: AI model yanıt süresi (saniye)
    - **Kalite Skoru**: Test senaryolarının kalite skoru (%)
    - **Geçerli Yapı**: Standart yapıya uygun test senaryoları yüzdesi
    - **Kapsam**: Gereksinimlerin ne kadarının kapsandığı
    """)
    
    st.subheader("⚖️ Karşılaştırma Metodolojisi")
    st.markdown("""
    Sistem, manuel ve otomatik test üretimi arasında şu kriterlere göre karşılaştırma yapar:
    - Test sayısı karşılaştırması
    - Test senaryosu detay düzeyi
    - Kapsam analizi
    - Verimlilik metrikleri
    """)
