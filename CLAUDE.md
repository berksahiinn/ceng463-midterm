# CLAUDE.md — CENG 463 Take-Home Midterm

Bu dosya, claude.ai'deki önceki konuşmanın özetidir. Claude Code bu projede çalışırken önce bu dosyayı okumalı ve buradaki kurallara uymalıdır.

## Kullanıcı ve iletişim
- Kullanıcı İYTE Bilgisayar Mühendisliği öğrencisi; ders **CENG 463 – Introduction to Machine Learning** (Prof. Dr. Aytuğ Onan, Fall 2026–27).
- Kullanıcıyla **Türkçe** konuş. Kod, yorum satırları, dosya adları ve rapor metni **İngilizce** olabilir.
- Kullanıcı adım adım ilerlemek istiyor: her adımda ne yapıldığını ve neden yapıldığını kısa ve net anlat.
- Kod örnekleri ve konular mümkün olduğunca derste ve lab'larda işlenen yaklaşımlara bağlanmalı (aşağıya bakınız).

## Görev
**Take-Home Midterm** (notun %20'si, bireysel). 5 soru, hepsi zorunlu, her biri 20 puan.
- **Son teslim:** Resmi olarak **1 Aralık 2026, 23:59** (Türkiye saati). Kullanıcının kendi hedefi **30 Kasım**. 1 Aralık yedek gün.
- **Teslim:** Sadece **Microsoft Teams** üzerinden. Tek ZIP dosyası: `CENG463_Midterm_<StudentID>.zip`
- **ZIP içeriği:** LaTeX kaynak + derlenmiş PDF rapor, çalıştırılabilir notebook'lar ya da scriptler, `requirements.txt`, çalıştırma talimatı (README), kaydedilmiş tablo ve figürler, donanım/yazılım özeti, raporda **GitHub ya da Colab linki** (hocanın erişebileceği şekilde).
- **Puanlama (her soru içinde):** metodolojik doğruluk %40, kanıta dayalı analiz derinliği %30, tekrarlanabilirlik ve kod kalitesi %20, raporun açıklığı %10.

## ⚠️ Akademik dürüstlük — Claude için bağlayıcı kurallar
Sınav metnine göre LLM'ler **yalnızca kod yazma, debug ve ortam kurulumu** için kullanılabilir.
- ✅ Yapabilirsin: kod yazmak, hata ayıklamak, ortam kurmak, LaTeX şablonu ve tablo/figür ekleme kodu hazırlamak, metodolojik gereksinimleri hatırlatmak, kullanıcıya **neyi yorumlaması gerektiğini** göstermek.
- ❌ Yapma: raporun **bilimsel yorum ve tartışma metnini** yazmak (sonuçların yorumu, tartışma, sınırlılık analizi, model seçim gerekçesi). Bu kısımları kullanıcı yazar. İstenirse yazdığı metindeki teknik hataları işaret edebilirsin.
- ❌ **Asla** sonuç, metrik ya da gözlem uydurma. Raporlanan her sayı gerçekten çalıştırılmış koddan gelmeli.
- Kullanıcı raporda bir **"LLM Usage Disclosure"** bölümü yazmak zorunda. Hangi araçla, hangi amaçla yardım alındığı ve örnek prompt'lar bu bölüme girer. Her önemli kod yardımını `LLM_USAGE_LOG.md` dosyasına kısa bir maddeyle kaydet: tarih, görev ve ne yapıldığı.

## Genel protokol (her soruda geçerli)
- `SEED = 463`. Bütün rastgelelikler bu seed'e bağlanır: numpy, sklearn `random_state`, bootstrap, bozulmalar.
- **Önce böl, sonra fit et.** Train/validation/test bölümleri herhangi bir dönüşüm fit edilmeden önce yapılır. **Tam bölüm boyutları** raporlanır.
- Sınıflandırma verisi: **%60 / %20 / %20 stratified** bölme. İndeksler `results/splits/clf_split_indices.csv` dosyasına kaydedilir ve **bütün notebook'lar aynı dosyayı okur** (Q1, Q2, Q4, Q5).
- Bütün ön işleme (imputation, scaling, encoding, feature selection, vectorization) bir **`Pipeline` / `ColumnTransformer` içinde** yapılır. CV'de her fold'un sadece training kısmında fit edilir.
- **Hiperparametre tuning:** Train verisinde **5-fold StratifiedKFold** ile `GridSearchCV`. Seçim metriği **Macro-F1**. Bütün modeller **aynı fold'ları** kullanır (`cv` nesnesi `utils.py` içinde tek bir yerde tanımlanır).
- Karşılaştırma ve analizler (Q2c–e, Q4, Q5b–c) **validation** setinde yapılır.
- **TEST SETİ Q5e'ye kadar açılmaz.** Hiçbir tuning ya da seçim kararı test metriğine bakılarak verilmez. Q3'ün kendi regresyon test seti var; o da sadece Q3'ün sonunda bir kez kullanılır.
- Her model için arama uzayı (grid), seçim metriği, pipeline adımları ve süreler kaydedilir. Bütün tablolar `results/tables/*.csv`, bütün figürler `results/figures/*.png` (dpi ≥ 150) olarak kaydedilir.
- Hesaplama ağırsa veri seti **tutarlı ve şeffaf** biçimde küçültülebilir. Ama istenen karşılaştırmaların sayısı azaltılamaz. Yapılan küçültme raporda belirtilir.
- Invalid leakage demosu kodda ve çıktılarda açıkça **`INVALID – demonstration only`** olarak etiketlenir ve başka hiçbir yerde kullanılmaz.

## Veri setleri (önceki konuşmada önerildi; kullanıcı onaylarsa kesinleşir)
- **Sınıflandırma (Q1, Q2, Q4, Q5): IBM Telco Customer Churn** (Kaggle). 7.043 satır, binary hedef `Churn` (yaklaşık %26 Yes), karışık özellik tipleri.
  - `TotalCharges` string geliyor; 11 boş değer var → `pd.to_numeric(errors='coerce')`.
  - `customerID` bir ID sütunu → modelden çıkarılır.
  - `TotalCharges` ≈ `tenure × MonthlyCharges` → yüksek korelasyon.
  - Alternatif: UCI Bank Marketing. Daha büyük, ama `duration` sütunu doğal bir leakage örneği.
- **Regresyon (Q3): California Housing** (`sklearn.datasets.fetch_california_housing`).
  - Eksik değer yok.
  - Hedef 5.0'da kesilmiş (yaklaşık 965 satır).
  - Korelasyonlu çiftler: `AveRooms`–`AveBedrms`, `Latitude`–`Longitude`.
  - `AveOccup` ve `AveRooms` içinde aşırı uç değerler var.
  - Hedef birimi 100.000 $.

## Proje yapısı
```
CENG463_Midterm/
├── CLAUDE.md
├── README.md                 # kurulum + adım adım çalıştırma
├── requirements.txt
├── environment.txt           # python/kütüphane sürümleri, CPU, RAM
├── LLM_USAGE_LOG.md          # disclosure bölümü için kayıt
├── data/                     # ham veri (ya da indirme talimatı)
├── src/utils.py              # SEED, load_data, make_split, load_split, build_preprocessor,
│                             # cv nesnesi, metrik fonksiyonları, save_table, save_fig, timer
├── notebooks/
│   ├── 00_setup_split.ipynb
│   ├── 01_Q1_data_leakage.ipynb
│   ├── 02_Q2_classification.ipynb
│   ├── 03_Q3_regression.ipynb
│   ├── 04_Q4_trees_ensembles.ipynb
│   └── 05_Q5_robustness_selection.ipynb
├── results/
│   ├── splits/  tables/  figures/
│   ├── frozen_configs.json   # Q5e öncesi dondurulan ayarlar + seçim kuralı
│   └── models/               # joblib
└── report/
    ├── main.tex  (9 zorunlu bölüm)
    ├── figures/  (results/figures'a link ya da kopya)
    └── main.pdf
```

## Soru bazında yapılacaklar (checklist)

### Q1 – Veri hazırlama, leakage, deney tasarımı
- [ ] **a)** Domain, hedef, özellik tipleri, örnek sayısı, sınıf dağılımı. Eksik değerler, duplicate'ler (`customerID` dahil ve hariç), anormal değerler, sorunlu predictor'lar (ID, `TotalCharges` korelasyonu, nadir ya da birbirine bağlı kategoriler).
- [ ] **b)** 60/20/20 stratified bölme + boyut tablosu. **Stratified ile random karşılaştırması:** 200 seed üzerinden her bölmede pozitif oranın tüm veriden mutlak sapması (mean, max, std) + boxplot. Hangi yöntem ne zaman başarısız olur: küçük ya da dengesiz veride random; çok nadir sınıf, gruplu veri ya da zaman serisinde stratified.
- [ ] **c)** Sayısal: `SimpleImputer(median)` → `StandardScaler`. Kategorik: `SimpleImputer(most_frequent)` → `OneHotEncoder(handle_unknown='ignore')`. Hangi dönüşüm hangi model ailesine gerekli, tablo (LR ve k-NN scaling ister; ağaçlar istemez ama sklearn'de encoding şart; NB varyanta göre değişir).
- [ ] **d)** Geçerli pipeline ile **INVALID** yöntemi aynı CV fold'larında karşılaştır. Öneriler: (1) 200 gürültü sütunu ekleyip `SelectKBest`'i bütün satırlarda fit etmek, (2) bütün veriden hesaplanan target encoding. Scaling'i bütün veride yapmak da denenir ve fark küçük çıkarsa dürüstçe raporlanır.
- [ ] **e)** Dataset audit tablosu (sütun, tip, eksik sayısı/oranı, benzersiz değer, min/max ya da en sık değer, not). Protokol diyagramı (TikZ ya da draw.io). Kod çalışsa bile sonucu geçersiz kılabilecek en az 3 failure mode.

