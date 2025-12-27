"""
Manuel vs Otomatik test senaryosu üretimi karşılaştırma modülü
"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class ManualVsAutomatedComparison:
    """Manuel ve otomatik test üretimi karşılaştırması"""
    
    def __init__(self):
        self.comparison_data = []
    
    def compare(self, 
                manual_test_cases: List[Dict], 
                automated_test_cases: List[Dict],
                requirement_text: str,
                comparison_name: str = "Karşılaştırma") -> Dict:
        """
        Manuel ve otomatik test senaryolarını karşılaştır
        
        Args:
            manual_test_cases: Manuel olarak hazırlanan test senaryoları
            automated_test_cases: Otomatik üretilen test senaryoları
            requirement_text: Gereksinim metni
            comparison_name: Karşılaştırma adı
            
        Returns:
            Karşılaştırma sonuçları
        """
        comparison = {
            'comparison_name': comparison_name,
            'timestamp': datetime.now().isoformat(),
            'requirement_length': len(requirement_text),
            'manual': {
                'count': len(manual_test_cases),
                'avg_fields_length': self._calculate_avg_field_length(manual_test_cases)
            },
            'automated': {
                'count': len(automated_test_cases),
                'avg_fields_length': self._calculate_avg_field_length(automated_test_cases)
            },
            'differences': self._calculate_differences(manual_test_cases, automated_test_cases),
            'coverage_analysis': self._analyze_coverage(manual_test_cases, automated_test_cases)
        }
        
        self.comparison_data.append(comparison)
        return comparison
    
    def _calculate_avg_field_length(self, test_cases: List[Dict]) -> Dict:
        """Ortalama alan uzunluklarını hesapla"""
        if not test_cases:
            return {'baslik': 0, 'on_kosul': 0, 'adimlar': 0, 'beklenen_sonuc': 0}
        
        totals = {'baslik': 0, 'on_kosul': 0, 'adimlar': 0, 'beklenen_sonuc': 0}
        
        for tc in test_cases:
            totals['baslik'] += len(str(tc.get('baslik', '')))
            totals['on_kosul'] += len(str(tc.get('on_kosul', '')))
            totals['adimlar'] += len(str(tc.get('adimlar', '')))
            totals['beklenen_sonuc'] += len(str(tc.get('beklenen_sonuc', '')))
        
        count = len(test_cases)
        return {k: round(v / count, 2) for k, v in totals.items()}
    
    def _calculate_differences(self, manual: List[Dict], automated: List[Dict]) -> Dict:
        """Farkları hesapla"""
        return {
            'count_difference': len(automated) - len(manual),
            'count_ratio': round(len(automated) / len(manual), 2) if len(manual) > 0 else 0,
            'count_percent_change': round((len(automated) - len(manual)) / len(manual) * 100, 2) if len(manual) > 0 else 0
        }
    
    def _analyze_coverage(self, manual: List[Dict], automated: List[Dict]) -> Dict:
        """Kapsam analizi yap"""
        # Basit bir kapsam analizi - test case sayılarına göre
        manual_coverage_score = len(manual) * 10  # Her test case 10 puan (örnek)
        automated_coverage_score = len(automated) * 10
        
        return {
            'manual_coverage_estimate': manual_coverage_score,
            'automated_coverage_estimate': automated_coverage_score,
            'coverage_ratio': round(automated_coverage_score / manual_coverage_score, 2) if manual_coverage_score > 0 else 0,
            'efficiency_gain': round((len(automated) / len(manual) - 1) * 100, 2) if len(manual) > 0 else 0
        }
    
    def save_comparison(self, filepath: str = 'comparisons.json'):
        """Karşılaştırma sonuçlarını kaydet"""
        # Mevcut karşılaştırmaları yükle
        all_comparisons = []
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    all_comparisons = json.load(f)
            except:
                all_comparisons = []
        
        # Yeni karşılaştırmaları ekle
        all_comparisons.extend(self.comparison_data)
        
        # Dosyaya yaz
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(all_comparisons, f, indent=2, ensure_ascii=False)
        
        return filepath


def load_comparisons(filepath: str = 'comparisons.json') -> List[Dict]:
    """Kaydedilmiş karşılaştırmaları yükle"""
    if not os.path.exists(filepath):
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

