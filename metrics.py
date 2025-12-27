"""
Performans ölçümü ve değerlendirme modülü
Test senaryosu üretim sürecinin metriklerini toplar ve değerlendirir.
"""
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd


class PerformanceMetrics:
    """Test senaryosu üretim performansını ölçer ve kaydeder"""
    
    def __init__(self):
        self.metrics = {
            'timestamp': None,
            'file_name': None,
            'file_type': None,
            'file_size_bytes': None,
            'file_content_length': None,
            'processing_time': None,
            'parsing_time': None,
            'ai_generation_time': None,
            'total_test_cases': None,
            'model_name': None,
            'success': None,
            'error_message': None
        }
        self.start_time = None
        self.parsing_start = None
        self.ai_start = None
    
    def start_processing(self, file_name: str, file_type: str, file_size: int, content_length: int):
        """İşlem başlangıcını kaydet"""
        self.start_time = time.time()
        self.metrics['timestamp'] = datetime.now().isoformat()
        self.metrics['file_name'] = file_name
        self.metrics['file_type'] = file_type
        self.metrics['file_size_bytes'] = file_size
        self.metrics['file_content_length'] = content_length
    
    def start_parsing(self):
        """Dosya parsing başlangıcını kaydet"""
        self.parsing_start = time.time()
    
    def end_parsing(self):
        """Dosya parsing bitişini kaydet"""
        if self.parsing_start:
            self.metrics['parsing_time'] = time.time() - self.parsing_start
    
    def start_ai_generation(self, model_name: str):
        """AI üretim başlangıcını kaydet"""
        self.ai_start = time.time()
        self.metrics['model_name'] = model_name
    
    def end_ai_generation(self):
        """AI üretim bitişini kaydet"""
        if self.ai_start:
            self.metrics['ai_generation_time'] = time.time() - self.ai_start
    
    def end_processing(self, test_cases: List, success: bool = True, error_message: Optional[str] = None):
        """İşlem bitişini kaydet"""
        if self.start_time:
            self.metrics['processing_time'] = time.time() - self.start_time
        self.metrics['total_test_cases'] = len(test_cases) if test_cases else 0
        self.metrics['success'] = success
        self.metrics['error_message'] = error_message
        return self.metrics
    
    def get_metrics(self) -> Dict:
        """Mevcut metrikleri döndür"""
        return self.metrics.copy()
    
    def save_to_file(self, filepath: str = 'metrics.json'):
        """Metrikleri JSON dosyasına kaydet"""
        # Eğer dosya varsa, mevcut verileri oku
        all_metrics = []
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    all_metrics = json.load(f)
            except:
                all_metrics = []
        
        # Yeni metrikleri ekle
        all_metrics.append(self.metrics)
        
        # Dosyaya yaz
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(all_metrics, f, indent=2, ensure_ascii=False)
        
        return filepath


class TestCaseEvaluator:
    """Üretilen test senaryolarını değerlendirir"""
    
    @staticmethod
    def evaluate_test_cases(test_cases: List[Dict]) -> Dict:
        """
        Test senaryolarını değerlendir ve istatistikler döndür
        
        Args:
            test_cases: Test senaryoları listesi
            
        Returns:
            Değerlendirme metrikleri
        """
        if not test_cases:
            return {
                'total_count': 0,
                'valid_structure': 0,
                'has_prerequisites': 0,
                'has_steps': 0,
                'has_expected_result': 0,
                'avg_steps_length': 0,
                'coverage_score': 0
            }
        
        total = len(test_cases)
        valid_structure = 0
        has_prerequisites = 0
        has_steps = 0
        has_expected_result = 0
        total_steps_length = 0
        
        required_fields = ['id', 'baslik', 'on_kosul', 'adimlar', 'beklenen_sonuc']
        
        for tc in test_cases:
            # Yapı kontrolü
            if all(field in tc for field in required_fields):
                valid_structure += 1
            
            # İçerik kontrolü
            if tc.get('on_kosul', '').strip():
                has_prerequisites += 1
            if tc.get('adimlar', '').strip():
                has_steps += 1
                total_steps_length += len(tc.get('adimlar', ''))
            if tc.get('beklenen_sonuc', '').strip():
                has_expected_result += 1
        
        avg_steps_length = total_steps_length / total if total > 0 else 0
        
        # Kapsam skoru (tüm kriterlerin ortalaması)
        coverage_score = (
            (valid_structure / total * 100) +
            (has_prerequisites / total * 100) +
            (has_steps / total * 100) +
            (has_expected_result / total * 100)
        ) / 4 if total > 0 else 0
        
        return {
            'total_count': total,
            'valid_structure': valid_structure,
            'has_prerequisites': has_prerequisites,
            'has_steps': has_steps,
            'has_expected_result': has_expected_result,
            'avg_steps_length': round(avg_steps_length, 2),
            'coverage_score': round(coverage_score, 2),
            'valid_structure_percent': round(valid_structure / total * 100, 2) if total > 0 else 0,
            'has_prerequisites_percent': round(has_prerequisites / total * 100, 2) if total > 0 else 0,
            'has_steps_percent': round(has_steps / total * 100, 2) if total > 0 else 0,
            'has_expected_result_percent': round(has_expected_result / total * 100, 2) if total > 0 else 0
        }


def load_metrics_history(filepath: str = 'metrics.json') -> List[Dict]:
    """Kaydedilmiş metrik geçmişini yükle"""
    if not os.path.exists(filepath):
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []


def get_aggregate_statistics(metrics_history: List[Dict]) -> Dict:
    """Toplu istatistikler hesapla"""
    if not metrics_history:
        return {}
    
    df = pd.DataFrame(metrics_history)
    
    successful_runs = df[df['success'] == True] if 'success' in df.columns else df
    
    stats = {
        'total_runs': len(df),
        'successful_runs': len(successful_runs) if 'success' in df.columns else len(df),
        'avg_processing_time': successful_runs['processing_time'].mean() if 'processing_time' in successful_runs.columns else 0,
        'avg_test_cases': successful_runs['total_test_cases'].mean() if 'total_test_cases' in successful_runs.columns else 0,
        'total_test_cases_generated': successful_runs['total_test_cases'].sum() if 'total_test_cases' in successful_runs.columns else 0
    }
    
    if 'parsing_time' in successful_runs.columns:
        stats['avg_parsing_time'] = successful_runs['parsing_time'].mean()
    
    if 'ai_generation_time' in successful_runs.columns:
        stats['avg_ai_generation_time'] = successful_runs['ai_generation_time'].mean()
    
    return stats