### Q2 – Sınıflandırma ve hata analizi
- [ ] **a)** `DummyClassifier(most_frequent)`, Logistic Regression, Naive Bayes (varyant seçimi gerekçeli), k-NN.
- [ ] **b)** Her modelde en az 2 hiperparametre, aynı CV ile:
  - LR: `C ∈ {0.01, 0.1, 1, 10, 100}` × `class_weight ∈ {None, 'balanced'}`
  - NB: GaussianNB `var_smoothing ∈ logspace(-12, -3)` + gösterim karşılaştırması (Gaussian+scaled ile `KBinsDiscretizer`+CategoricalNB, `alpha ∈ {0.1, 0.5, 1, 2}`, `n_bins ∈ {5, 10}`)
  - k-NN: `n_neighbors ∈ {1, 3, 5, 11, 21, 41}` × `weights ∈ {uniform, distance}` (opsiyonel `p ∈ {1, 2}`)
- [ ] **c)** Validation'da Accuracy, Macro-F1, sınıf bazında P/R/F1, confusion matrix (sayı + normalize), ROC-AUC, PR-AUC ve eğrileri. Hangi metriğin en uygun olduğu gerekçelendirilir (dengesiz veri → Macro-F1, PR-AUC, churn recall).
- [ ] **d)** Sınıf bazında hatalar. Kontrollü müdahale: `class_weight='balanced'` ile ağırlıksız versiyonun karşılaştırması (ya da sadece training fold'unda oversampling, imblearn Pipeline ile). Opsiyonel: validation üzerinde eşik ayarı.
- [ ] **e)** Final adayın yanlış sınıflandırdığı en az 10 validation örneği: tablo (özellikler, gerçek, tahmin, olasılık), hata kategorileri, girdi özellikleriyle ilişki, somut iyileştirme önerileri. **Test etiketlerine bakılmaz.**

