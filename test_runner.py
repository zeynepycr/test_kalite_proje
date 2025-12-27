"""
Test runner script - Örnek test senaryolarını çalıştırmak için
"""
import json
import os
from metrics import TestCaseEvaluator

def evaluate_test_file(test_file_path):
    """
    Test senaryosu dosyasını değerlendir
    
    Args:
        test_file_path: Test senaryosu JSON dosyası yolu
    """
    if not os.path.exists(test_file_path):
        print(f"❌ Dosya bulunamadı: {test_file_path}")
        return None
    
    with open(test_file_path, 'r', encoding='utf-8') as f:
        test_cases = json.load(f)
    
    evaluator = TestCaseEvaluator()
    evaluation = evaluator.evaluate_test_cases(test_cases)
    
    print(f"\n📊 Test Senaryosu Değerlendirmesi: {test_file_path}")
    print("=" * 60)
    print(f"Toplam Test Sayısı: {evaluation['total_count']}")
    print(f"Geçerli Yapı: {evaluation['valid_structure']} ({evaluation['valid_structure_percent']}%)")
    print(f"Ön Koşul Var: {evaluation['has_prerequisites']} ({evaluation['has_prerequisites_percent']}%)")
    print(f"Adımlar Var: {evaluation['has_steps']} ({evaluation['has_steps_percent']}%)")
    print(f"Beklenen Sonuç: {evaluation['has_expected_result']} ({evaluation['has_expected_result_percent']}%)")
    print(f"Ortalama Adım Uzunluğu: {evaluation['avg_steps_length']}")
    print(f"Kalite Skoru: {evaluation['coverage_score']}%")
    print("=" * 60)
    
    return evaluation

if __name__ == "__main__":
    # Örnek test dosyasını değerlendir
    example_file = "examples/example_manual_tests.json"
    if os.path.exists(example_file):
        evaluate_test_file(example_file)
    else:
        print(f"⚠️ Örnek dosya bulunamadı: {example_file}")