### Q3 – Regresyon, regularization, genelleme (California Housing)
- [ ] **a)** Eksik veri, hedef dağılımı (çarpıklık, 5.0 kesilmesi), korelasyon matrisi, aykırı değerler. 60/20/20 bölme (KFold). Scaling pipeline içinde.
- [ ] **b)** `DummyRegressor`, `LinearRegression`, `Ridge`, `Lasso`, `DecisionTreeRegressor`, `RandomForestRegressor`.
- [ ] **c)** Polinom derecesi 1–4 (+ küçük alpha'lı Ridge) ve ağaç derinliği 1–20 için train ve validation complexity curve'leri. Bias-variance ile yorum. Opsiyonel: `learning_curve`.
- [ ] **d)** Ridge ve Lasso için `alpha ∈ logspace(-4, 2)` CV tuning. Coefficient path grafiği. Lasso'da sıfırlanan katsayı sayısı. Korelasyonlu çiftlerde OLS, Ridge ve Lasso katsayılarının karşılaştırma tablosu.
- [ ] **e)** MAE, RMSE, R² (birim: 100.000 $). Predicted vs actual ve residual vs predicted grafikleri. En büyük en az 5 validation residual'ının tek tek incelenmesi (kesilme noktası mı, uç `AveOccup` mu). Residual örüntüsü (heteroscedasticity). Final Q3 testi bir kez.

### Q4 – Karar ağaçları, bagging, boosting
- [ ] **a)** DT, RF, AdaBoost, GB + Q2'deki en iyi ağaç dışı model (referans). Aynı protokol.
- [ ] **b)** DT: `criterion ∈ {gini, entropy, log_loss}`, `max_depth`, `min_samples_leaf`, `ccp_alpha` (ya da `max_leaf_nodes`). Derinliği ≤ 3 olan bir ağaç için `plot_tree` + `export_text` ve en az 3 karar yolunun yorumu.
- [ ] **c)** RF: `n_estimators ∈ {50, 100, 200, 400}`, `max_depth ∈ {5, 10, None}`, `max_features ∈ {'sqrt', 'log2', 0.5, None}`. Train ve validation skorları, OOB. Kanıt olarak: farklı `max_features` değerlerinde ağaçların validation tahminleri arasındaki ortalama ikili korelasyon. Lab 07 formülü: Var = σ²(ρ + (1−ρ)/B).
- [ ] **d)** AdaBoost ve GB: `n_estimators ∈ {50, 100, 200, 400}` × `learning_rate ∈ {0.05, 0.1, 0.5, 1.0}`. `staged_predict` ile validation Macro-F1'in tahminci sayısına göre grafiği. Sıralı hata düzeltme ile bağımsız bagging karşılaştırması.
- [ ] **e)** Tablo: Macro-F1, Accuracy, train time, inference time (`time.perf_counter`). Built-in importance ile validation verisindeki permutation importance yan yana. Importance'ın yanıltıcı olduğu en az 2 durum (korelasyonlu özellikler, impurity'nin çok değerli/sürekli özellikleri kayırması, one-hot dağılımı, nedensellik değil).

### Q5 – Robustness, istatistiksel karşılaştırma, model seçimi
- [ ] **a)** En az 4 aday (LR, NB, RF, GB; opsiyonel k-NN). Aynı fold'larda CV Macro-F1, ortalama ± standart sapma, fold bazında boxplot.
- [ ] **b)** Validation'da robustness: eksik değer oranı (%0, 10, 30, 50) ya da sayısal gürültü (σ = 0, 0.1, 0.3, 0.5 × özelliğin std'si). Sabit seed ile **bir kez** üretilen aynı bozulmuş set bütün modellerde kullanılır. Macro-F1'in şiddete göre grafiği.
- [ ] **c)** Paired bootstrap: sampling unit = validation örneği, B = 2000 (ya da 5000). Her resample'da iki modelin Macro-F1 farkı, %95 percentile güven aralığı + histogram. Neyi gösterir, neyi göstermez.
- [ ] **d)** Çok kriterli tablo: performans, robustness, yorumlanabilirlik, train/inference maliyeti, implementasyon karmaşıklığı. 0–1 normalize, gerekçeli ağırlıklar (örnek: 0.40 / 0.20 / 0.15 / 0.15 / 0.10). Duyarlılık analizi (±%50 ya da 1000 rastgele ağırlık senaryosu), kazananın değişip değişmediği.
- [ ] **e)** Hiperparametreleri ve seçim kuralını `results/frozen_configs.json` dosyasına + modelleri joblib ile **testten önce** kaydet. Bütün dondurulmuş adayları test setinde **bir kez** değerlendir. Final tablo, seçilen model (kurala göre), sınırlılıklar ve geçerliliği tehdit eden etkenler.

## Rapor (LaTeX, zorunlu bölüm sırası)
1. Introduction, research questions, datasets
2. Data audit, preprocessing, leakage controls
3. Methods and experimental design (Q1–5)
4. Validation scheme, tuning grids, random seeds, computing environment
5. Results (etiketli tablo ve figürler) and interpretation
6. Error analysis, robustness, uncertainty, limitations
7. Final model-selection rationale and test-set evaluation
8. LLM Usage Disclosure
9. References and reproducibility appendix (komutlar, linkler, konfigürasyonlar)

Claude, LaTeX iskeletini, tablo ve figür ekleme kodunu ve reproducibility appendix'ini hazırlayabilir. **Yorum ve tartışma paragraflarını kullanıcı yazar.**

## Zaman planı
| Gün | İş |
|---|---|
| Çar 25 Kas (akşam) | Kurulum: repo, klasörler, `requirements.txt`, Overleaf/LaTeX şablonu, veri indirme, `utils.py`, `00_setup_split`. Q1a'ya başla. |
| Per 26 | Q1'in tamamı + rapor bölüm 2 |
| Cum 27 | Q2'nin tamamı + Q2 rapor kısmı |
| Cmt 28 | Q3'ün tamamı (bağımsız veri seti) + Q3 rapor kısmı |
| Paz 29 | Q4'ün tamamı + akşam Q5a |
| Pzt 30 | Q5b–e (dondur → final test) + raporun kalanı, README, Restart & Run All, ZIP, Teams'e yükleme |
| Sal 1 Ara | Yedek gün (resmi son teslim 23:59) |

## Kod kuralları
- Her notebook en başta `src/utils.py`'den import eder ve seed'i ayarlar. Bütün notebook'lar **Restart & Run All** ile hatasız çalışmalı.
- Paralel işlem için `n_jobs=-1`. Uzun süren hücrelerin süreleri ölçülüp kaydedilir.
- Her tablo CSV olarak ve LaTeX'e eklenebilir biçimde (`df.to_latex`) kaydedilir.
- Sürümler `pip freeze > requirements.txt` ile sabitlenir. `environment.txt` dosyasına Python sürümü, işletim sistemi, CPU ve RAM yazılır.

## Ders bağlantıları (kodda ve açıklamalarda referans için)
- **L2 (Data & Learning):** train/test, 10-fold CV, overfitting, ZeroR baseline, accuracy/TP/FP/FN, ROC/AUC, F = 2TP/(2TP+FP+FN), confusion matrix. Dengesiz veride CV'de bir sınıfın eksik kalması (L5 s.32–33'teki R uyarısı).
- **L3 (Text Classification):** Naive Bayes, Laplace smoothing, Multinomial/Bernoulli/Gaussian varyantları.
- **L4 (Regression):** k-NN regresyon, inverse/Gaussian ağırlıklandırma, normalizasyon gerekliliği.
- **L5 (Decision Support):** entropy, information gain, overfitting ve pruning, J48/CART.
- **L6 (Kernel & SVM):** RBF, C, γ.
- **L7 (Ensemble):** bias/variance, bagging variance'ı azaltır, boosting bias'ı azaltır, RF, AdaBoost, GB, XGBoost, stacking.
- **L8 (ANN):** softmax, cross-entropy, L2 regularization, gradient descent, ReLU gizli katman.
- **Lab'lar (kodları uyarlanabilir):** Lab02-03 (Dummy, NB varyantları, eşik ve abstention, imbalance), Lab04 (ColumnTransformer + Pipeline, scaler karşılaştırması, MAE/RMSE/R², residual grafikleri, leakage örneği), Lab05 (ID3, Gini/entropy, ccp_alpha, RF/ET/AdaBoost/GB/HGB, permutation importance, calibration), Lab06 (SVM, GridSearch), Lab07 (voting, bagging, OOB, korelasyon formülü, staged boosting, aynı fold'larla karşılaştırma), Lab08 (NumPy MLP).
- Kullanıcının kendi ders materyalleri (slayt PDF'leri, lab notebook'ları) bu repoda yoksa ve gerekirse kullanıcıdan `course_materials/` klasörüne koyması istenebilir.
