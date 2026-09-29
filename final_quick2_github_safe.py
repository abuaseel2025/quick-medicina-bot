import os
import re
import io
import time
import telebot
from google import genai
from google.genai import types
from PIL import Image

# ============================================================
# 1) مفاتيح التشغيل
# ============================================================
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
if not TELEGRAM_TOKEN or not GEMINI_API_KEY or TELEGRAM_TOKEN.startswith("ضع_") or GEMINI_API_KEY.startswith("ضع_"):
    raise RuntimeError("من فضلك ضع TELEGRAM_TOKEN و GEMINI_API_KEY في أول الكود.")

client = genai.Client(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ============================================================
# 2) قوائم الأسعار (القائمة الأساسية لوراثة العينة والمدة)
# ============================================================
PRICE_LIST_TEXTS = {
    '💰 برايس كويك القديم': r"""
- 1-25 OH-Vitamin D: السعر 140، العينة Serum (500 μL)، المدة 1 Day
- 17 Ketosteroids in Urine (24 hrs): السعر 480، العينة 24h Urine in acidified container، المدة 5 Days
- 17 OH progesterone: السعر 200، العينة Serum، المدة 4 Days
- A/G Ratio: السعر 30، العينة Serum، المدة 2 Days
- AB- Thrombo Type Plus: السعر 2000، العينة Frozen Serum، المدة 2 Days
- ABO Group: السعر 10، العينة Edita whole blood، المدة 2 Hours
- Absolute CD 4 + Cells Count: السعر 750، العينة EDTA Blood، المدة 5 Days
- Acetone in Urine: السعر 10، العينة Urine، المدة 6 Hours
- Acid Phosphatase (Prostatic): السعر 180، العينة Serum، المدة 2 Days
- Acid Phosphatase (Total): السعر 80، العينة Serum، المدة 2 Days
- ACTH (AM): السعر 85، العينة Frozen EDTA plasma in plastic tube، المدة 1 Days
- ACTH (PM): السعر 85، العينة Frozen EDTA plasma in plastic tube، المدة 1 Days
- ACTH Random: السعر 105، العينة Frozen EDTA plasma in plastic tube، المدة 1 Days
- Acti Fibro test: السعر 1700، العينة Serum (Required: Fasting)، المدة 6 Days
- ADA: السعر 160، العينة Pericardial Fluid، المدة 1 Day
- ADA(Adenosine Deaminase in Ascitic Fluid): السعر 160، العينة Fluid، المدة 2 Days
- ADA(Adenosine Deaminase in serum): السعر 160، العينة Serum، المدة 2 Days
- Adenovirus (ADV) DNA: السعر 200، العينة Serum، المدة 2 Days
- ADH (Anti-diuretic hormone): السعر 840، العينة Frozen EDTA plasma، المدة 10 Days
- Adrenalin: السعر 2000، العينة EDTA plasma، المدة 8 Days
- Albumin / Creatinine ratio (A/C %): السعر 35، العينة Urine، المدة 6 Hours
- Albumin in Urine (Random): السعر 30، العينة Urine، المدة 6 Hours
- Aldolase: السعر 310، العينة Serum، المدة 2 Days
- Aldosterone / Renin ratio: السعر 1200، العينة Frozen morning EDTA plasma + Serum، المدة 6 Days
- Alk Phosphatase: السعر 12، العينة Serum، المدة 6 Hours
- Alpha - 1 Anti trypsin: السعر 170، العينة Serum، المدة 2 Days
- Alpha 1 globulin: السعر Contact Lab، العينة Serum، المدة 2 Days
- Alpha Feto Protein in serum: السعر 50، العينة Serum، المدة 6 Hours
- Alpha-glucosidase in semen: السعر 580، العينة Seminal Fluid في انبوبة وزرمان، المدة 3 Days
- AMA: السعر 150، العينة Serum، المدة 4 Days
- AMH (Anti Mullerian Hormone): السعر 165، العينة Serum، المدة 6 Hours
- Ammonia: السعر 50، العينة EDTA frozen plasma، المدة 6 Hours
- Amylase in Urine: السعر 18، العينة Urine، المدة 6 Hours
- Amyloid A: السعر 220، العينة Serum، المدة 3 Days
- ANA: السعر 75، العينة Serum، المدة 1 Days
- ANA by Immunofluorescence: السعر 100، العينة Serum، المدة 3 Days
- Anal Swab for oxyruis ova: السعر Contact Lab، العينة Swab، المدة 1 Day
- ANCA C (Cytoplasmic): السعر 125، العينة Serum، المدة 1 Day
- ANCA P (Perinuclear): السعر 125، العينة Serum، المدة 1 Day
- Androstenedione: السعر 350، العينة Serum، المدة 4 Days
- Angiotensin converting Enzyme: السعر 480، العينة Serum، المدة 2 Days
- AnSCL 70 Antibody: السعر 360، العينة Serum، المدة 4 Days
- Anti - (d.s) DNA: السعر 75، العينة Serum، المدة 1 Days
- Anti - CCP Antibody (Ab): السعر 120، العينة Serum، المدة 1 Days
- Anti - Gliadin Antibody (IgG): السعر 320، العينة Serum، المدة 4 Days
- Anti - Histones Antibody: السعر 750، العينة Serum، المدة 4 Days
- Anti - Parietal Antibody: السعر 400، العينة Serum، المدة 4 Days
- Anti - Phospholipid Antibody (IgG): السعر 180، العينة Serum، المدة 1 Days
- Anti - Phospholipid Antibody (IgM): السعر 180، العينة Serum، المدة 1 Days
- Anti - Platelet Antibody (Direct): السعر 600، العينة 4 (EDTA tube - 2mL)، المدة 5 Days
- Anti - Platelet Antibody (Indirect): السعر 600، العينة Serum، المدة 4 Days
- Anti - RNP Antibody: السعر 350، العينة Serum، المدة 4 Days
- Anti - ss - A/Ro Antibody: السعر 330، العينة Serum، المدة 3 Days
- Anti-ss-B/La Antibody: السعر 330، العينة Serum، المدة 3 Days
- Anti GAD (Anti-glutamic acid decarboxylase): السعر 700، العينة Serum، المدة 4 Days
- Anti ICA (Anti-Islet cell Ab): السعر 320، العينة Serum، المدة 4 Days
- Anti Intrinsic factor Ab: السعر 430، العينة Serum، المدة 4 Days
- ASOT LATEX: السعر 20، العينة Serum، المدة 1 Days
- Anti MOG (IFA) (anti-Myelin oligodendrocyte Glycoprotein): السعر 1500، العينة Serum، المدة 5 Days
- Anti MuSK (muscle specific tyrosine kinase): السعر 5000، العينة Serum، المدة 5 Days
- Anti Smooth muscle Antibodies (ASMA): السعر 230، العينة Serum، المدة 1 Days
- Anti Streptolysin (ASOT): السعر 40، العينة Serum، المدة 6 Hours
- Anti thyroid Antibody: السعر 180، العينة Serum، المدة 1 Days
- Anti Tissue transglutaminase Ab IgA: السعر 280، العينة Serum، المدة 4 Days
- Anti-B2 Glycoprotein(IgG): السعر 320، العينة Serum، المدة 4 Days
- Anti-B2 Glycoprotein (IgM): السعر 320، العينة Serum، المدة 4 Days
- Anticardiolipin IgG: السعر 100، العينة Serum، المدة 1 Days
- Anticardiolipin IgM: السعر 100، العينة Serum، المدة 1 Days
- Antidiuretic Hormone (ADH): السعر 850، العينة frozen EDTA plasma، المدة 10 Days
- Anti-Smith Antibody: السعر 300، العينة Serum، المدة 4 Days
- Antisperm Antibody (IgG): السعر Contact Lab، العينة Serum، المدة 2 Days
- Antisperm Antibody (IgM): السعر Contact Lab، العينة Serum، المدة 2 Days
- Anti-Sperm Antibody in Semen: السعر Contact Lab، العينة Seminal fluid، المدة 2 Days
- AntiSperm Antibody: السعر 450، العينة Serum، المدة 4 Days
- Antithrombin III: السعر 160، العينة Citrated plasma، المدة 2 Days
- Anti-thyroglobulin Antibody (ATG): السعر 80، العينة Serum، المدة 8 Hours
- Anti-TSH receptor antibody: السعر 550، العينة Serum، المدة 2 Days
- ASCA Antibody (IgA): السعر 570، العينة Serum، المدة 4 Days
- ASCA Antibody (IgG): السعر 570، العينة Serum، المدة 4 Days
- Ascitic fluid C/S: السعر 50، العينة Fluid، المدة 4 Days
- Ascitic Fluid Examination: السعر 75، العينة Fluid، المدة 6 Hours
- B2 Microglobuilin: السعر 110، العينة Serum، المدة 2 Days
- B2 Microglobulin in urine: السعر 140، العينة Urine، المدة 2 Days
- BCR-ABL Minor (p190) gene by Real Time PCR: السعر 3000، العينة EDTA Blood، المدة 6 Days
- Bence Jones protein in urine: السعر 20، العينة Urine، المدة 6 Hours
- BHCG: السعر 35، العينة Serum، المدة 6 Hours
- Bleeding Time: السعر 10، العينة Edita whole blood، المدة 6 Hours
- Blood C/S: السعر 70، العينة blood media، المدة 10 Days
- Blood film: السعر 30، العينة Edita whole blood، المدة 8 Hours
- Blood Gas Profile (ABG): السعر 100، العينة Heparinized Whole blood، المدة 1 Hours
- Blood Urea: السعر 10، العينة Serum، المدة 6 Hours
- Body Fluid Culture: السعر 50، العينة Fluid، المدة 5 Days
- BONE MARROW EX.: السعر 7500، العينة BONE MARROW، المدة 7 Days
- Breast Discharge Culture: السعر 40، العينة Sterile Swab، المدة 3 Days
- Brucella IgG: السعر 340، العينة Serum، المدة 1 Days
- Brucella IgM: السعر 340، العينة Serum، المدة 1 Days
- Brucella Test: السعر 20، العينة Serum، المدة 6 Hours
- BUN: السعر 10، العينة Serum، المدة 6 Hours
- C- Peptide (Fasting): السعر 75، العينة Serum، المدة 6 Hours
- C - Peptide (Postprandial): السعر 75، العينة Serum، المدة 6 Hours
- C. Reactive Protein (CRP): السعر 40، العينة Serum، المدة 6 Hours
- C1 esterase inhibitor: السعر 520، العينة Edita plasma، المدة 3 Days
- C3: السعر 45، العينة Serum، المدة 1 Days
- C4: السعر 45، العينة Serum، المدة 1 Days
- CA 125: السعر 75، العينة Serum، المدة 6 Hours
- CA 15.3: السعر 75، العينة Serum، المدة 6 Hours
- CA 19.9: السعر 75، العينة Serum، المدة 6 Hours
- Calcitonin: السعر 680، العينة Frozen Serum (500 µl)، المدة 5 Days
- Calcium / Phosphorus Ratio: السعر 45، العينة Urine، المدة 6 Hours
- Calcium in Urine (24hrs): السعر 12، العينة Urine، المدة 6 Hours
- Calcium/Creatinine ratio: السعر 30، العينة Urine، المدة 6 Hours
- Calcium/Phosphorus (Ca - Ph): السعر 25، العينة Urine، المدة 6 Hours
- Calprotectin Stool Quantitative: السعر 220، العينة Stool، المدة 1 Days
- Carbamazepin (Tegretol): السعر 120، العينة Serum، المدة 1 Days
- Catecholamine (Adrenalin Serum): السعر Contact Lab، العينة Edita plasma، المدة 8 Days
- Catecholamine (Noradrenalin Serum): السعر Contact Lab، العينة Edita plasma، المدة 8 Days
- Catecholamines in Urine (24 hrs): السعر 900، العينة Urine، المدة 7 Days
- CD 10: السعر 700، العينة Paraffin blocks، المدة 10 Days
- CD 19: السعر 850، العينة Paraffin blocks، المدة 10 Days
- CD 1a: السعر 700، العينة Paraffin blocks، المدة 10 Days
- CD4/CD 8: السعر 1050، العينة Paraffin blocks، المدة 5 Days
- CD 5: السعر 700، العينة Paraffin blocks، المدة 10 Days
- CD 7: السعر 700، العينة Paraffin blocks، المدة 10 Days
- CEA: السعر 50، العينة Serum، المدة 6 Hours
- Ceruloplasmin: السعر 120، العينة Serum، المدة 2 Days
- Cervical Swab C/S: السعر 50، العينة Strile swab، المدة 3 Days
- Chlamydia Antibody: السعر 480، العينة Serum، المدة 3 Days
- Chlamydia Antibody (IgG): السعر 480، العينة Serum، المدة 3 Days
- Chloride (Serum): السعر 20، العينة Serum، المدة 6 Hours
- Chloride Urine (24 hrs): السعر 20، العينة Serum، المدة 6 Hours
- Chol/HDL: السعر 28، العينة Serum، المدة 4 Hours
- Cholinestrase: السعر Contact Lab، العينة Serum، المدة 5 Days
- Chromogranin A in serum: السعر 800، العينة Serum، المدة 6 Days
- Clotting Time: السعر 10، العينة Edita whole blood، المدة 6 Hours
- CMV Antibody (IgG): السعر 40، العينة Serum، المدة 1 Days
- CMV Antibody (IgM): السعر 40، العينة Serum، المدة 1 Days
- Complete Blood Count: السعر 19، العينة EDTA Blood، المدة 4 Hours
- Complete Blood Count (CBC): السعر 19، العينة Edita whole blood، المدة 2 Hours
- Comprehensive Metabolic Panel: السعر 300، العينة Serum، المدة 1 Day
- Coombs' Test (Direct): السعر 25، العينة EDTA blood (1mL)، المدة 1 Hours
- Coombs' Test (Indirect): السعر 30، العينة Serum (500 μL)، المدة 1 Days
- Copper: السعر 60، العينة Serum، المدة 1 Days
- Copper in Urine (24 hrs): السعر 60، العينة Urine 24 hrs، المدة 6 Hours
- Cortisol 9 am: السعر 75، العينة Serum، المدة 6 Hours
- Cortisol (Random): السعر 75، العينة Serum، المدة 6 Hours
- Cortisol 9 pm: السعر 75، العينة Serum، المدة 6 Hours
- Cortisol In Urine (24 hrs): السعر 75، العينة Urine 24 hrs، المدة 6 Hours
- Covid 19 Antigen: السعر Contact Lab، العينة Serum، المدة 1 Day
- COVID IgG Ab: السعر 250، العينة Serum، المدة 6 Hours
- COVID IgM Ab: السعر 250، العينة Serum، المدة 6 Hours
- COVID-19 test by RT-PCR: السعر 700، العينة Nasal swab، المدة 1 Days
- COVID-19 test by RT-PCR (Qualitative detection of SARS-COV-2): السعر Contact Lab، العينة Swab in special media، المدة 1 Day
- CPK: السعر 15، العينة Serum، المدة 6 Hours
- CPK (MB): السعر 30، العينة Serum، المدة 6 Hours
- Creatinine Clearance: السعر 15، العينة Serum and 24 hrs Urine، المدة 6 Hours
- Creatinine in urine: السعر 10، العينة 24 hrs. Urine، المدة 6 Hours
- Cryoglobulin: السعر 60، العينة Serum، المدة 6 Days
- CSF C/S: السعر 50، العينة CSF Fluid، المدة 3 Days
- CSF examination: السعر 75، العينة CSF Fluid، المدة 8 Hours
- CRP LATEX: السعر 20، العينة Serum، المدة 1 Days
- Culture Report: السعر 50، العينة Sample، المدة 3 Days
- Cyclosporine (Sandimmune): السعر 450، العينة Edita blood، المدة 3 Days
- Cystatin C: السعر 150، العينة Serum، المدة 1 Days
- CYTOLOGICAL ASSESSMENTS: السعر 500، العينة Fluid، المدة 10 Days
- CYTOLOGY: السعر 480، العينة Sample، المدة 10 Days
- D-Dimer: السعر 60، العينة Citrated plasma، المدة 6 Hours
- Depakine (Valproic Acid): السعر 140، العينة Serum، المدة 1 Days
- DHEA: السعر 120، العينة Serum، المدة 1 Days
- DHEA-S: السعر 90، العينة Serum، المدة 1 Days
- Differential Leucocytic Count (WBCs): السعر 15، العينة Edita whole blood، المدة 2 Hours
- Digoxin (Lanoxin) therapeutic level: السعر 125، العينة Serum، المدة 1 Days
- dihydrotestosterone (DHT): السعر 380، العينة Serum، المدة 4 Days
- Direct Bilirubin: السعر 10، العينة Serum، المدة 4 Hours
- DNA Fragmentation from sperm: السعر 1300، العينة Semen، المدة 2 Days
- Double Marker (1st trimester) (11-13 w): السعر 500، العينة Serum، المدة 4 Days
- Drugs Screening: السعر 150، العينة Urine، المدة 6 Hours
- Dysmorphic RBCs in urine: السعر 70، العينة Urine، المدة 1 Day
- E.S.R: السعر 15، العينة Edita whole blood، المدة 6 Hours
- EBV Antibody (IgG): السعر 110، العينة Serum، المدة 4 Days
- EBV Antibody (IgM): السعر 110، العينة Serum، المدة 3 Days
- EBV By PCR Quantitative: السعر 850، العينة EDTA plasma، المدة 4 Days
- eGFR: السعر 30، العينة Serum، المدة 6 Hours
- Endomysial IgA (IFA): السعر 380، العينة Serum، المدة 4 Days
- Endomysial IgG (IFA): السعر 285، العينة Serum، المدة 4 Days
- Entamoeba histolytica Ab: السعر 210، العينة Serum، المدة 2 Days
- Epanutin (Phenytoin, dilantin): السعر 120، العينة Serum، المدة 1 Days
- Estradiol (E2): السعر 45، العينة Serum، المدة 6 Hours
- Estriol (E3): السعر 320، العينة Serum، المدة 4 Days
- Estrogen Receptors (ER+): السعر 750، العينة Serum، المدة 6 Days
- Ethanol (Alcohol) level: السعر 80، العينة Urine، المدة 1 Days
- Extractable Nuclear Antigens (ENA) Panel: السعر 900، العينة Serum، المدة 5 Days
- F.D.P: السعر 150، العينة Citrated plasma، المدة 2 Days
- Factor - IX: السعر 240، العينة Citrated plasma، المدة 3 Days
- Factor - VIII: السعر 1000، العينة Citrated plasma، المدة 4 Days
- Factor II: السعر 1200، العينة Citrated plasma، المدة 4 Days
- Factor V: السعر 1000، العينة Citrated plasma، المدة 4 Days
- Factor V Leiden Mutation By PCR: السعر 750، العينة Edita whole blood، المدة 7 Days
- Factor VII (F. 7): السعر 1200، العينة Citrated plasma، المدة 4 Days
- Factor X (F. 10): السعر 1200، العينة Citrated plasma، المدة 4 Days
- Factor XI (F. 11): السعر 1200، العينة Citrated plasma، المدة 4 Days
- Factor XII (F. 12): السعر 1200، العينة Citrated plasma، المدة 4 Days
- Fasciola Ab Titre: السعر 180، العينة Serum، المدة 2 Days
- Fasciola Ab: السعر 240، العينة Serum، المدة 1 Day
- Fasting Blood Glucose: السعر 10، العينة Fasting Serum on floride tube، المدة 6 Hours
- Ferritin: السعر 45، العينة Serum، المدة 6 Hours
- Fibrin/ Fibrinogen Degradation Products (FDP): السعر 100، العينة Citrated plasma، المدة 2 Days
- Fibrinogen: السعر 70، العينة Citrated plasma، المدة 2 Days
- Fibrosis-4 (FIB-4): السعر 180، العينة EDTA blood + Serum، المدة 2 Days
- Filaria Ag: السعر 450، العينة Serum، المدة 1 Day
- Filaria antibodies: السعر 210، العينة Serum، المدة 2 Days
- Filaria Film: السعر 50، العينة EDTA Blood، المدة 1 Days
- Fluid Amylase: السعر 22، العينة Fluid، المدة 6 Hours
- Fluid C/S: السعر 50، العينة Fluid، المدة 3 Days
- Fluid Lipase: السعر 35، العينة Fluid، المدة 6 Hours
- Folic Acid: السعر 280، العينة Frozen Serum (500 μL)، المدة 2 Days
- Food Allergy Panel: السعر 950، العينة Serum، المدة 15 Days
- Free Metanephrine: السعر 1300، العينة Edita plasma، المدة 8 Days
- Free Prostatic Specific Ag (PSA): السعر 45، العينة Serum، المدة 6 Hours
- Free PSA/Total PSA ratio: السعر 85، العينة Serum، المدة 4 Hours
- Fructosamine: السعر 65، العينة Serum، المدة 1 Days
- Fructose in semen: السعر 65، العينة Seminal Fluid (Fresh or Frozen sample)، المدة 2 Days
- FSH: السعر 30، العينة Serum، المدة 6 Hours
- FSH/LH ratio: السعر 60، العينة Serum، المدة 4 Hours
- FTI: السعر 90، العينة Serum، المدة 1 Days
- Fungal stain: السعر 130، العينة Any body Fluid، المدة 2 Days
- G6PD (Quantitative): السعر 70، العينة Edita whole blood، المدة 2 Hours
- Gastrin: السعر 450، العينة Fasting, frozen Serum، المدة 4 Days
- Gingival Swab C/S: السعر 50، العينة Strile swab، المدة 3 Days
- Globulin: السعر 75، العينة Serum، المدة 2 Hours
- Glucose in Urine: السعر 10، العينة Urine، المدة 6 Hours
- Glycosylated Hb (HbA1c): السعر 30، العينة Edita whole blood، المدة 8 Hours
- Gram Stain: السعر 20، العينة sample، المدة 1 Days
- Growth Hormone: السعر 90، العينة Serum، المدة 2 Days
- Gum Discharge C/S: السعر 50، العينة Strile swab، المدة 3 Days
- H. Pylori IgA: السعر 80، العينة Serum، المدة 2 Days
- Haptoglobin: السعر 260، العينة Serum، المدة 2 Days
- HAV (Ig M): السعر 50، العينة Serum، المدة 1 Days
- HAV (IgG): السعر 50، العينة Serum، المدة 1 Day
- HAV Ab (total): السعر 50، العينة Serum، المدة 1 Days
- HBc IgG: السعر 45، العينة Serum، المدة 1 Days
- HBc IgM: السعر 45، العينة Serum، المدة 1 Days
- HBe Ab: السعر 45، العينة Serum، المدة 1 Days
- HBe Ag: السعر 45، العينة Serum، المدة 1 Days
- HBs Ab: السعر 45، العينة Serum، المدة 1 Days
- HBV-DNA by PCR (Quantitative): السعر 200، العينة Serum Edita، المدة 1 Days
- HCV - RNA by PCR (Quantitative): السعر 190، العينة Serum Edita، المدة 1 Days
- HCV Antibody (IgM): السعر 350، العينة Serum، المدة 1 Days
- HCV IgG (ELISA third generation): السعر Contact Lab، العينة Serum، المدة 1 Day
- HDL: السعر 18، العينة Serum Fasting، المدة 6 Hours
- HDV (IgM): السعر 375، العينة Serum، المدة 8 Days
- HDV (Total): السعر 375، العينة Serum، المدة 8 Days
- Helicobacter Pylori Antigen in Stool qualitative: السعر 65، العينة Stool، المدة 6 Hours
- Helicobacter Pylori Antigen in Stool Quantitative: السعر 75، العينة Stool، المدة 6 Hours
- Hemoglobin: السعر 15، العينة Edita whole blood، المدة 2 Hours
- Hemoglobin Electrophoresis: السعر 380، العينة EDTA Blood، المدة 3 Days
- Hepatitis Bs Antigen (HbsAg): السعر 35، العينة Serum، المدة 6 Hours
- Hepatitis C Virus (Ab): السعر 40، العينة Serum، المدة 6 Hours
- HER-2: السعر 740، العينة Paraffin blocks، المدة 10 Days
- Herpes simplex panel By PCR: السعر 2300، العينة CSF، المدة 2 Days
- Herpes Simplex Virus Type I IgG: السعر 40، العينة Serum، المدة 1 Days
- Herpes Simplex Virus Type I IgM: السعر 40، العينة Serum، المدة 1 Days
- Herpes Simplex Virus Type II IgG: السعر 40، العينة Serum، المدة 1 Days
- Herpes Simplex Virus Type II IgM: السعر 40، العينة Serum، المدة 1 Days
- HEV antibodies IgM: السعر 210، العينة Serum، المدة 4 Days
- HEV antibody IgG: السعر 800، العينة Serum، المدة 3 Days
- Histamine: السعر 3000، العينة Frozen plasma (EDTA or Heparin)، المدة 4 Days
- HIV-2 RNA PCR (Quantitative): السعر 1100، العينة Serum "Must be in a gel tube"، المدة 4 Days
- HIV-RNA PCR (Quantitative): السعر 1300، العينة Serum "Must be in a gel tube"، المدة 5 Days
- HLA-B27: السعر 500، العينة Edita whole blood، المدة 6 Days
- HOMA IR (Insulin Resistance test): السعر 70، العينة F. Serum، المدة 6 Hours
- Homocysteine: السعر 380، العينة Serum، المدة 2 Days
- HPV Human Papillomavirus PCR: السعر 750، العينة Vaginal swab in a transport medium، المدة 7 Days
- HPV IgG (Human papilloma virus): السعر 1200، العينة Serum، المدة 4 Days
- H-Pylori Ab (IgG) Qualitative: السعر 65، العينة Serum، المدة 6 Hours
- H-Pylori Ab (IgM): السعر 50، العينة Serum، المدة 6 Hours
- H-Pylori antibodies: السعر 50، العينة Serum، المدة 6 Hours
- hs-CRP: السعر 15، العينة Serum، المدة 1 Day
- Human Immunodeficiency Virus (HIV) Ab: السعر 50، العينة Serum، المدة 6 Hours
- Hydatid Ab: السعر 390، العينة Serum، المدة 3 Days
- IgA (TTG): السعر 280، العينة Serum، المدة 2 Days
- IgE (Immunoglobulin E Total): السعر 55، العينة Serum، المدة 1 Days
- IgE Food Allergy Panel: السعر 950، العينة Serum، المدة 15 Days
- IgE Inhalant allergy testing panel: السعر 850، العينة Serum، المدة 4 Days
- IGF-1 (Insulin like growth factor-1): السعر 350، العينة Serum، المدة 4 Days
- IgG TOTAL: السعر 60، العينة Serum، المدة 2 Days
- Immuno fixation: السعر 2200، العينة 2 (Serum tube - 2mL) For each unit، المدة 6 Days
- Immunoglobulin A: السعر 60، العينة Serum، المدة 2 Days
- Immunoglobulin G: السعر 55، العينة Serum، المدة 2 Days
- Immunoglobulin M: السعر 60، العينة Serum، المدة 2 Days
- Immunoglobulin-G (IgG) in CSF: السعر 200، العينة CSF، المدة 2 Days
- Immunoglobulin-G4 (IgG4): السعر 900، العينة Serum، المدة 3 Days
- Immunophenotyping by Flow Cytometry: السعر 2200، العينة Bone marrow aspirate، المدة 5 Days
- Inhibin A: السعر 2500، العينة Frozen Serum، المدة 4 Days
- Inhibin B: السعر 2500، العينة Frozen Serum، المدة 5 Days
- Insulin (Fasting): السعر 65، العينة Serum، المدة 6 Hours
- Insulin (Postprandial): السعر 65، العينة Serum، المدة 6 Hours
- Insulin Ab: السعر 305، العينة Serum، المدة 4 Days
- Insulin Glucose Ratio: السعر 70، العينة EDTA plasma، المدة 6 Hours
- Interleukin 6 (IL-6): السعر 250، العينة Serum، المدة 6 Hours
- Interleukin-28 (IL-B 28): السعر 1650، العينة Edita whole blood، المدة 5 Days
- Iron: السعر 18، العينة Serum، المدة 6 Hours
- Iron Profile: السعر Contact Lab، العينة Serum، المدة 1 Day
- k2 + (strooks, voodo): السعر 45، العينة Urine، المدة 6 Hours
- Ketone bodies: السعر 450، العينة EDTA Blood، المدة 2 Days
- Kidney Profile: السعر 24، العينة Serum، المدة 4 Hours
- Kleihauer-Betke test: السعر 550، العينة Edita whole blood، المدة 3 Days
- Knee aspirate C/S: السعر 50، العينة Ascitic، المدة 5 Days
- L- Lactate: السعر 60، العينة Serum on fluride tube، المدة 6 Hours
- L.E. Cells: السعر 90، العينة Serum، المدة 1 Days
- Lactoferrin in stool: السعر 500، العينة Stool، المدة 2 Days
- LDH: السعر 12، العينة Serum، المدة 6 Hours
- LDL: السعر 32، العينة Serum، المدة 6 Hours
- LDL/HDL: السعر Contact Lab، العينة Serum، المدة 4 Hours
- Left Conjunctival Swab C/S: السعر 50، العينة Sterile swab، المدة 3 Days
- Left Ear Discharge C/S: السعر 50، العينة Sterile swab، المدة 3 Days
- Left Nipple Discharge C/S: السعر 50، العينة Sterile swab، المدة 3 Days
- Leishmania: السعر 1200، العينة Serum، المدة 2 Days
- Leptin: السعر 600، العينة Serum، المدة 4 Days
- Leucocytes: السعر 12، العينة Edita whole blood، المدة 2 Hours
- Leutinizing Hormone (LH): السعر 30، العينة Serum، المدة 6 Hours
- Lipase: السعر 38، العينة Serum، المدة 6 Hours
- Lipid Profile: السعر 45، العينة Serum، المدة 4 Hours
- Lipoprotein (a): السعر 300، العينة Serum، المدة 2 Days
- Lithuim: السعر 60، العينة Serum، المدة 1 Days
- Liver Function: السعر 40، العينة Serum، المدة 4 Hours
- liver profile basic: السعر 16، العينة Serum، المدة 6 Hours
- LKM-Ab: السعر 250، العينة Serum، المدة 4 Days
- Lupus Anticoagulant: السعر 80، العينة Citrated plasma، المدة 1 Days
- Lymphocyte subsets Cell Count CD3, CD4, CD8,CD19,(CD16/CD56): السعر 2300، العينة Edita whole blood، المدة 5 Days
- M2PK (Schebo test) (pyruvate kinase isoenzyme M2) Stool: السعر 1650، العينة Stool، المدة 4 Days
- Magnesium in Urine (24 hrs): السعر 12، العينة Urine، المدة 6 Hours
- Malaria Ab (Anti-Plasmodium IgG): السعر 520، العينة Serum، المدة 3 Days
- Malaria Ag: السعر 360، العينة Edita whole blood، المدة 1 Days
- Malaria Film: السعر 20، العينة Edita whole blood، المدة 1 Days
- methamphetamine (crystal ice, shaboo): السعر 45، العينة Urine، المدة 6 Hours
- Methotrexate: السعر 1850، العينة Serum، المدة 2 Days
- Microalbuminuria: السعر 45، العينة Urine، المدة 6 Hours
- Milk + Gluten Panel: السعر 1200، العينة Serum، المدة 4 Days
- Monospot Test (Paul-Bunnell): السعر 50، العينة Serum، المدة 1 Days
- Multiplex PCR for Pathogens Causing Diarrhea: السعر 7500، العينة Stool، المدة 3 Days
- Myoglobin: السعر 210، العينة Serum، المدة 2 Days
- Myoglobin in urine: السعر 210، العينة Urine، المدة 2 Days
- Nail Scarping KOH: السعر 130، العينة Skin, scalp or nail، المدة 10 Days
- Nail Scraping C/S: السعر 130، العينة Skin, scalp or nail، المدة 3 Days
- Nasal Discharge C/S: السعر 50، العينة Sterile swab، المدة 3 Days
- Neuron Specific Enolase (NSE): السعر 1200، العينة Paraffin blocks or non hemolyzed، المدة 10 Days
- new blood film: السعر 30، العينة Edita whole blood، المدة 8 Hours
- Nicotine in Blood (Quantitative) (tobacco - smoking): السعر 250، العينة Serum، المدة 2 Days
- Nicotine in Urine (tobacco - smoking): السعر 65، العينة Urine، المدة 6 Hours
- NK cells (CD16/CD56): السعر 900، العينة 4 (EDTA tube - 2mL)، المدة 5 Days
- Occult Blood in Stool: السعر 35، العينة Stool، المدة 6 Hours
- Oligoclonal bands in CSF: السعر 2500، العينة CSF، المدة 5 Days
- Oral Glucose Tolerance Test: السعر 40، العينة Serum on fluride tube، المدة 6 Hours
- Osmolality in Urine 24 hrs: السعر 70، العينة Urine، المدة 2 Days
- Osmotic Fragility: السعر 30، العينة Fresh heparinized blood (3 mL)، المدة 1 Days
- Osteocalcin in Serum (N-MID): السعر 200، العينة Serum، المدة 2 Days
- OX19 Ab (Weil-Felix test): السعر 130، العينة Serum، المدة 2 Days
- Pancreatic amylase: السعر 140، العينة Serum، المدة 1 Day
- Pancreatic elastase: السعر 1600، العينة Serum، المدة 1 Day
- Pap smear: السعر 450، العينة Smear، المدة 10 Days
- Parathyroid Hormone (PTH): السعر 95، العينة 2.0 ml. frozen EDTA plasma or Serum، المدة 8 Hours
- Parental testing: السعر 11000، العينة 5 EDTA Blood، المدة 60 Days
- Partial Thromboplastin Time (PTT): السعر 16، العينة Citrated plasma، المدة 6 Hours
- Pathology Report: السعر 500، العينة Sample، المدة 10 Days
- PATHOLOGY REPORT (Organ): السعر 1200، العينة Sample، المدة 10 Days
- PATHOLOGY REPORT (Very Large): السعر 850، العينة Sample، المدة 10 Days
- PATHOLOGY REPORT (Large): السعر 1000، العينة Sample، المدة 10 Days
- PATHOLOGY REPORT (medium): السعر 600، العينة Sample، المدة 10 Days
- PATHOLOGY REPORT (small): السعر 500، العينة Sample، المدة 10 Days
- PCR for Brucella: السعر 1050، العينة EDTA blood (1 mL)، المدة 4 Days
- PCR for CMV: السعر 850، العينة EDTA plasma، المدة 5 Days
- PCR for Familial Mediterranean Fever Gene Mutation: السعر 900، العينة EDTA Blood، المدة 3 Days
- PCR for H1N1 influenza virus (Swine flu): السعر 900، العينة Nasopharyngeal swab، المدة 3 Days
- PCR for HCV genotyping: السعر 1000، العينة EDTA Blood (5 mL)، المدة 5 Days
- PCR for HEV: السعر 1400، العينة EDTA Plasma، المدة 3 Days
- PCR for HLA-B5: السعر 1000، العينة EDTA Blood، المدة 6 Days
- PCR for HLA-B51: السعر 1000، العينة EDTA Blood، المدة 6 Days
- PCR for HLA-B57: السعر 1000، العينة EDTA Blood، المدة 6 Days
- PCR for HLA-Typing - Class I (A): السعر 1900، العينة Edita whole blood، المدة 6 Days
- PCR for HLA-Typing - Class I (B) (Reverse hybridization): السعر 2000، العينة EDTA Blood، المدة 6 Days
- PCR for HLA-Typing - Class II (DRB1): السعر 1500، العينة Edita whole blood، المدة 6 Days
- PCR for JAK2 gene mutation: السعر 2000، العينة Edita whole blood، المدة 6 Days
- PCR for Methylene tetrahydrofolateReductase Gene Mutation (MTHFR): السعر 650، العينة Edita whole blood، المدة 7 Days
- PCR for MRSA (GeneXpert): السعر 1000، العينة Swab، المدة 3 Days
- PCR for Prothrombin gene mutation: السعر 1000، العينة EDTA Blood، المدة 5 Days
- Peroxidase test(leuco screen): السعر 60، العينة Seminal Fluid في انبوبة وزرمان، المدة 2 Days
- pH in Blood: السعر 100، العينة Heparinized Whole blood، المدة 1 Hours
- pH in Stool: السعر 10، العينة Stool، المدة 6 Hours
- pH in Urine (spot sample): السعر 10، العينة Urine، المدة 6 Hours
- Phenobarbital: السعر 800، العينة Serum، المدة 3 Days
- Phenytoin (Epanutin): السعر 110، العينة Serum، المدة 2 Days
- Phosphorus in urine (24hrs): السعر 12، العينة Urine، المدة 6 Hours
- Plasminogen, Plasma: السعر 400، العينة Edita whole blood، المدة 3 Days
- Platelet Function: السعر 850، العينة Fresh Edita whole blood، المدة 3 Days
- Platelets Count: السعر 15، العينة Edita whole blood، المدة 6 Hours
- Pleural Fluid C/S: السعر 50، العينة Fluid، المدة 5 Days
- Pleural Fluid Examination: السعر 75، العينة Fluid، المدة 6 Hours
- PNH (CD55/CD59): السعر 950، العينة Edita whole blood، المدة 5 Days
- Postprandial Blood Glucose: السعر 10، العينة Floride tube، المدة 6 Hours
- potassium in urine: السعر Contact Lab، العينة Urine، المدة 4 Hours
- Pregnancy test: السعر 15، العينة Serum or Urine، المدة 6 Hours
- Pro-BNP(Pro B-type natriuretic peptide): السعر 650، العينة Serum، المدة 2 Days
- Procalcitonin PCT-Q: السعر 230، العينة Serum، المدة 6 Hours
- Progesterone: السعر 50، العينة Serum، المدة 6 Hours
- Prolactin: السعر 30، العينة Serum، المدة 6 Hours
- Prostatic Discharge C/S: السعر 50، العينة Discharge، المدة 3 Days
- Protein "C": السعر 250، العينة Citrated plasma، المدة 4 Days
- Protein "S": السعر 250، العينة Citrated plasma، المدة 4 Days
- Protein immunofixation (serum): السعر 2000، العينة Serum، المدة 6 Days
- Protein immunofixation in urine: السعر 1500، العينة Urine، المدة 6 Days
- Protein in Urine (24hrs): السعر 15، العينة 24 hrs. Urine، المدة 6 Hours
- Prothrombine Time (PT): السعر 12، العينة 1.8ml blood on 0.2 citrate and sent immediately frozen، المدة 2 Hours
- PSA Profile: السعر 92، العينة Serum، المدة 6 Hours
- Pus C/S: السعر 50، العينة Sterile swab، المدة 3 Days
- Pus Discharge C/S: السعر 50، العينة Sterile swab، المدة 3 Days
- Pyruvate: السعر 350، العينة Edita whole blood، المدة 2 Days
- QuantiFERON-TB Gold: السعر 1200، العينة 4 tubes of lithium heparine، المدة 3 Days
- Random Blood Glucose: السعر 10، العينة Fasting Serum on floride tue، المدة 6 Hours
- Reducing Substance in Stool: السعر 35، العينة Stool، المدة 8 Hours
- Reducing substances in urine: السعر 35، العينة Urine، المدة 1 Days
- Renin level: السعر 620، العينة Frozen morning EDTA plasma، المدة 6 Days
- Reticulocyte Count: السعر 15، العينة Edita whole blood، المدة 8 Hours
- Rh antibody titre: السعر 120، العينة Serum، المدة 1 Days
- Rh Grouping: السعر 10، العينة Edita whole blood، المدة 6 Hours
- Rheumatoid Factor (RF): السعر 40، العينة Serum، المدة 6 Hours
- Right Conjunctival Swab C/S: السعر 50، العينة Strile swab، المدة 3 Days
- Right Ear Discharge C/S: السعر 50، العينة Strile swab، المدة 3 Days
- Right Nipple Discharge C/S: السعر 50، العينة Strile swab، المدة 3 Days
- Rose Waaler Test: السعر 30، العينة Serum، المدة 2 Days
- RF LATEX: السعر 20، العينة Serum، المدة 1 Days
- Routine fungal culture: السعر 375، العينة Sample، المدة 10 Days
- RPR: السعر 40، العينة Serum، المدة 1 Days
- Rubella IgG Ab: السعر 40، العينة Serum، المدة 1 Days
- Rubella IgM Ab: السعر 40، العينة Serum، المدة 1 Days
- S. Magnesium (Mg): السعر 12، العينة Serum، المدة 6 Hours
- S.G.O.T (AST): السعر 10، العينة Serum، المدة 6 Hours
- S.G.P.T (ALT): السعر 10، العينة Serum، المدة 6 Hours
- SAAG Ratio: السعر 40، العينة Peritoneal (Ascitic) Fluid + Serum، المدة 1 Day
- Schistosoma (Bilharzia) Ab (IHA): السعر 140، العينة Serum، المدة 1 Days
- Schistosoma (Bilharzia) Ab. (IgG): السعر 390، العينة Serum، المدة 3 Days
- Schistosoma (Bilharzia) Ab. (IgM): السعر 390، العينة Serum، المدة 3 Days
- Schistosoma (Bilharzia) Ag: السعر 200، العينة Urine، المدة 2 Days
- Screening for (THC): السعر 45، العينة Urine، المدة 6 Hours
- Screening for Amphetamine: السعر 45، العينة Urine، المدة 6 Hours
- Screening for Barbiturates (BAR): السعر 45، العينة Urine، المدة 6 Hours
- Screening for Benzodizepines (Valium): السعر 45، العينة Urine، المدة 6 Hours
- Screening for Canabinoid (Hashish, Banjo): السعر 45، العينة Urine، المدة 6 Hours
- Screening for Cocaine (COCAIN): السعر 45، العينة Urine، المدة 6 Hours
- Screening for Herion: السعر 45، العينة Urine، المدة 6 Hours
- Screening for Met - Amphetamine: السعر 45، العينة Urine، المدة 6 Hours
- Screening for Morphine: السعر 45، العينة Urine، المدة 6 Hours
- Screening for Opiates (MOP, Heroin): السعر 45، العينة Urine، المدة 6 Hours
- Semen Analysis: السعر 20، العينة semen، المدة 6 Hours
- Semen C/S: السعر 50، العينة semen، المدة 3 Days
- Serous Fluid C/S: السعر 50، العينة Fluid، المدة 3 Days
- Serum Sodium (Na): السعر 12، العينة Serum، المدة 2 Hours
- Serum Albumin: السعر 10، العينة Serum، المدة 6 Hours
- Serum Aldosterone Hormone: السعر 450، العينة Serum، المدة 5 Days
- Serum Amylase: السعر 22، العينة Serum، المدة 6 Hours
- serum bicarbonate (total CO2): السعر 120، العينة Serum، المدة 6 Hours
- Serum Bilirubin profile: السعر 16، العينة Serum، المدة 6 Hours
- Serum Calcium: السعر 12، العينة Serum، المدة 6 Hours
- Serum Creatinine: السعر 10، العينة Serum، المدة 6 Hours
- Serum GGT: السعر 12، العينة Serum، المدة 6 Hours
- Serum ionized Calcium: السعر 18، العينة Serum، المدة 4 Hours
- Serum Osmolality (estimated): السعر 65، العينة Serum، المدة 2 Days
- Serum Osmolality: السعر 70، العينة Serum، المدة 2 Days
- Serum Phosphorus: السعر 12، العينة Serum، المدة 6 Hours
- Serum Potassium(K): السعر 12، العينة Serum، المدة 2 Hours
- Serum Protein Electrophoresis: السعر 320، العينة Serum، المدة 3 Days
- Serum Triglycerides: السعر 10، العينة Serum Fasting، المدة 6 Hours
- Serum uric acid: السعر 10، العينة Serum، المدة 6 Hours
- Sex Hormone Binding Globulin: السعر 115، العينة Serum، المدة 2 Days
- Sirolimus (Rapamycin): السعر 520، العينة EDTA blood، المدة 5 Days
- Sodium and Potassium (Serum): السعر 24، العينة Serum، المدة 2 Hours
- Sodium in Urine: السعر 12، العينة Urine، المدة 6 Hours
- Specific IgE for Candida albicans: السعر 220، العينة Serum، المدة 4 Days
- Sputum C/S: السعر 50، العينة Sputume، المدة 3 Days
- Stone Analysis: السعر 35، العينة Urinary stone، المدة 2 Days
- Stool Analysis: السعر 10، العينة Stool، المدة 6 Hours
- Stool C/S: السعر 50، العينة Stool، المدة 3 Days
- Synthetic Marijuana (Strox): السعر 45، العينة Urine، المدة 6 Hours
- Synthetic Marijuana (Voodoo): السعر 45، العينة Urine، المدة 6 Hours
- Syphilis ab: السعر 50، العينة Serum، المدة 1 Days
- T Uptake: السعر 110، العينة Serum، المدة 1 Days
- T.B Culture: السعر 600، العينة Sterile body Fluids, aspirate and tissue ...etc، المدة 45 Days
- T3: السعر 22، العينة Serum، المدة 6 Hours
- T3 (Free): السعر 22، العينة Serum، المدة 6 Hours
- T3 And T4: السعر 44، العينة Serum، المدة 6 Hours
- T4: السعر 22، العينة Serum، المدة 6 Hours
- T4 (Free): السعر 22، العينة Serum، المدة 6 Hours
- Tacrolimus (FK 506) (Prograf®): السعر 750، العينة Edita whole blood، المدة 3 Days
- TB-DNA by PCR: السعر 850، العينة Any biological Fluid، المدة 5 Days
- TB Antibody: السعر 130، العينة Serum، المدة 2 Days
- TBG (Thyroxine binding globulin): السعر 280، العينة Serum، المدة 2 Days
- Testosterone (Free): السعر 40، العينة Serum، المدة 6 Hours
- Testosterone (Total): السعر 40، العينة Serum، المدة 6 Hours
- Theophylline: السعر 380، العينة Serum، المدة 2 Days
- Thick Film Malaria: السعر 20، العينة Edita whole blood، المدة 1 Days
- Throat Swab C/S: السعر 50، العينة Sterile swab، المدة 3 Days
- Thyroglobulin: السعر 120، العينة Serum، المدة 6 Hours
- Thyroid Anti-Microsomal Ab.: السعر 80، العينة Serum، المدة 6 Hours
- Thyroid Anti-Peroxidase Ab.: السعر 80، العينة Serum، المدة 6 Hours
- Tissue transglutaminase IgG: السعر 280، العينة Serum، المدة 4 Days
- Tongue Swab C/S: السعر 50، العينة Sterile swab، المدة 3 Days
- Total Bilirubin: السعر 10، العينة Serum، المدة 4 Hours
- Total Body Protein: السعر 15، العينة Serum، المدة 6 Hours
- Total Cholesterol: السعر 10، العينة Serum Fasting، المدة 6 Hours
- Total Iron binding capacity (TIBC): السعر 30، العينة Serum، المدة 6 Hours
- Total Kappa light chain: السعر 200، العينة Serum، المدة 2 Days
- Total Lambda light chain: السعر 180، العينة Serum، المدة 2 Days
- Total Lipids: السعر 45، العينة Serum، المدة 1 Days
- Total Metanephrine: السعر 400، العينة 24h Urine، المدة 8 Days
- Total Prostatic Specific Ag (PSA): السعر 40، العينة Serum، المدة 6 Hours
- Total Protein: السعر 10، العينة Serum، المدة 6 Hours
- Toxoplasma IgG Ab: السعر 40، العينة Serum، المدة 1 Days
- Toxoplasma IgM Ab: السعر 40، العينة Serum، المدة 1 Days
- Tramadol: السعر 45، العينة Urine، المدة 1 Days
- Transferrin: السعر 85، العينة Serum، المدة 6 Hours
- Transferrin Saturation: السعر 80، العينة Serum، المدة 6 Hours
- Treponema pallidum hemagglutination assay (IHA): السعر 90، العينة Serum، المدة 2 Days
- Trichinella spiralis Ab: السعر 1300، العينة Serum، المدة 6 Days
- Trig/HDL: السعر Contact Lab، العينة Serum، المدة 4 Hours
- Triple Marker (2nd trimester) (15-20 w): السعر 800، العينة Serum، المدة 4 Days
- Triple Test: السعر 600، العينة Serum، المدة 4 Days
- Troponin - I: السعر 45، العينة Serum، المدة 6 Hours
- Troponin - T: السعر 200، العينة Serum، المدة 1 Day
- Troponin I (High sensitive): السعر 170، العينة Serum، المدة 2 Days
- Trypsin: السعر 160، العينة Serum، المدة 2 Days
- TSH: السعر 23، العينة Serum، المدة 6 Hours
- TSH ULTRA SENSITIVE: السعر 23، العينة Serum، المدة 1 Day
- Urea Clearance: السعر 15، العينة Serum (300 µL) + 24h Urine، المدة 6 Hours
- Urethral Discharge C/S: السعر 50، العينة Discharge، المدة 3 Days
- Uric Acid in Urine (24hrs): السعر 10، العينة Urine 24 hrs، المدة 6 Hours
- Urinary VMA (24hrs): السعر 400، العينة 24h Urine، المدة 3 Days
- Urine albumin / Creatinine ratio: السعر 45، العينة Urine، المدة 6 Hours
- Urine Analysis: السعر 10، العينة Urine، المدة 6 Hours
- Urine C/S: السعر 50، العينة Urine، المدة 3 Days
- Urine Examination After Massage: السعر 10، العينة Urine، المدة 6 Hours
- Urine Examination Before Massage: السعر 10، العينة Urine، المدة 6 Hours
- Urine Osmolality (random): السعر 80، العينة Random Urine، المدة 1 Days
- Urine total protein/ Creatinine ratio: السعر Contact Lab، العينة Serum + Urine، المدة 4 Hours
- Urine total protein/ Creatinine ratio (24hrs): السعر 30، العينة 24 hrs. Urine، المدة 6 Hours
- Vaginal Swab C/S: السعر 50، العينة Sterile swab، المدة 3 Days
- Varicella (chickenpox) IgG: السعر 300، العينة Serum، المدة 2 Days
- VDRL (syphilis): السعر 40، العينة Serum، المدة 1 Days
- Vitamin B12: السعر 170، العينة Serum، المدة 1 Day
- Vitamin D (25-OH vitamin D total): السعر 130، العينة Serum، المدة 6 Hours
- Vitamin D 3: السعر 130، العينة Serum، المدة 6 Hours
- VLDL: السعر 50، العينة Serum، المدة 1 Days
- Vomitus C/S: السعر 50، العينة sample، المدة 3 Days
- White Cell Count: السعر 12، العينة Edita blood، المدة 4 Hours
- Widal Test: السعر 20، العينة Serum، المدة 6 Hours
- Wound Swab C/S: السعر 50، العينة Sterile swab، المدة 3 Days
- Ziehl Neelsen Stain: السعر 35، العينة Sputum، المدة 1 Days
- Ziehl Neelsen Stain (Urine): السعر 35، العينة Urine، المدة 1 Days
- Ziehl Neelsen Stain 3 samples: السعر 105، العينة Sputum، المدة 3 Days
- Zinc (Serum): السعر 70، العينة Serum، المدة 6 Hours
- Zn in Urine (24 hrs): السعر 70، العينة Serum، المدة 6 Hours
""",
    '🏜️ برايس طارق للصعيد': r"""
- 1-25 OH-Vitamin D: السعر 265
- 17 OH progesterone: السعر 150
- A/G Ratio: السعر 30
- ABO Group: السعر 25
- Acetone in Urine: السعر 15
- ACTH (AM): السعر 110
- ACTH (PM): السعر 110
- ACTH Random: السعر 110
- Acti Fibro test: السعر 4000
- ADA: السعر 120
- ADA(Adenosine Deaminase in Ascitic Fluid): السعر 120
- ADA(Adenosine Deaminase in serum): السعر 120
- Albumin / Creatinine ratio (A/C %): السعر 60
- Aldolase: السعر 250
- Alk Phosphatase: السعر 15
- Alpha - 1 Anti trypsin: السعر 160
- Alpha Feto Protein in serum: السعر 80
- Alpha-glucosidase in semen: السعر 600
- AMA: السعر 250
- AMH (Anti Mullerian Hormone): السعر 230
- Ammonia: السعر 100
- Amylase in Urine: السعر 35
- Amyloid A: السعر 195
- ANA: السعر 100
- ANA by Immunofluorescence: السعر 240
- ANCA C (Cytoplasmic): السعر 200
- ANCA P (Perinuclear): السعر 200
- Androstenedione: السعر 300
- Angiotensin converting Enzyme: السعر 400
- AnSCL 70 Antibody: السعر 250
- Anti - (d.s) DNA: السعر 140
- Anti - CCP Antibody (Ab): السعر 185
- Anti - Gliadin Antibody (IgG): السعر 380
- Anti - Parietal Antibody: السعر 250
- Anti - Phospholipid Antibody (IgG): السعر 200
- Anti - Phospholipid Antibody (IgM): السعر 200
- Anti - Platelet Antibody (Direct): السعر 600
- Anti - Platelet Antibody (Indirect): السعر 600
- Anti - RNP Antibody: السعر 300
- Anti - ss - A/Ro Antibody: السعر 245
- Anti-ss-B/La Antibody: السعر 245
- Anti GAD (Anti-glutamic acid decarboxylase): السعر 1300
- ASOT LATEX: السعر 25
- Anti MuSK (muscle specific tyrosine kinase): السعر 5000
- Anti Smooth muscle Antibodies (ASMA): السعر 245
- Anti Streptolysin (ASOT): السعر 55
- Anti thyroid Antibody: السعر 120
- Anti Tissue transglutaminase Ab IgA: السعر 250
- Anti-B2 Glycoprotein(IgG): السعر 250
- Anti-B2 Glycoprotein (IgM): السعر 250
- Anticardiolipin IgG: السعر 170
- Anticardiolipin IgM: السعر 170
- Anti-Smith Antibody: السعر 250
- Antisperm Antibody (IgG): السعر 240
- Antisperm Antibody (IgM): السعر 240
- Anti-Sperm Antibody in Semen: السعر 240
- AntiSperm Antibody: السعر 240
- Antithrombin III: السعر 135
- Anti-thyroglobulin Antibody (ATG): السعر 120
- Anti-TSH receptor antibody: السعر 385
- ASCA Antibody (IgA): السعر 250
- ASCA Antibody (IgG): السعر 250
- Ascitic fluid C/S: السعر 120
- Ascitic Fluid Examination: السعر 100
- B2 Microglobuilin: السعر 130
- B2 Microglobulin in urine: السعر 140
- BCR-ABL Minor (p190) gene by Real Time PCR: السعر 2200
- Bence Jones protein in urine: السعر 40
- BHCG: السعر 70
- Blood C/S: السعر 190
- Blood film: السعر 45
- Blood Urea: السعر 15
- Body Fluid Culture: السعر 110
- Brucella IgG: السعر 300
- Brucella IgM: السعر 300
- Brucella Test: السعر 25
- BUN: السعر 15
- C- Peptide (Fasting): السعر 105
- C - Peptide (Postprandial): السعر 105
- C. Reactive Protein (CRP): السعر 45
- C3: السعر 65
- C4: السعر 65
- CA 125: السعر 105
- CA 15.3: السعر 105
- CA 19.9: السعر 105
- Calcitonin: السعر 900
- Calcium in Urine (24hrs): السعر 15
- Calcium/Creatinine ratio: السعر 25
- Calprotectin Stool Quantitative: السعر 260
- Carbamazepin (Tegretol): السعر 95
- Catecholamines in Urine (24 hrs): السعر 2850
- CEA: السعر 90
- Ceruloplasmin: السعر 80
- Cervical Swab C/S: السعر 120
- Chlamydia Antibody (IgG): السعر 285
- Chloride (Serum): السعر 30
- Chloride Urine (24 hrs): السعر 30
- Cholinestrase: السعر 500
- CMV Antibody (IgG): السعر 85
- CMV Antibody (IgM): السعر 85
- Complete Blood Count: السعر 50
- Complete Blood Count (CBC): السعر 50
- Comprehensive Metabolic Panel: السعر 1350
- Coombs' Test (Direct): السعر 40
- Coombs' Test (Indirect): السعر 45
- Copper: السعر 70
- Copper in Urine (24 hrs): السعر 70
- Cortisol 9 am: السعر 100
- Cortisol (Random): السعر 100
- Cortisol 9 pm: السعر 100
- Cortisol In Urine (24 hrs): السعر 100
- CPK: السعر 25
- CPK (MB): السعر 70
- Creatinine Clearance: السعر 30
- Creatinine in urine: السعر 15
- Cryoglobulin: السعر 80
- CSF C/S: السعر 120
- CSF examination: السعر 150
- CRP LATEX: السعر 25
- Culture Report: السعر 110
- Cyclosporine (Sandimmune): السعر 400
- D-Dimer: السعر 135
- Depakine (Valproic Acid): السعر 115
- DHEA: السعر 115
- DHEA-S: السعر 115
- Differential Leucocytic Count (WBCs): السعر 25
- Digoxin (Lanoxin) therapeutic level: السعر 350
- dihydrotestosterone (DHT): السعر 500
- Direct Bilirubin: السعر 15
- Drugs Screening: السعر 200
- E.S.R: السعر 35
- EBV Antibody (IgG): السعر 265
- EBV Antibody (IgM): السعر 265
- eGFR: السعر 60
- Endomysial IgA (IFA): السعر 500
- Endomysial IgG (IFA): السعر 500
- Entamoeba histolytica Ab: السعر 300
- Epanutin (Phenytoin, dilantin): السعر 150
- Estradiol (E2): السعر 50
- Estriol (E3): السعر 300
- Ethanol (Alcohol) level: السعر 200
- Extractable Nuclear Antigens (ENA) Panel: السعر 750
- F.D.P: السعر 220
- Factor - IX: السعر 700
- Factor - VIII: السعر 700
- Factor V: السعر 700
- Factor V Leiden Mutation By PCR: السعر 550
- Factor VII (F. 7): السعر 700
- Factor X (F. 10): السعر 700
- Factor XI (F. 11): السعر 1000
- Factor XII (F. 12): السعر 1000
- Fasciola Ab Titre: السعر 300
- Fasciola Ab: السعر 300
- Fasting Blood Glucose: السعر 15
- Ferritin: السعر 55
- Fibrin/ Fibrinogen Degradation Products (FDP): السعر 220
- Fibrinogen: السعر 80
- Filaria Ag: السعر 300
- Filaria antibodies: السعر 300
- Filaria Film: السعر 50
- Fluid Amylase: السعر 35
- Fluid C/S: السعر 110
- Fluid Lipase: السعر 35
- Folic Acid: السعر 220
- Food Allergy Panel: السعر 8000
- Free Metanephrine: السعر 2850
- Free Prostatic Specific Ag (PSA): السعر 85
- Fructosamine: السعر 65
- Fructose in semen: السعر 45
- FSH: السعر 41
- FTI: السعر 300
- Fungal stain: السعر 65
- G6PD (Quantitative): السعر 95
- Globulin: السعر 22
- Glucose in Urine: السعر 15
- Glycosylated Hb (HbAlc): السعر 32
- Gram Stain: السعر 35
- Growth Hormone: السعر 95
- H. Pylori IgA: السعر 120
- Haptoglobin: السعر 105
- HAV (Ig M): السعر 115
- HAV (IgG): السعر 115
- HAV Ab (total): السعر 115
- HBc IgG: السعر 105
- HBc IgM: السعر 105
- HBe Ab: السعر 105
- HBe Ag: السعر 105
- HBs Ab: السعر 75
- HBV-DNA by PCR (Quantitative): السعر 250
- HCV - RNA by PCR (Quantitative): السعر 250
- HCV Antibody (IgM): السعر 500
- HCV IgG (ELISA third generation): السعر 130
- HDL: السعر 30
- HDV (IgM): السعر 450
- HDV (Total): السعر 450
- Helicobacter Pylori Antigen in Stool qualitative: السعر 100
- Helicobacter Pylori Antigen in Stool Quantitative: السعر 100
- Hemoglobin: السعر 20
- Hemoglobin Electrophoresis: السعر 180
- Hepatitis Bs Antigen (HbsAg): السعر 95
- Hepatitis C Virus (Ab): السعر 130
- Herpes Simplex Virus Type I IgG: السعر 105
- Herpes Simplex Virus Type I IgM: السعر 105
- Herpes Simplex Virus Type II IgG: السعر 135
- Herpes Simplex Virus Type II IgM: السعر 135
- HEV antibodies IgM: السعر 300
- HEV antibody IgG: السعر 300
- HIV-2 RNA PCR (Quantitative): السعر 700
- HIV-RNA PCR (Quantitative): السعر 700
- HLA-B27: السعر 550
- HOMA IR (Insulin Resistance test): السعر 100
- Homocysteine: السعر 315
- H-Pylori Ab (IgG) Qualitative: السعر 95
- H-Pylori Ab (IgM): السعر 120
- H-Pylori antibodies: السعر 95
- hs-CRP: السعر 200
- Human Immunodeficiency Virus (HIV) Ab: السعر 100
- Hydatid Ab: السعر 250
- IgA (TTG): السعر 250
- IgE (Immunoglobulin E Total): السعر 90
- IgE Food Allergy Panel: السعر 1400
- IgE Inhalant allergy testing panel: السعر 1400
- IGF-1 (Insulin like growth factor-1): السعر 450
- IgG TOTAL: السعر 65
- Immuno fixation: السعر 2300
- Immunoglobulin A: السعر 65
- Immunoglobulin G: السعر 65
- Immunoglobulin M: السعر 65
- Immunoglobulin-G (IgG) in CSF: السعر 200
- Immunoglobulin-G4 (IgG4): السعر 1000
- Insulin (Fasting): السعر 95
- Insulin (Postprandial): السعر 95
- Insulin Ab: السعر 320
- Interleukin 6 (IL-6): السعر 220
- Iron: السعر 25
- Ketone bodies: السعر 15
- L- Lactate: السعر 80
- L.E. Cells: السعر 150
- Lactoferrin in stool: السعر 1200
- LDH: السعر 20
- LDL: السعر 35
- Left Conjunctival Swab C/S: السعر 110
- Left Nipple Discharge C/S: السعر 110
- Leptin: السعر 950
- Leucocytes: السعر 22
- Leutinizing Hormone (LH): السعر 41
- Lipase: السعر 35
- Lipid Profile: السعر 70
- Lithuim: السعر 260
- LKM-Ab: السعر 250
- Lupus Anticoagulant: السعر 125
- M2PK (Schebo test) (pyruvate kinase isoenzyme M2) Stool: السعر 1815
- Magnesium in Urine (24 hrs): السعر 22
- Malaria Ab (Anti-Plasmodium IgG): السعر 600
- Malaria Ag: السعر 200
- Malaria Film: السعر 50
- Microalbuminuria: السعر 60
- Monospot Test (Paul-Bunnell): السعر 55
- Nail Scarping KOH: السعر 65
- Nail Scraping C/S: السعر 160
- Nasal Discharge C/S: السعر 120
- new blood film: السعر 45
- Nicotine in Urine (tobacco - smoking): السعر 300
- Occult Blood in Stool: السعر 55
- Oral Glucose Tolerance Test: السعر 65
- Osmolality in Urine 24 hrs: السعر 65
- Osmotic Fragility: السعر 55
- Pancreatic amylase: السعر 35
- Parathyroid Hormone (PTH): السعر 130
- Partial Thromboplastin Time (PTT): السعر 40
- PCR for CMV: السعر 550
- PCR for Familial Mediterranean Fever Gene Mutation: السعر 1350
- PCR for JAK2 gene mutation: السعر 700
- PCR for Methylene tetrahydrofolateReductase Gene Mutation (MTHFR): السعر 550
- PCR for MRSA (GeneXpert): السعر 300
- PCR for Prothrombin gene mutation: السعر 550
- pH in Blood: السعر 20
- pH in Stool: السعر 20
- pH in Urine (spot sample): السعر 20
- Phenytoin (Epanutin): السعر 150
- Phosphorus in urine (24hrs): السعر 20
- Platelets Count: السعر 22
- Pleural Fluid C/S: السعر 110
- Pleural Fluid Examination: السعر 100
- Postprandial Blood Glucose: السعر 15
- potassium in urine: السعر 22
- Pregnancy test: السعر 70
- Pro-BNP(Pro B-type natriuretic peptide): السعر 510
- Procalcitonin PCT-Q: السعر 500
- Progesterone: السعر 50
- Prolactin: السعر 41
- Prostatic Discharge C/S: السعر 110
- Protein "C": السعر 340
- Protein "S": السعر 340
- Protein immunofixation (serum): السعر 2300
- Protein immunofixation in urine: السعر 2300
- Protein in Urine (24hrs): السعر 45
- Prothrombine Time (PT): السعر 35
- PSA Profile: السعر 80
- Pus C/S: السعر 120
- Pus Discharge C/S: السعر 120
- Pyruvate: السعر 250
- QuantiFERON-TB Gold: السعر 1700
- Random Blood Glucose: السعر 15
- Reducing Substance in Stool: السعر 50
- Reducing substances in urine: السعر 50
- Renin level: السعر 450
- Reticulocyte Count: السعر 450
- Rh antibody titre: السعر 60
- Rh Grouping: السعر 22
- Rheumatoid Factor (RF): السعر 47
- Right Conjunctival Swab C/S: السعر 110
- Right Ear Discharge C/S: السعر 110
- Right Nipple Discharge C/S: السعر 110
- Rose Waaler Test: السعر 47
- RF LATEX: السعر 20
- Routine fungal culture: السعر 160
- RPR: السعر 60
- Rubella IgG Ab: السعر 85
- Rubella IgM Ab: السعر 85
- S. Magnesium (Mg): السعر 22
- S.G.O.T (AST): السعر 15
- S.G.P.T (ALT): السعر 15
- Schistosoma (Bilharzia) Ab (IHA): السعر 155
- Schistosoma (Bilharzia) Ab. (IgG): السعر 155
- Schistosoma (Bilharzia) Ab. (IgM): السعر 155
- Schistosoma (Bilharzia) Ag: السعر 200
- Screening for (THC): السعر 70
- Screening for Amphetamine: السعر 70
- Screening for Barbiturates (BAR): السعر 70
- Screening for Benzodizepines (Valium): السعر 70
- Screening for Canabinoid (Hashish, Banjo): السعر 70
- Screening for Cocaine (COCAIN): السعر 70
- Screening for Herion: السعر 65
- Screening for Met - Amphetamine: السعر 70
- Screening for Morphine: السعر 65
- Screening for Opiates (MOP, Heroin): السعر 65
- Semen Analysis: السعر 40
- Semen C/S: السعر 110
- Serous Fluid C/S: السعر 110
- Serum Sodium (Na): السعر 22
- Serum Albumin: السعر 15
- Serum Aldosterone Hormone: السعر 370
- Serum Amylase: السعر 35
- serum bicarbonate (total CO2): السعر 95
- Serum Bilirubin profile: السعر 15
- Serum Calcium: السعر 15
- Serum Creatinine: السعر 15
- Serum GGT: السعر 15
- Serum ionized Calcium: السعر 30
- Serum Osmolality (estimated): السعر 65
- Serum Osmolality:: السعر 65
- Serum Phosphorus: السعر 20
- Serum Potassium(K): السعر 22
- Serum Protein Electrophoresis: السعر 215
- Serum Triglycerides: السعر 20
- Serum uric acid: السعر 15
- Sex Hormone Binding Globulin: السعر 350
- Sodium and Potassium (Serum): السعر 22
- Sodium in Urine: السعر 22
- Sputum C/S: السعر 120
- Stone Analysis: السعر 40
- Stool Analysis: السعر 20
- Stool C/S: السعر 110
- Syphilis ab: السعر 135
- T Uptake: السعر 92
- T.B Culture: السعر 185
- T3: السعر 32
- T3 (Free): السعر 32
- T3 And T4: السعر 32
- T4: السعر 32
- T4 (Free): السعر 32
- Tacrolimus (FK 506) (Prograf®): السعر 590
- TB-DNA by PCR: السعر 750
- TB Antibody: السعر 115
- TBG (Thyroxine binding globulin): السعر 400
- Testosterone (Free): السعر 75
- Testosterone (Total): السعر 50
- Thick Film Malaria: السعر 50
- Throat Swab C/S: السعر 110
- Thyroglobulin: السعر 210
- Thyroid Anti-Microsomal Ab.: السعر 120
- Thyroid Anti-Peroxidase Ab.: السعر 120
- Tissue transglutaminase IgG: السعر 250
- Tongue Swab C/S: السعر 110
- Total Bilirubin: السعر 15
- Total Body Protein: السعر 15
- Total Cholesterol: السعر 15
- Total Iron binding capacity (TIBC): السعر 40
- Total Lipids: السعر 60
- Total Metanephrine: السعر 2850
- Total Prostatic Specific Ag (PSA): السعر 80
- Total Protein: السعر 15
- Toxoplasma IgG Ab: السعر 85
- Toxoplasma IgM Ab: السعر 85
- Tramadol: السعر 80
- Transferrin: السعر 115
- Transferrin Saturation: السعر 80
- Treponema pallidum hemagglutination assay (IHA): السعر 50
- Triple Marker (2nd trimester) (15-20 w): السعر 400
- Triple Test: السعر 400
- Troponin - I: السعر 200
- Troponin I (High sensitive): السعر 250
- TSH: السعر 32
- TSH ULTRA SENSITIVE: السعر 32
- Urea Clearance: السعر 30
- Urethral Discharge C/S: السعر 110
- Uric Acid in Urine (24hrs): السعر 15
- Urinary VMA (24hrs): السعر 300
- Urine albumin / Creatinine ratio: السعر 60
- Urine Analysis: السعر 15
- Urine C/S: السعر 100
- Urine Osmolality (random): السعر 65
- Urine total protein/ Creatinine ratio: السعر 60
- Urine total protein/ Creatinine ratio (24hrs): السعر 60
- Vaginal Swab C/S: السعر 120
- Varicella (chickenpox) IgG: السعر 800
- VDRL (syphilis): السعر 50
- Vitamin B12: السعر 175
- Vitamin D (1. 25): السعر 265
- Vitamin D 3: السعر 150
- VLDL: السعر 20
- Vomitus C/S: السعر 110
- White Cell Count: السعر 22
- Widal Test: السعر 40
- Wound Swab C/S: السعر 110
- Ziehl Neelsen Stain: السعر 35
- Ziehl Neelsen Stain (Urine): السعر 35
- Ziehl Neelsen Stain 3 samples: السعر 105
- Zinc (Serum): السعر 85
- Zn in Urine (24 hrs): السعر 85
""",
    '🌊 برايس طارق بحري مع عروضها': r"""
- 1-25 OH-Vitamin D: السعر 265
- 17 OH progesterone: السعر 140
- A/G Ratio: السعر 27
- ABO Group: السعر 21
- Acetone in Urine: السعر 15
- ACTH (AM): السعر 110
- ACTH (PM): السعر 110
- ACTH Random: السعر 110
- Acti Fibro test: السعر 4000
- ADA: السعر 110
- ADA(Adenosine Deaminase in Ascitic Fluid): السعر 110
- ADA(Adenosine Deaminase in serum): السعر 110
- Albumin / Creatinine ratio (A/C %): السعر 57
- Aldolase: السعر 240
- Alk Phosphatase: السعر 14
- Alpha - 1 Anti trypsin: السعر 160
- Alpha Feto Protein in serum: السعر 80
- Alpha-glucosidase in semen: السعر 600
- AMA: السعر 250
- AMH (Anti Mullerian Hormone): السعر 230
- Ammonia: السعر 92
- Amylase in Urine: السعر 32
- Amyloid A: السعر 195
- ANA: السعر 100
- ANA by Immunofluorescence: السعر 240
- ANCA C (Cytoplasmic): السعر 195
- ANCA P (Perinuclear): السعر 195
- Androstenedione: السعر 300
- Angiotensin converting Enzyme: السعر 400
- AnSCL 70 Antibody: السعر 250
- Anti - (d.s) DNA: السعر 140
- Anti - CCP Antibody (Ab): السعر 185
- Anti - Gliadin Antibody (IgG): السعر 380
- Anti - Parietal Antibody: السعر 250
- Anti - Phospholipid Antibody (IgG): السعر 200
- Anti - Phospholipid Antibody (IgM): السعر 200
- Anti - Platelet Antibody (Direct): السعر 600
- Anti - Platelet Antibody (Indirect): السعر 600
- Anti - RNP Antibody: السعر 300
- Anti - ss - A/Ro Antibody: السعر 245
- Anti-ss-B/La Antibody: السعر 245
- Anti GAD (Anti-glutamic acid decarboxylase): السعر 1300
- ASOT LATEX: السعر 20
- Anti MuSK (muscle specific tyrosine kinase): السعر 5000
- Anti Smooth muscle Antibodies (ASMA): السعر 245
- Anti Streptolysin (ASOT): السعر 55
- Anti thyroid Antibody: السعر 120
- Anti Tissue transglutaminase Ab IgA: السعر 250
- Anti-B2 Glycoprotein(IgG): السعر 250
- Anti-B2 Glycoprotein (IgM): السعر 250
- Anticardiolipin IgG: السعر 168
- Anticardiolipin IgM: السعر 168
- Anti-Smith Antibody: السعر 250
- Antisperm Antibody (IgG): السعر 240
- Antisperm Antibody (IgM): السعر 240
- Anti-Sperm Antibody in Semen: السعر 240
- AntiSperm Antibody: السعر 240
- Antithrombin III: السعر 135
- Anti-thyroglobulin Antibody (ATG): السعر 120
- Anti-TSH receptor antibody: السعر 385
- ASCA Antibody (IgA): السعر 250
- ASCA Antibody (IgG): السعر 250
- Ascitic fluid C/S: السعر 110
- Ascitic Fluid Examination: السعر 100
- B2 Microglobuilin: السعر 130
- B2 Microglobulin in urine: السعر 140
- BCR-ABL Minor (p190) gene by Real Time PCR: السعر 2200
- Bence Jones protein in urine: السعر 40
- BHCG: السعر 65
- Blood C/S: السعر 185
- Blood film: السعر 42
- Blood Urea: السعر 14
- Body Fluid Culture: السعر 110
- Brucella IgG: السعر 300
- Brucella IgM: السعر 300
- Brucella Test: السعر 22
- BUN: السعر 14
- C- Peptide (Fasting): السعر 105
- C - Peptide (Postprandial): السعر 105
- C. Reactive Protein (CRP): السعر 43
- C3: السعر 62
- C4: السعر 62
- CA 125: السعر 100
- CA 15.3: السعر 100
- CA 19.9: السعر 100
- Calcitonin: السعر 900
- Calcium in Urine (24hrs): السعر 14
- Calcium/Creatinine ratio: السعر 25
- Calprotectin Stool Quantitative: السعر 256
- Carbamazepin (Tegretol): السعر 95
- Catecholamines in Urine (24 hrs): السعر 2850
- CEA: السعر 80
- Ceruloplasmin: السعر 80
- Cervical Swab C/S: السعر 110
- Chlamydia Antibody (IgG): السعر 285
- Chloride (Serum): السعر 26
- Chloride Urine (24 hrs): السعر 26
- Cholinestrase: السعر 500
- CMV Antibody (IgG): السعر 85
- CMV Antibody (IgM): السعر 85
- Complete Blood Count: السعر 50
- Complete Blood Count (CBC): السعر 50
- Comprehensive Metabolic Panel: السعر 1350
- Coombs' Test (Direct): السعر 38
- Coombs' Test (Indirect): السعر 42
- Copper: السعر 67
- Copper in Urine (24 hrs): السعر 67
- Cortisol 9 am: السعر 95
- Cortisol (Random): السعر 95
- Cortisol 9 pm: السعر 95
- Cortisol In Urine (24 hrs): السعر 100
- CPK: السعر 22
- CPK (MB): السعر 68
- Creatinine Clearance: السعر 26
- Creatinine in urine: السعر 14
- Cryoglobulin: السعر 80
- CSF C/S: السعر 110
- CSF examination: السعر 150
- CRP LATEX: السعر 20
- Culture Report: السعر 110
- Cyclosporine (Sandimmune): السعر 400
- D-Dimer: السعر 135
- Depakine (Valproic Acid): السعر 115
- DHEA: السعر 113
- DHEA-S: السعر 113
- Differential Leucocytic Count (WBCs): السعر 25
- Digoxin (Lanoxin) therapeutic level: السعر 350
- dihydrotestosterone (DHT): السعر 500
- Direct Bilirubin: السعر 14
- Drugs Screening: السعر 200
- E.S.R: السعر 35
- EBV Antibody (IgG): السعر 265
- EBV Antibody (IgM): السعر 265
- eGFR: السعر 57
- Endomysial IgA (IFA): السعر 500
- Endomysial IgG (IFA): السعر 500
- Entamoeba histolytica Ab: السعر 300
- Epanutin (Phenytoin, dilantin): السعر 150
- Estradiol (E2): السعر 50
- Estriol (E3): السعر 300
- Ethanol (Alcohol) level: السعر 200
- Extractable Nuclear Antigens (ENA) Panel: السعر 750
- F.D.P: السعر 220
- Factor - IX: السعر 700
- Factor - VIII: السعر 700
- Factor V: السعر 700
- Factor V Leiden Mutation By PCR: السعر 550
- Factor VII (F. 7): السعر 700
- Factor X (F. 10): السعر 700
- Factor XI (F. 11): السعر 1000
- Factor XII (F. 12): السعر 1000
- Fasciola Ab Titre: السعر 300
- Fasciola Ab: السعر 300
- Fasting Blood Glucose: السعر 14
- Ferritin: السعر 55
- Fibrin/ Fibrinogen Degradation Products (FDP): السعر 220
- Fibrinogen: السعر 80
- Filaria Ag: السعر 300
- Filaria antibodies: السعر 300
- Filaria Film: السعر 50
- Fluid Amylase: السعر 32
- Fluid C/S: السعر 110
- Fluid Lipase: السعر 32
- Folic Acid: السعر 220
- Food Allergy Panel: السعر 8000
- Free Metanephrine: السعر 2850
- Free Prostatic Specific Ag (PSA): السعر 85
- Fructosamine: السعر 63
- Fructose in semen: السعر 45
- FSH: السعر 40
- FTI: السعر 300
- Fungal stain: السعر 65
- G6PD (Quantitative): السعر 93
- Globulin: السعر 21
- Glucose in Urine: السعر 14
- Glycosylated Hb (HbAlc): السعر 33
- Gram Stain: السعر 35
- Growth Hormone: السعر 95
- H. Pylori IgA: السعر 120
- Haptoglobin: السعر 105
- HAV (Ig M): السعر 115
- HAV (IgG): السعر 115
- HAV Ab (total): السعر 115
- HBc IgG: السعر 105
- HBc IgM: السعر 105
- HBe Ab: السعر 105
- HBe Ag: السعر 105
- HBs Ab: السعر 75
- HBV-DNA by PCR (Quantitative): السعر 250
- HCV - RNA by PCR (Quantitative): السعر 250
- HCV Antibody (IgM): السعر 500
- HCV IgG (ELISA third generation): السعر 130
- HDL: السعر 27
- HDV (IgM): السعر 450
- HDV (Total): السعر 450
- Helicobacter Pylori Antigen in Stool qualitative: السعر 100
- Helicobacter Pylori Antigen in Stool Quantitative: السعر 100
- Hemoglobin: السعر 20
- Hemoglobin Electrophoresis: السعر 180
- Hepatitis Bs Antigen (HbsAg): السعر 95
- Hepatitis C Virus (Ab): السعر 130
- Herpes Simplex Virus Type I IgG: السعر 105
- Herpes Simplex Virus Type I IgM: السعر 105
- Herpes Simplex Virus Type II IgG: السعر 135
- Herpes Simplex Virus Type II IgM: السعر 135
- HEV antibodies IgM: السعر 300
- HEV antibody IgG: السعر 300
- HIV-2 RNA PCR (Quantitative): السعر 700
- HIV-RNA PCR (Quantitative): السعر 700
- HLA-B27: السعر 550
- HOMA IR (Insulin Resistance test): السعر 100
- Homocysteine: السعر 315
- H-Pylori Ab (IgG) Qualitative: السعر 95
- H-Pylori Ab (IgM): السعر 120
- H-Pylori antibodies: السعر 95
- hs-CRP: السعر 200
- Human Immunodeficiency Virus (HIV) Ab: السعر 100
- Hydatid Ab: السعر 250
- IgA (TTG): السعر 250
- IgE (Immunoglobulin E Total): السعر 90
- IgE Food Allergy Panel: السعر 1400
- IgE Inhalant allergy testing panel: السعر 1400
- IGF-1 (Insulin like growth factor-1): السعر 450
- IgG TOTAL: السعر 62
- Immuno fixation: السعر 2300
- Immunoglobulin A: السعر 62
- Immunoglobulin G: السعر 62
- Immunoglobulin M: السعر 62
- Immunoglobulin-G (IgG) in CSF: السعر 200
- Immunoglobulin-G4 (IgG4): السعر 1000
- Insulin (Fasting): السعر 95
- Insulin (Postprandial): السعر 95
- Insulin Ab: السعر 320
- Interleukin 6 (IL-6): السعر 220
- Iron: السعر 21
- Ketone bodies: السعر 15
- L- Lactate: السعر 80
- L.E. Cells: السعر 150
- Lactoferrin in stool: السعر 1200
- LDH: السعر 16
- LDL: السعر 33
- Left Conjunctival Swab C/S: السعر 110
- Left Nipple Discharge C/S: السعر 110
- Leptin: السعر 950
- Leucocytes: السعر 21
- Leutinizing Hormone (LH): السعر 40
- Lipase: السعر 32
- Lipid Profile: السعر 70
- Lithuim: السعر 260
- LKM-Ab: السعر 250
- Lupus Anticoagulant: السعر 125
- M2PK (Schebo test) (pyruvate kinase isoenzyme M2) Stool: السعر 1815
- Magnesium in Urine (24 hrs): السعر 21
- Malaria Ab (Anti-Plasmodium IgG): السعر 600
- Malaria Ag: السعر 200
- Malaria Film: السعر 50
- Microalbuminuria: السعر 57
- Monospot Test (Paul-Bunnell): السعر 55
- Nail Scarping KOH: السعر 65
- Nail Scraping C/S: السعر 160
- Nasal Discharge C/S: السعر 110
- new blood film: السعر 42
- Nicotine in Urine (tobacco - smoking): السعر 300
- Occult Blood in Stool: السعر 52
- Oral Glucose Tolerance Test: السعر 65
- Osmolality in Urine 24 hrs: السعر 63
- Osmotic Fragility: السعر 55
- Pancreatic amylase: السعر 32
- Parathyroid Hormone (PTH): السعر 130
- Partial Thromboplastin Time (PTT): السعر 38
- PCR for CMV: السعر 550
- PCR for Familial Mediterranean Fever Gene Mutation: السعر 1350
- PCR for JAK2 gene mutation: السعر 700
- PCR for Methylene tetrahydrofolateReductase Gene Mutation (MTHFR): السعر 550
- PCR for MRSA (GeneXpert): السعر 300
- PCR for Prothrombin gene mutation: السعر 550
- pH in Blood: السعر 16
- pH in Stool: السعر 20
- pH in Urine (spot sample): السعر 16
- Phenytoin (Epanutin): السعر 150
- Phosphorus in urine (24hrs): السعر 20
- Platelets Count: السعر 21
- Pleural Fluid C/S: السعر 110
- Pleural Fluid Examination: السعر 100
- Postprandial Blood Glucose: السعر 14
- potassium in urine: السعر 21
- Pregnancy test: السعر 65
- Pro-BNP(Pro B-type natriuretic peptide): السعر 510
- Procalcitonin PCT-Q: السعر 500
- Progesterone: السعر 50
- Prolactin: السعر 40
- Prostatic Discharge C/S: السعر 110
- Protein "C": السعر 340
- Protein "S": السعر 340
- Protein immunofixation (serum): السعر 2300
- Protein immunofixation in urine: السعر 2300
- Protein in Urine (24hrs): السعر 45
- Prothrombine Time (PT): السعر 33
- PSA Profile: السعر 80
- Pus C/S: السعر 110
- Pus Discharge C/S: السعر 110
- Pyruvate: السعر 250
- QuantiFERON-TB Gold: السعر 1700
- Random Blood Glucose: السعر 14
- Reducing Substance in Stool: السعر 50
- Reducing substances in urine: السعر 50
- Renin level: السعر 450
- Reticulocyte Count: السعر 450
- Rh antibody titre: السعر 60
- Rh Grouping: السعر 21
- Rheumatoid Factor (RF): السعر 47
- Right Conjunctival Swab C/S: السعر 110
- Right Ear Discharge C/S: السعر 110
- Right Nipple Discharge C/S: السعر 110
- Rose Waaler Test: السعر 47
- RF LATEX: السعر 20
- Routine fungal culture: السعر 160
- RPR: السعر 60
- Rubella IgG Ab: السعر 85
- Rubella IgM Ab: السعر 85
- S. Magnesium (Mg): السعر 21
- S.G.O.T (AST): السعر 14
- S.G.P.T (ALT): السعر 14
- Schistosoma (Bilharzia) Ab (IHA): السعر 155
- Schistosoma (Bilharzia) Ab. (IgG): السعر 155
- Schistosoma (Bilharzia) Ab. (IgM): السعر 155
- Schistosoma (Bilharzia) Ag: السعر 200
- Screening for (THC): السعر 70
- Screening for Amphetamine: السعر 70
- Screening for Barbiturates (BAR): السعر 70
- Screening for Benzodizepines (Valium): السعر 70
- Screening for Canabinoid (Hashish, Banjo): السعر 70
- Screening for Cocaine (COCAIN): السعر 70
- Screening for Herion: السعر 65
- Screening for Met - Amphetamine: السعر 70
- Screening for Morphine: السعر 65
- Screening for Opiates (MOP, Heroin): السعر 65
- Semen Analysis: السعر 40
- Semen C/S: السعر 110
- Serous Fluid C/S: السعر 110
- Serum Sodium (Na): السعر 21
- Serum Albumin: السعر 14
- Serum Aldosterone Hormone: السعر 370
- Serum Amylase: السعر 32
- serum bicarbonate (total CO2): السعر 95
- Serum Bilirubin profile: السعر 14
- Serum Calcium: السعر 14
- Serum Creatinine: السعر 14
- Serum GGT: السعر 14
- Serum ionized Calcium: السعر 26
- Serum Osmolality (estimated): السعر 63
- Serum Osmolality:: السعر 63
- Serum Phosphorus: السعر 16
- Serum Potassium(K): السعر 21
- Serum Protein Electrophoresis: السعر 215
- Serum Triglycerides: السعر 16
- Serum uric acid: السعر 14
- Sex Hormone Binding Globulin: السعر 350
- Sodium and Potassium (Serum): السعر 21
- Sodium in Urine: السعر 21
- Sputum C/S: السعر 110
- Stone Analysis: السعر 40
- Stool Analysis: السعر 17
- Stool C/S: السعر 110
- Syphilis ab: السعر 135
- T Uptake: السعر 92
- T.B Culture: السعر 185
- T3: السعر 32
- T3 (Free): السعر 32
- T3 And T4: السعر 32
- T4: السعر 32
- T4 (Free): السعر 32
- Tacrolimus (FK 506) (Prograf®): السعر 590
- TB-DNA by PCR: السعر 750
- TB Antibody: السعر 115
- TBG (Thyroxine binding globulin): السعر 400
- Testosterone (Free): السعر 72
- Testosterone (Total): السعر 50
- Thick Film Malaria: السعر 50
- Throat Swab C/S: السعر 110
- Thyroglobulin: السعر 210
- Thyroid Anti-Microsomal Ab.: السعر 120
- Thyroid Anti-Peroxidase Ab.: السعر 120
- Tissue transglutaminase IgG: السعر 250
- Tongue Swab C/S: السعر 110
- Total Bilirubin: السعر 14
- Total Body Protein: السعر 14
- Total Cholesterol: السعر 14
- Total Iron binding capacity (TIBC): السعر 40
- Total Lipids: السعر 60
- Total Metanephrine: السعر 2850
- Total Prostatic Specific Ag (PSA): السعر 80
- Total Protein: السعر 14
- Toxoplasma IgG Ab: السعر 85
- Toxoplasma IgM Ab: السعر 85
- Tramadol: السعر 80
- Transferrin: السعر 115
- Transferrin Saturation: السعر 80
- Treponema pallidum hemagglutination assay (IHA): السعر 50
- Triple Marker (2nd trimester) (15-20 w): السعر 400
- Triple Test: السعر 400
- Troponin - I: السعر 200
- Troponin I (High sensitive): السعر 250
- TSH: السعر 32
- TSH ULTRA SENSITIVE: السعر 32
- Urea Clearance: السعر 26
- Urethral Discharge C/S: السعر 110
- Uric Acid in Urine (24hrs): السعر 14
- Urinary VMA (24hrs): السعر 300
- Urine albumin / Creatinine ratio: السعر 57
- Urine Analysis: السعر 16
- Urine C/S: السعر 100
- Urine Osmolality (random): السعر 63
- Urine total protein/ Creatinine ratio: السعر 60
- Urine total protein/ Creatinine ratio (24hrs): السعر 60
- Vaginal Swab C/S: السعر 110
- Varicella (chickenpox) IgG: السعر 800
- VDRL (syphilis): السعر 50
- Vitamin B12: السعر 175
- Vitamin D (1. 25): السعر 265
- Vitamin D 3: السعر 150
- VLDL: السعر 16
- Vomitus C/S: السعر 110
- White Cell Count: السعر 21
- Widal Test: السعر 40
- Wound Swab C/S: السعر 110
- Ziehl Neelsen Stain: السعر 35
- Ziehl Neelsen Stain (Urine): السعر 35
- Ziehl Neelsen Stain 3 samples: السعر 105
- Zinc (Serum): السعر 82
- Zn in Urine (24 hrs): السعر 82
""",
    '✨ برايس كويك الجديد مع العروض': r"""
- 1-25 OH-Vitamin D: السعر 140، العينة Serum (500 μL)، المدة 1 Day
- 17 Ketosteroids in Urine (24 hrs): السعر 480، العينة 24h Urine in acidified container، المدة 5 Days
- 17 OH progesterone: السعر 200، العينة Serum، المدة 4 Days
- A/G Ratio: السعر 30، العينة Serum، المدة 2 Days
- AB- Thrombo Type Plus: السعر 2000، العينة Frozen Serum، المدة 2 Days
- ABO Group: السعر 10، العينة Edita whole blood، المدة 2 Hours
- Absolute CD 4 + Cells Count: السعر 750، العينة EDTA Blood، المدة 5 Days
- Acetone in Urine: السعر 10، العينة Urine، المدة 6 Hours
- Acid Phosphatase (Prostatic): السعر 180، العينة Serum، المدة 2 Days
- Acid Phosphatase (Total): السعر 80، العينة Serum، المدة 2 Days
- ACTH (AM): السعر 90، العينة Frozen EDTA plasma in plastic tube، المدة 1 Days
- ACTH (PM): السعر 90، العينة Frozen EDTA plasma in plastic tube، المدة 1 Days
- ACTH Random: السعر 90، العينة Frozen EDTA plasma in plastic tube، المدة 1 Days
- Acti Fibro test: السعر 1700، العينة Serum (Required:، المدة 6 Days
- ADA: السعر 160، العينة Pericardial Fluid، المدة 1 Day
- ADA(Adenosine Deaminase in Ascitic Fluid): السعر 160، العينة Fluid، المدة 2 Days
- ADA(Adenosine Deaminase in serum): السعر 160، العينة Serum، المدة 2 Days
- Adenovirus (ADV) DNA: السعر 200، العينة Serum، المدة 2 Days
- ADH (Anti-diuretic hormone): السعر 840، العينة Frozen EDTA plasma، المدة 10 Days
- Adrenalin: السعر 2000، العينة EDTA plasma، المدة 8 Days
- Albumin / Creatinine ratio (A/C %): السعر 45، العينة Urine، المدة 6 Hours
- Albumin in Urine (Random): السعر 30، العينة Urine، المدة 6 Hours
- Aldolase: السعر 310، العينة Serum، المدة 2 Days
- Aldosterone / Renin ratio: السعر 1200، العينة Frozen morning EDTA plasma + Serum، المدة 6 Days
- Alk Phosphatase: السعر 15، العينة Serum، المدة 6 Hours
- Alpha - 1 Anti trypsin: السعر 170، العينة Serum، المدة 2 Days
- Alpha 1 globulin: السعر Contact Lab، العينة Serum، المدة 2 Days
- Alpha Feto Protein in serum: السعر 60، العينة Serum، المدة 6 Hours
- Alpha-glucosidase in semen: السعر 580، العينة في انبوبة وزرمان Seminal Fluid، المدة 3 Days
- AMA: السعر 150، العينة Serum، المدة 4 Days
- AMH (Anti Mullerian Hormone): السعر 200، العينة Serum، المدة 6 Hours
- Ammonia: السعر 75، العينة EDTA frozen plasma، المدة 6 Hours
- Amylase in Urine: السعر 20، العينة Urine، المدة 6 Hours
- Amyloid A: السعر 210، العينة Serum، المدة 3 Days
- ANA: السعر 80، العينة Serum، المدة 1 Days
- ANA by Immunofluorescence: السعر 100، العينة Serum، المدة 3 Days
- Anal Swab for oxyruis ova: السعر Contact Lab، العينة Swab، المدة 1 Day
- ANCA C (Cytoplasmic): السعر 130، العينة Serum، المدة 1 Day
- ANCA P (Perinuclear): السعر 130، العينة Serum، المدة 1 Day
- Androstenedione: السعر 350، العينة Serum، المدة 4 Days
- Angiotensin converting Enzyme: السعر 480، العينة Serum، المدة 2 Days
- AnSCL 70 Antibody: السعر 360، العينة Serum، المدة 4 Days
- Anti - (d.s) DNA: السعر 80، العينة Serum، المدة 1 Days
- Anti - CCP Antibody (Ab): السعر 135، العينة Serum، المدة 1 Days
- Anti - Gliadin Antibody (IgG): السعر 320، العينة Serum، المدة 4 Days
- Anti - Histones Antibody: السعر 750، العينة Serum، المدة 4 Days
- Anti - Parietal Antibody: السعر 400، العينة Serum، المدة 4 Days
- Anti - Phospholipid Antibody (IgG): السعر 170، العينة Serum، المدة 1 Days
- Anti - Phospholipid Antibody (IgM): السعر 170، العينة Serum، المدة 1 Days
- Anti - Platelet Antibody (Direct): السعر 600، العينة 4 (EDTA tube - 2mL)، المدة 5 Days
- Anti - Platelet Antibody (Indirect): السعر 600، العينة Serum، المدة 4 Days
- Anti - RNP Antibody: السعر 350، العينة Serum، المدة 4 Days
- Anti - ss - A/Ro Antibody: السعر 210، العينة Serum، المدة 3 Days
- Anti-ss-B/La Antibody: السعر 210، العينة Serum، المدة 3 Days
- Anti GAD (Anti-glutamic acid decarboxylase): السعر 700، العينة Serum، المدة 4 Days
- Anti ICA (Anti-Islet cell Ab): السعر 320، العينة Serum، المدة 4 Days
- Anti Intrinsic factor Ab: السعر 430، العينة Serum، المدة 4 Days
- ASOT LATEX: السعر 15، العينة Serum، المدة 1 Days
- Anti MOG (IFA) (anti-Myelin oligodendrocyte Glycoprotein): السعر 1500، العينة Serum، المدة 5 Days
- Anti MuSK (muscle specific tyrosine kinase): السعر 5000، العينة Serum، المدة 5 Days
- Anti Smooth muscle Antibodies (ASMA): السعر 230، العينة Serum، المدة 1 Days
- Anti Streptolysin (ASOT): السعر 40، العينة Serum، المدة 6 Hours
- Anti thyroid Antibody: السعر 160، العينة Serum، المدة 1 Days
- Anti Tissue transglutaminase Ab IgA: السعر 225، العينة Serum، المدة 4 Days
- Anti-B2 Glycoprotein(IgG): السعر 225، العينة Serum، المدة 4 Days
- Anti-B2 Glycoprotein (IgM): السعر 225، العينة Serum، المدة 4 Days
- Anticardiolipin IgG: السعر 110، العينة Serum، المدة 1 Days
- Anticardiolipin IgM: السعر 110، العينة Serum، المدة 1 Days
- Antidiuretic Hormone (ADH): السعر 750، العينة frozen EDTA plasma، المدة 10 Days
- Anti-Smith Antibody: السعر 300، العينة Serum، المدة 4 Days
- Antisperm Antibody (IgG): السعر Contact Lab، العينة Serum، المدة 2 Days
- Antisperm Antibody (IgM): السعر Contact Lab، العينة Serum، المدة 2 Days
- Anti-Sperm Antibody in Semen: السعر Contact Lab، العينة Seminal fluid، المدة 2 Days
- AntiSperm Antibody: السعر 450، العينة Serum، المدة 4 Days
- Antithrombin III: السعر 160، العينة Citrated plasma، المدة 2 Days
- Anti-thyroglobulin Antibody (ATG): السعر 80، العينة Serum، المدة 8 Hours
- Anti-TSH receptor antibody: السعر 385، العينة Serum، المدة 2 Days
- ASCA Antibody (IgA): السعر 260، العينة Serum، المدة 4 Days
- ASCA Antibody (IgG): السعر 260، العينة Serum، المدة 4 Days
- Ascitic fluid C/S: السعر 80، العينة Fluid، المدة 4 Days
- Ascitic Fluid Examination: السعر 75، العينة Fluid، المدة 6 Hours
- B2 Microglobuilin: السعر 110، العينة Serum، المدة 2 Days
- B2 Microglobulin in urine: السعر 140، العينة Urine، المدة 2 Days
- BCR-ABL Minor (p190) gene by Real Time PCR: السعر 3000، العينة EDTA Blood، المدة 6 Days
- Bence Jones protein in urine: السعر 20، العينة Urine، المدة 6 Hours
- BHCG: السعر 60، العينة Serum، المدة 6 Hours
- Bleeding Time: السعر 10، العينة Edita whole blood، المدة 6 Hours
- Blood C/S: السعر 110، العينة blood media، المدة 10 Days
- Blood film: السعر 30، العينة Edita whole blood، المدة 8 Hours
- Blood Gas Profile (ABG): السعر 100، العينة Heparinized Whole blood، المدة 1 Hours
- Blood Urea: السعر 10، العينة Serum، المدة 6 Hours
- Body Fluid Culture: السعر 40، العينة Fluid، المدة 5 Days
- BONE MARROW EX.: السعر 7500، العينة BONE MARROW، المدة 7 Days
- Breast Discharge Culture: السعر 40، العينة Sterile Swab، المدة 3 Days
- Brucella IgG: السعر 340، العينة Serum، المدة 1 Days
- Brucella IgM: السعر 340، العينة Serum، المدة 1 Days
- Brucella Test: السعر 30، العينة Serum، المدة 6 Hours
- BUN: السعر 10، العينة Serum، المدة 6 Hours
- C- Peptide (Fasting): السعر 70، العينة Serum، المدة 6 Hours
- C - Peptide (Postprandial): السعر 75، العينة Serum، المدة 6 Hours
- C. Reactive Protein (CRP): السعر 40، العينة Serum، المدة 6 Hours
- Cl esterase inhibitor: السعر 520، العينة Edita plasma، المدة 3 Days
- C3: السعر 50، العينة Serum، المدة 1 Days
- C4: السعر 50، العينة Serum، المدة 1 Days
- CA 125: السعر 75، العينة Serum، المدة 6 Hours
- CA 15.3: السعر 75، العينة Serum، المدة 6 Hours
- CA 19.9: السعر 75، العينة Serum، المدة 6 Hours
- Calcitonin: السعر 680، العينة Frozen Serum (500 µl)، المدة 5 Days
- Calcium / Phosphorus Ratio: السعر 50، العينة Urine، المدة 6 Hours
- Calcium in Urine (24hrs): السعر 12، العينة Urine، المدة 6 Hours
- Calcium/Creatinine ratio: السعر 30، العينة Urine، المدة 6 Hours
- Calcium/Phosphorus (Ca - Ph): السعر 25، العينة Urine، المدة 6 Hours
- Calprotectin Stool Quantitative: السعر 220، العينة Stool، المدة 1 Days
- Carbamazepin (Tegretol): السعر 120، العينة Serum، المدة 1 Days
- Catecholamine (Adrenalin Serum): السعر Contact Lab، العينة Edita plasma، المدة 8 Days
- Catecholamine (Noradrenalin Serum): السعر Contact Lab، العينة Edita plasma، المدة 8 Days
- Catecholamines in Urine (24 hrs): السعر 900، العينة Urine، المدة 7 Days
- CD 10: السعر 700، العينة Paraffin blocks، المدة 10 Days
- CD 19: السعر 850، العينة Paraffin blocks، المدة 10 Days
- CD la: السعر 700، العينة Paraffin blocks، المدة 10 Days
- CD4/CD 8: السعر 1050، العينة Paraffin blocks، المدة 5 Days
- CD 5: السعر 700، العينة Paraffin blocks، المدة 10 Days
- CD 7: السعر 700، العينة Paraffin blocks، المدة 10 Days
- CEA: السعر 55، العينة Serum، المدة 6 Hours
- Ceruloplasmin: السعر 120، العينة Serum، المدة 2 Days
- Cervical Swab C/S: السعر 80، العينة Strile swab، المدة 3 Days
- Chlamydia Antibody: السعر 480، العينة Serum، المدة 3 Days
- Chlamydia Antibody (IgG): السعر 480، العينة Serum، المدة 3 Days
- Chloride (Serum): السعر 20، العينة Serum، المدة 6 Hours
- Chloride Urine (24 hrs): السعر 20، العينة Serum، المدة 6 Hours
- Chol/HDL: السعر 28، العينة Serum، المدة 4 Hours
- Cholinestrase: السعر Contact Lab، العينة Serum، المدة 5 Days
- Chromogranin A in serum: السعر 800، العينة Serum، المدة 6 Days
- Clotting Time: السعر 10، العينة Edita whole blood، المدة 6 Hours
- CMV Antibody (IgG): السعر 55، العينة Serum، المدة 1 Days
- CMV Antibody (IgM): السعر 55، العينة Serum، المدة 1 Days
- Complete Blood Count: السعر 19، العينة EDTA Blood، المدة 4 Hours
- Complete Blood Count (CBC): السعر 19، العينة Edita whole blood، المدة 2 Hours
- Comprehensive Metabolic Panel: السعر 300، العينة Serum، المدة 1 Day
- Coombs' Test (Direct): السعر 28، العينة EDTA blood (1mL)، المدة 1 Hours
- Coombs' Test (Indirect): السعر 33، العينة Serum (500 μL)، المدة 1 Days
- Copper: السعر 60، العينة Serum، المدة 1 Days
- Copper in Urine (24 hrs): السعر 60، العينة Urine 24 hrs، المدة 6 Hours
- Cortisol 9 am: السعر 75، العينة Serum، المدة 6 Hours
- Cortisol (Random): السعر 75، العينة Serum، المدة 6 Hours
- Cortisol 9 pm: السعر 75، العينة Serum، المدة 6 Hours
- Cortisol In Urine (24 hrs): السعر 75، العينة Urine 24 hrs، المدة 6 Hours
- Covid 19 Antigen: السعر Contact Lab، العينة Serum، المدة 1 Day
- COVID IgG Ab: السعر 250، العينة Serum، المدة 6 Hours
- COVID IgM Ab: السعر 250، العينة Serum، المدة 6 Hours
- COVID-19 test by RT-PCR: السعر 700، العينة Nasal swab، المدة 1 Days
- COVID-19 test by RT-PCR (Qualitative detection of SARS-COV-2): السعر Contact Lab، العينة Swab in special media، المدة 1 Day
- CPK: السعر 18، العينة Serum، المدة 6 Hours
- CPK (MB): السعر 45، العينة Serum، المدة 6 Hours
- Creatinine Clearance: السعر 18، العينة Serum and 24 hrs Urine، المدة 6 Hours
- Creatinine in urine: السعر 10، العينة 24 hrs. Urine، المدة 6 Hours
- Cryoglobulin: السعر 60، العينة Serum، المدة 6 Days
- CSF C/S: السعر 80، العينة CSF Fluid، المدة 3 Days
- CSF examination: السعر 75، العينة CSF Fluid، المدة 8 Hours
- CRP LATEX: السعر 15، العينة Serum، المدة 1 Days
- Culture Report: السعر 40، العينة Sample، المدة 3 Days
- Cyclosporine (Sandimmune): السعر 450، العينة Edita blood، المدة 3 Days
- Cystatin C: السعر 150، العينة Serum، المدة 1 Days
- CYTOLOGICAL ASSESSMENTS: السعر 500، العينة Fluid، المدة 10 Days
- CYTOLOGY: السعر 480، العينة Sample، المدة 10 Days
- D-Dimer: السعر 75، العينة Citrated plasma، المدة 6 Hours
- Depakine (Valproic Acid): السعر 90، العينة Serum، المدة 1 Days
- DHEA: السعر 100، العينة Serum، المدة 1 Days
- DHEA-S: السعر 100، العينة Serum، المدة 1 Days
- Differential Leucocytic Count (WBCs): السعر 15، العينة Edita whole blood، المدة 2 Hours
- Digoxin (Lanoxin) therapeutic level: السعر 125، العينة Serum، المدة 1 Days
- dihydrotestosterone (DHT): السعر 380، العينة Serum، المدة 4 Days
- Direct Bilirubin: السعر 10، العينة Serum، المدة 4 Hours
- DNA Fragmentation from sperm: السعر 1300، العينة Semen، المدة 2 Days
- Double Marker (1st trimester) (11-13 w): السعر 500، العينة Serum، المدة 4 Days
- Drugs Screening: السعر 160، العينة Urine، المدة 6 Hours
- Dysmorphic RBCs in urine: السعر 70، العينة Urine، المدة 1 Day
- E.S.R: السعر 15، العينة Edita whole blood، المدة 6 Hours
- EBV Antibody (IgG): السعر 110، العينة Serum، المدة 4 Days
- EBV Antibody (IgM): السعر 110، العينة Serum، المدة 3 Days
- EBV By PCR Quantitative: السعر 850، العينة EDTA plasma، المدة 4 Days
- eGFR: السعر 50، العينة Serum، المدة 6 Hours
- Endomysial IgA (IFA): السعر 380، العينة Serum، المدة 4 Days
- Endomysial IgG (IFA): السعر 285، العينة Serum، المدة 4 Days
- Entamoeba histolytica Ab: السعر 210، العينة Serum، المدة 2 Days
- Epanutin (Phenytoin, dilantin): السعر 120، العينة Serum، المدة 1 Days
- Estradiol (E2): السعر 40، العينة Serum، المدة 6 Hours
- Estriol (E3): السعر 320، العينة Serum، المدة 4 Days
- Estrogen Receptors (ER+): السعر 750، العينة Serum، المدة 6 Days
- Ethanol (Alcohol) level: السعر 80، العينة Urine، المدة 1 Days
- Extractable Nuclear Antigens (ENA) Panel: السعر 900، العينة Serum، المدة 5 Days
- F.D.P: السعر 150، العينة Citrated plasma، المدة 2 Days
- Factor - IX: السعر 240، العينة Citrated plasma، المدة 3 Days
- Factor - VIII: السعر 1000، العينة Citrated plasma، المدة 4 Days
- Factor II: السعر 1200، العينة Citrated plasma، المدة 4 Days
- Factor V: السعر 1000، العينة Citrated plasma، المدة 4 Days
- Factor V Leiden Mutation By PCR: السعر 550، العينة Edita whole blood، المدة 7 Days
- Factor VII (F. 7): السعر 1200، العينة Citrated plasma، المدة 4 Days
- Factor X (F. 10): السعر 1200، العينة Citrated plasma، المدة 4 Days
- Factor XI (F. 11): السعر 1200، العينة Citrated plasma، المدة 4 Days
- Factor XII (F. 12): السعر 1200، العينة Citrated plasma، المدة 4 Days
- Fasciola Ab Titre: السعر 180، العينة Serum، المدة 2 Days
- Fasciola Ab: السعر 240، العينة Serum، المدة 1 Day
- Fasting Blood Glucose: السعر 10، العينة Fasting Serum on floride tube، المدة 6 Hours
- Ferritin: السعر 45، العينة Serum، المدة 6 Hours
- Fibrin/ Fibrinogen Degradation Products (FDP): السعر 100، العينة Citrated plasma، المدة 2 Days
- Fibrinogen: السعر 70، العينة Citrated plasma، المدة 2 Days
- Fibrosis-4 (FIB-4): السعر 180، العينة EDTA blood + Serum، المدة 2 Days
- Filaria Ag: السعر 450، العينة Serum، المدة 1 Day
- Filaria antibodies: السعر 210، العينة Serum، المدة 2 Days
- Filaria Film: السعر 50، العينة EDTA Blood، المدة 1 Days
- Fluid Amylase: السعر 22، العينة Fluid، المدة 6 Hours
- Fluid C/S: السعر 80، العينة Fluid، المدة 3 Days
- Fluid Lipase: السعر 35، العينة Fluid، المدة 6 Hours
- Folic Acid: السعر 280، العينة Frozen Serum (500 μL)، المدة 2 Days
- Food Allergy Panel: السعر 950، العينة Serum، المدة 15 Days
- Free Metanephrine: السعر 1300، العينة Edita plasma، المدة 8 Days
- Free Prostatic Specific Ag (PSA): السعر 55، العينة Serum، المدة 6 Hours
- Free PSA/Total PSA ratio: السعر 105، العينة Serum، المدة 4 Hours
- Fructosamine: السعر 65، العينة Serum، المدة 1 Days
- Fructose in semen: السعر 65، العينة Seminal Fluid (Fresh or Frozen sample)، المدة 2 Days
- FSH: السعر 35، العينة Serum، المدة 6 Hours
- FSH/LH ratio: السعر 70، العينة Serum، المدة 4 Hours
- FTI: السعر 90، العينة Serum، المدة 1 Days
- Fungal stain: السعر 130، العينة Any body Fluid، المدة 2 Days
- G6PD (Quantitative): السعر 70، العينة Edita whole blood، المدة 2 Hours
- Gastrin: السعر 450، العينة Fasting, frozen Serum، المدة 4 Days
- Gingival Swab C/S: السعر 80، العينة Strile swab، المدة 3 Days
- Globulin: السعر 75، العينة Serum، المدة 2 Hours
- Glucose in Urine: السعر 10، العينة Urine، المدة 6 Hours
- Glycosylated Hb (HbAlc): السعر 30، العينة Edita whole blood، المدة 8 Hours
- Gram Stain: السعر 20، العينة sample، المدة 1 Days
- Growth Hormone: السعر 90، العينة Serum، المدة 2 Days
- Gum Discharge C/S: السعر 80، العينة Strile swab، المدة 3 Days
- H. Pylori IgA: السعر 80، العينة Serum، المدة 2 Days
- Haptoglobin: السعر 260، العينة Serum، المدة 2 Days
- HAV (Ig M): السعر 60، العينة Serum، المدة 1 Days
- HAV (IgG): السعر 60، العينة Serum، المدة 1 Day
- HAV Ab (total): السعر 60، العينة Serum، المدة 1 Days
- HBc IgG: السعر 50، العينة Serum، المدة 1 Days
- HBc IgM: السعر 50، العينة Serum، المدة 1 Days
- HBe Ab: السعر 50، العينة Serum، المدة 1 Days
- HBe Ag: السعر 50، العينة Serum، المدة 1 Days
- HBs Ab: السعر 50، العينة Serum، المدة 1 Days
- HBV-DNA by PCR (Quantitative): السعر 230، العينة Serum Edita، المدة 1 Days
- HCV - RNA by PCR (Quantitative): السعر 200، العينة Serum Edita، المدة 1 Days
- HCV Antibody (IgM): السعر 350، العينة Serum، المدة 1 Days
- HCV IgG (ELISA third generation): السعر Contact Lab، العينة Serum، المدة 1 Day
- HDL: السعر 20، العينة Serum Fasting، المدة 6 Hours
- HDV (IgM): السعر 375، العينة Serum، المدة 8 Days
- HDV (Total): السعر 375، العينة Serum، المدة 8 Days
- Helicobacter Pylori Antigen in Stool qualitative: السعر 60، العينة Stool، المدة 6 Hours
- Helicobacter Pylori Antigen in Stool Quantitative: السعر 75، العينة Stool، المدة 6 Hours
- Hemoglobin: السعر 15، العينة Edita whole blood، المدة 2 Hours
- Hemoglobin Electrophoresis: السعر 380، العينة EDTA Blood، المدة 3 Days
- Hepatitis Bs Antigen (HbsAg): السعر 35، العينة Serum، المدة 6 Hours
- Hepatitis C Virus (Ab): السعر 30، العينة Serum، المدة 6 Hours
- HER-2: السعر 740، العينة Paraffin blocks، المدة 10 Days
- Herpes simplex panel By PCR: السعر 2300، العينة CSF، المدة 2 Days
- Herpes Simplex Virus Type I IgG: السعر 55، العينة Serum، المدة 1 Days
- Herpes Simplex Virus Type I IgM: السعر 55، العينة Serum، المدة 1 Days
- Herpes Simplex Virus Type II IgG: السعر 55، العينة Serum، المدة 1 Days
- Herpes Simplex Virus Type II IgM: السعر 55، العينة Serum، المدة 1 Days
- HEV antibodies IgM: السعر 210، العينة Serum، المدة 4 Days
- HEV antibody IgG: السعر 800، العينة Serum، المدة 3 Days
- Histamine: السعر 3000، العينة Frozen plasma (EDTA or، المدة 4 Days
- HIV-2 RNA PCR (Quantitative): السعر 1100، العينة Serum "Must be in a gel tube"، المدة 4 Days
- HIV-RNA PCR (Quantitative): السعر 1300، العينة Serum "Must be in a gel tube"، المدة 5 Days
- HLA-B27: السعر 500، العينة Edita whole blood، المدة 6 Days
- HOMA IR (Insulin Resistance test): السعر 80، العينة F. Serum، المدة 6 Hours
- Homocysteine: السعر 380، العينة Serum، المدة 2 Days
- HPV Human Papillomavirus PCR: السعر 750، العينة Vaginal swab in a transport medium، المدة 7 Days
- HPV IgG (Human papilloma virus): السعر 1200، العينة Serum، المدة 4 Days
- H-Pylori Ab (IgG) Qualitative: السعر 65، العينة Serum، المدة 6 Hours
- H-Pylori Ab (IgM): السعر 50، العينة Serum، المدة 6 Hours
- H-Pylori antibodies: السعر 50، العينة Serum، المدة 6 Hours
- hs-CRP: السعر 15، العينة Serum، المدة 1 Day
- Human Immunodeficiency Virus (HIV) Ab: السعر 50، العينة Serum، المدة 6 Hours
- Hydatid Ab: السعر 390، العينة Serum، المدة 3 Days
- IgA (TTG): السعر 280، العينة Serum، المدة 2 Days
- IgE (Immunoglobulin E Total): السعر 60، العينة Serum، المدة 1 Days
- IgE Food Allergy Panel: السعر 950، العينة Serum، المدة 15 Days
- IgE Inhalant allergy testing panel: السعر 850، العينة Serum، المدة 4 Days
- IGF-1 (Insulin like growth factor-1): السعر 300، العينة Serum، المدة 4 Days
- IgG TOTAL: السعر 60، العينة Serum، المدة 2 Days
- Immuno fixation: السعر 2200، العينة 2 (Serum tube - 2mL) For each unit، المدة 6 Days
- Immunoglobulin A: السعر 55، العينة Serum، المدة 2 Days
- Immunoglobulin G: السعر 55، العينة Serum، المدة 2 Days
- Immunoglobulin M: السعر 55، العينة Serum، المدة 2 Days
- Immunoglobulin-G (IgG) in CSF: السعر 200، العينة CSF، المدة 2 Days
- Immunoglobulin-G4 (IgG4): السعر 900، العينة Serum، المدة 3 Days
- Immunophenotyping by Flow Cytometry: السعر 2200، العينة Bone marrow aspirate، المدة 5 Days
- Inhibin A: السعر 2500، العينة Frozen Serum، المدة 4 Days
- Inhibin B: السعر 2500، العينة Frozen Serum، المدة 5 Days
- Insulin (Fasting): السعر 65، العينة Serum، المدة 6 Hours
- Insulin (Postprandial): السعر 65، العينة Serum، المدة 6 Hours
- Insulin Ab: السعر 305، العينة Serum، المدة 4 Days
- Insulin Glucose Ratio: السعر 70، العينة EDTA plasma، المدة 6 Hours
- Interleukin 6 (IL-6): السعر 250، العينة Serum، المدة 6 Hours
- Interleukin-28 (IL-B 28): السعر 1650، العينة Edita whole blood، المدة 5 Days
- Iron: السعر 25، العينة Serum، المدة 6 Hours
- Iron Profile: السعر 100، العينة Serum، المدة 1 Day
- k2 + (strooks, voodo): السعر 45، العينة Urine، المدة 6 Hours
- Ketone bodies: السعر 450، العينة EDTA Blood، المدة 2 Days
- Kidney Profile: السعر 24، العينة Serum، المدة 4 Hours
- Kleihauer-Betke test: السعر 550، العينة Edita whole blood، المدة 3 Days
- Knee aspirate C/S: السعر 60، العينة Ascitic، المدة 5 Days
- L- Lactate: السعر 60، العينة Serum on fluride tube، المدة 6 Hours
- L.E. Cells: السعر 90، العينة Serum، المدة 1 Days
- Lactoferrin in stool: السعر 500، العينة Stool، المدة 2 Days
- LDH: السعر 15، العينة Serum، المدة 6 Hours
- LDL: السعر 32، العينة Serum، المدة 6 Hours
- LDL/HDL: السعر Contact Lab، العينة Serum، المدة 4 Hours
- Left Conjunctival Swab C/S: السعر 80، العينة Sterile swab، المدة 3 Days
- Left Ear Discharge C/S: السعر 80، العينة Sterile swab، المدة 3 Days
- Left Nipple Discharge C/S: السعر 80، العينة Sterile swab، المدة 3 Days
- Leishmania: السعر 1200، العينة Serum، المدة 2 Days
- Leptin: السعر 600، العينة Serum، المدة 4 Days
- Leucocytes: السعر 12، العينة Edita whole blood، المدة 2 Hours
- Leutinizing Hormone (LH): السعر 35، العينة Serum، المدة 6 Hours
- Lipase: السعر 38، العينة Serum، المدة 6 Hours
- Lipid Profile: السعر 55، العينة Serum، المدة 4 Hours
- Lipoprotein (a): السعر 300، العينة Serum، المدة 2 Days
- Lithuim: السعر 60، العينة Serum، المدة 1 Days
- Liver Function: السعر 40، العينة Serum، المدة 4 Hours
- liver profile basic: السعر 20، العينة Serum، المدة 6 Hours
- LKM-Ab: السعر 250، العينة Serum، المدة 4 Days
- Lupus Anticoagulant: السعر 85، العينة Citrated plasma، المدة 1 Days
- Lymphocyte subsets Cell Count CD3, CD4, CD8,CD19,(CD16/CD56): السعر 2300، العينة Edita whole blood، المدة 5 Days
- M2PK (Schebo test) (pyruvate kinase isoenzyme M2) Stool: السعر 1650، العينة Stool، المدة 4 Days
- Magnesium in Urine (24 hrs): السعر 15، العينة Urine، المدة 6 Hours
- Malaria Ab (Anti-Plasmodium IgG): السعر 520، العينة Serum، المدة 3 Days
- Malaria Ag: السعر 360، العينة Edita whole blood، المدة 1 Days
- Malaria Film: السعر 20، العينة Edita whole blood، المدة 1 Days
- methamphetamine (crystal ice, shaboo): السعر 45، العينة Urine، المدة 6 Hours
- Methotrexate: السعر 1850، العينة Serum، المدة 2 Days
- Microalbuminuria: السعر 45، العينة Urine، المدة 6 Hours
- Milk + Gluten Panel: السعر 1200، العينة Serum، المدة 4 Days
- Monospot Test (Paul-Bunnell): السعر 50، العينة Serum، المدة 1 Days
- Multiplex PCR for Pathogens Causing Diarrhea: السعر 7500، العينة Stool، المدة 3 Days
- Myoglobin: السعر 210، العينة Serum، المدة 2 Days
- Myoglobin in urine: السعر 210، العينة Urine، المدة 2 Days
- Nail Scarping KOH: السعر 130، العينة Skin, scalp or nail، المدة 10 Days
- Nail Scraping C/S: السعر 130، العينة Skin, scalp or nail، المدة 3 Days
- Nasal Discharge C/S: السعر 80، العينة Sterile swab، المدة 3 Days
- Neuron Specific Enolase (NSE): السعر 1200، العينة Paraffin blocks or non hemolyzed، المدة 10 Days
- new blood film: السعر 30، العينة Edita whole blood، المدة 8 Hours
- Nicotine in Blood (Quantitative) (tobacco - smoking): السعر 250، العينة Serum، المدة 2 Days
- Nicotine in Urine (tobacco - smoking): السعر 65، العينة Urine، المدة 6 Hours
- NK cells (CD16/CD56): السعر 900، العينة 4 (EDTA tube - 2mL)، المدة 5 Days
- Occult Blood in Stool: السعر 40، العينة Stool، المدة 6 Hours
- Oligoclonal bands in CSF: السعر 2500، العينة CSF، المدة 5 Days
- Oral Glucose Tolerance Test: السعر 40، العينة Serum on fluride tube، المدة 6 Hours
- Osmolality in Urine 24 hrs: السعر 70، العينة Urine، المدة 2 Days
- Osmotic Fragility: السعر 30، العينة Fresh heparinized blood (3 mL)، المدة 1 Days
- Osteocalcin in Serum (N-MID): السعر 200، العينة Serum، المدة 2 Days
- OX19 Ab (Weil-Felix test): السعر 130، العينة Serum، المدة 2 Days
- Pancreatic amylase: السعر 140، العينة Serum، المدة 1 Day
- Pancreatic elastase: السعر 1600، العينة Serum، المدة 1 Day
- Pap smear: السعر 450، العينة Smear، المدة 10 Days
- Parathyroid Hormone (PTH): السعر 95، العينة 2.0 ml. frozen EDTA plasma or Serum، المدة 8 Hours
- Parental testing: السعر 11000، العينة 5 EDTA Blood، المدة 60 Days
- Partial Thromboplastin Time (PTT): السعر 25، العينة Citrated plasma، المدة 6 Hours
- Pathology Report: السعر 500، العينة Sample، المدة 10 Days
- PATHOLOGY REPORT (Organ): السعر 1200، العينة Sample، المدة 10 Days
- PATHOLOGY REPORT (Very Large): السعر 850، العينة Sample، المدة 10 Days
- PATHOLOGY REPORT (Large): السعر 1000، العينة Sample، المدة 10 Days
- PATHOLOGY REPORT (medium): السعر 600، العينة Sample، المدة 10 Days
- PATHOLOGY REPORT (small): السعر 500، العينة Sample، المدة 10 Days
- PCR for Brucella: السعر 1050، العينة EDTA blood (1 mL)، المدة 4 Days
- PCR for CMV: السعر 850، العينة EDTA plasma، المدة 5 Days
- PCR for Familial Mediterranean Fever Gene Mutation: السعر 900، العينة EDTA Blood، المدة 3 Days
- PCR for H1N1 influenza virus (Swine flu): السعر 900، العينة Nasopharyngeal swab، المدة 3 Days
- PCR for HCV genotyping: السعر 1000، العينة EDTA Blood (5 mL)، المدة 5 Days
- PCR for HEV: السعر 1400، العينة EDTA Plasma، المدة 3 Days
- PCR for HLA-B5: السعر 1000، العينة EDTA Blood، المدة 6 Days
- PCR for HLA-B51: السعر 1000، العينة EDTA Blood، المدة 6 Days
- PCR for HLA-B57: السعر 1000، العينة EDTA Blood، المدة 6 Days
- PCR for HLA-Typing - Class I (A): السعر 1900، العينة Edita whole blood، المدة 6 Days
- PCR for HLA-Typing - Class I (B) (Reverse hybridization): السعر 2000، العينة EDTA Blood، المدة 6 Days
- PCR for HLA-Typing - Class II (DRB1): السعر 1500، العينة Edita whole blood، المدة 6 Days
- PCR for JAK2 gene mutation: السعر 650، العينة Edita whole blood، المدة 6 Days
- PCR for Methylene tetrahydrofolateReductase Gene Mutation (MTHFR): السعر 650، العينة Edita whole blood، المدة 7 Days
- PCR for MRSA (GeneXpert): السعر 1000، العينة Swab، المدة 3 Days
- PCR for Prothrombin gene mutation: السعر 1000، العينة EDTA Blood، المدة 5 Days
- Peroxidase test(leuco screen): السعر 60، العينة في انبوبة وزرمان Seminal Fluid، المدة 2 Days
- pH in Blood: السعر 100، العينة Heparinized Whole blood، المدة 1 Hours
- pH in Stool: السعر 10، العينة Stool، المدة 6 Hours
- pH in Urine (spot sample): السعر 10، العينة Urine، المدة 6 Hours
- Phenobarbital: السعر 800، العينة Serum، المدة 3 Days
- Phenytoin (Epanutin): السعر 110، العينة Serum، المدة 2 Days
- Phosphorus in urine (24hrs): السعر 12، العينة Urine، المدة 6 Hours
- Plasminogen, Plasma: السعر 400، العينة Edita whole blood، المدة 3 Days
- Platelet Function: السعر 850، العينة Fresh Edita whole blood، المدة 3 Days
- Platelets Count: السعر 15، العينة Edita whole blood، المدة 6 Hours
- Pleural Fluid C/S: السعر 80، العينة Fluid، المدة 5 Days
- Pleural Fluid Examination: السعر 75، العينة Fluid، المدة 6 Hours
- PNH (CD55/CD59): السعر 950، العينة Edita whole blood، المدة 5 Days
- Postprandial Blood Glucose: السعر 8، العينة Floride tube، المدة 6 Hours
- potassium in urine: السعر Contact Lab، العينة Urine، المدة 4 Hours
- Pregnancy test: السعر 15، العينة Serum or Urine، المدة 6 Hours
- Pro-BNP(Pro B-type natriuretic peptide): السعر 650، العينة Serum، المدة 2 Days
- Procalcitonin PCT-Q: السعر 230، العينة Serum، المدة 6 Hours
- Progesterone: السعر 40، العينة Serum، المدة 6 Hours
- Prolactin: السعر 35، العينة Serum، المدة 6 Hours
- Prostatic Discharge C/S: السعر 80، العينة Discharge، المدة 3 Days
- Protein "C": السعر 280، العينة Citrated plasma، المدة 4 Days
- Protein "S": السعر 280، العينة Citrated plasma، المدة 4 Days
- Protein immunofixation (serum): السعر 2000، العينة Serum، المدة 6 Days
- Protein immunofixation in urine: السعر 1500، العينة Urine، المدة 6 Days
- Protein in Urine (24hrs): السعر 15، العينة 24 hrs. Urine، المدة 6 Hours
- Prothrombine Time (PT): السعر 15، العينة 1.8ml blood on 0.2 citrate and sent immediately frozen، المدة 2 Hours
- PSA Profile: السعر 105، العينة Serum، المدة 6 Hours
- Pus C/S: السعر 80، العينة Sterile swab، المدة 3 Days
- Pus Discharge C/S: السعر 80، العينة Sterile swab، المدة 3 Days
- Pyruvate: السعر 350، العينة Edita whole blood، المدة 2 Days
- QuantiFERON-TB Gold: السعر 1100، العينة 4 tubes of lithium heparine، المدة 3 Days
- Random Blood Glucose: السعر 10، العينة Fasting Serum on floride tue، المدة 6 Hours
- Reducing Substance in Stool: السعر 35، العينة Stool، المدة 8 Hours
- Reducing substances in urine: السعر 35، العينة Urine، المدة 1 Days
- Renin level: السعر 620، العينة Frozen morning EDTA plasma، المدة 6 Days
- Reticulocyte Count: السعر 15، العينة Edita whole blood، المدة 8 Hours
- Rh antibody titre: السعر 120، العينة Serum، المدة 1 Days
- Rh Grouping: السعر 10، العينة Edita whole blood، المدة 6 Hours
- Rheumatoid Factor (RF): السعر 40، العينة Serum، المدة 6 Hours
- Right Conjunctival Swab C/S: السعر 80، العينة Strile swab، المدة 3 Days
- Right Ear Discharge C/S: السعر 80، العينة Strile swab، المدة 3 Days
- Right Nipple Discharge C/S: السعر 80، العينة Strile swab، المدة 3 Days
- Rose Waaler Test: السعر 30، العينة Serum، المدة 2 Days
- RF LATEX: السعر 20، العينة Serum، المدة 1 Days
- Routine fungal culture: السعر 375، العينة Sample، المدة 10 Days
- RPR: السعر 40، العينة Serum، المدة 1 Days
- Rubella IgG Ab: السعر 55، العينة Serum، المدة 1 Days
- Rubella IgM Ab: السعر 55، العينة Serum، المدة 1 Days
- S. Magnesium (Mg): السعر 15، العينة Serum، المدة 6 Hours
- S.G.O.T (AST): السعر 10، العينة Serum، المدة 6 Hours
- S.G.P.T (ALT): السعر 10، العينة Serum، المدة 6 Hours
- SAAG Ratio: السعر 40، العينة Peritoneal (Ascitic) Fluid + Serum، المدة 1 Day
- Schistosoma (Bilharzia) Ab (IHA): السعر 140، العينة Serum، المدة 1 Days
- Schistosoma (Bilharzia) Ab. (IgG): السعر 390، العينة Serum، المدة 3 Days
- Schistosoma (Bilharzia) Ab. (IgM): السعر 390، العينة Serum، المدة 3 Days
- Schistosoma (Bilharzia) Ag: السعر 200، العينة Urine، المدة 2 Days
- Screening for (THC): السعر 45، العينة Urine، المدة 6 Hours
- Screening for Amphetamine: السعر 45، العينة Urine، المدة 6 Hours
- Screening for Barbiturates (BAR): السعر 45، العينة Urine، المدة 6 Hours
- Screening for Benzodizepines (Valium): السعر 45، العينة Urine، المدة 6 Hours
- Screening for Canabinoid (Hashish, Banjo): السعر 45، العينة Urine، المدة 6 Hours
- Screening for Cocaine (COCAIN): السعر 45، العينة Urine، المدة 6 Hours
- Screening for Herion: السعر 45، العينة Urine، المدة 6 Hours
- Screening for Met - Amphetamine: السعر 45، العينة Urine، المدة 6 Hours
- Screening for Morphine: السعر 45، العينة Urine، المدة 6 Hours
- Screening for Opiates (MOP, Heroin): السعر 45، العينة Urine، المدة 6 Hours
- Semen Analysis: السعر 30، العينة semen، المدة 6 Hours
- Semen C/S: السعر 80، العينة semen، المدة 3 Days
- Serous Fluid C/S: السعر 80، العينة Fluid، المدة 3 Days
- Serum Sodium (Na): السعر 15، العينة Serum، المدة 2 Hours
- Serum Albumin: السعر 15، العينة Serum، المدة 6 Hours
- Serum Aldosterone Hormone: السعر 450، العينة Serum، المدة 5 Days
- Serum Amylase: السعر 25، العينة Serum، المدة 6 Hours
- serum bicarbonate (total CO2): السعر 120، العينة Serum، المدة 6 Hours
- Serum Bilirubin profile: السعر 20، العينة Serum، المدة 6 Hours
- Serum Calcium: السعر 15، العينة Serum، المدة 6 Hours
- Serum Creatinine: السعر 15، العينة Serum، المدة 6 Hours
- Serum GGT: السعر 12، العينة Serum، المدة 6 Hours
- Serum ionized Calcium: السعر 20، العينة Serum، المدة 4 Hours
- Serum Osmolality (estimated): السعر 65، العينة Serum، المدة 2 Days
- Serum Osmolality:: السعر 70، العينة Serum، المدة 2 Days
- Serum Phosphorus: السعر 15، العينة Serum، المدة 6 Hours
- Serum Potassium(K): السعر 15، العينة Serum، المدة 2 Hours
- Serum Protein Electrophoresis: السعر 320، العينة Serum، المدة 3 Days
- Serum Triglycerides: السعر 10، العينة Serum Fasting، المدة 6 Hours
- Serum uric acid: السعر 10، العينة Serum، المدة 6 Hours
- Sex Hormone Binding Globulin: السعر 115، العينة Serum، المدة 2 Days
- Sirolimus (Rapamycin): السعر 520، العينة EDTA blood، المدة 5 Days
- Sodium and Potassium (Serum): السعر 24، العينة Serum، المدة 2 Hours
- Sodium in Urine: السعر 15، العينة Urine، المدة 6 Hours
- Specific IgE for Candida albicans: السعر 220، العينة Serum، المدة 4 Days
- Sputum C/S: السعر 80، العينة Sputume، المدة 3 Days
- Stone Analysis: السعر 40، العينة Urinary stone، المدة 2 Days
- Stool Analysis: السعر 15، العينة Stool، المدة 6 Hours
- Stool C/S: السعر 80، العينة Stool، المدة 3 Days
- Synthetic Marijuana (Strox): السعر 80، العينة Urine، المدة 6 Hours
- Synthetic Marijuana (Voodoo): السعر 45، العينة Urine، المدة 6 Hours
- Syphilis ab: السعر 50، العينة Serum، المدة 1 Days
- T Uptake: السعر 110، العينة Serum، المدة 1 Days
- T.B Culture: السعر 600، العينة Sterile body Fluids, aspirate and tissue ...etc، المدة 45 Days
- T3: السعر 22، العينة Serum، المدة 6 Hours
- T3 (Free): السعر 25، العينة Serum، المدة 6 Hours
- T3 And T4: السعر 44، العينة Serum، المدة 6 Hours
- T4: السعر 22، العينة Serum، المدة 6 Hours
- T4 (Free): السعر 25، العينة Serum، المدة 6 Hours
- Tacrolimus (FK 506) (Prograf®): السعر 750، العينة Edita whole blood، المدة 3 Days
- TB-DNA by PCR: السعر 850، العينة Any biological Fluid، المدة 5 Days
- TB Antibody: السعر 150، العينة Serum، المدة 2 Days
- TBG (Thyroxine binding globulin): السعر 280، العينة Serum، المدة 2 Days
- Testosterone (Free): السعر 50، العينة Serum، المدة 6 Hours
- Testosterone (Total): السعر 45، العينة Serum، المدة 6 Hours
- Theophylline: السعر 380، العينة Serum، المدة 2 Days
- Thick Film Malaria: السعر 20، العينة Edita whole blood، المدة 1 Days
- Throat Swab C/S: السعر 60، العينة Sterile swab، المدة 3 Days
- Thyroglobulin: السعر 135، العينة Serum، المدة 6 Hours
- Thyroid Anti-Microsomal Ab.: السعر 80، العينة Serum، المدة 6 Hours
- Thyroid Anti-Peroxidase Ab.: السعر 80، العينة Serum، المدة 6 Hours
- Tissue transglutaminase IgG: السعر 225، العينة Serum، المدة 4 Days
- Tongue Swab C/S: السعر 80، العينة Sterile swab، المدة 3 Days
- Total Bilirubin: السعر 10، العينة Serum، المدة 4 Hours
- Total Body Protein: السعر 15، العينة Serum، المدة 6 Hours
- Total Cholesterol: السعر 10، العينة Serum Fasting، المدة 6 Hours
- Total Iron binding capacity (TIBC): السعر 30، العينة Serum، المدة 6 Hours
- Total Kappa light chain: السعر 200، العينة Serum، المدة 2 Days
- Total Lambda light chain: السعر 180، العينة Serum، المدة 2 Days
- Total Lipids: السعر 55، العينة Serum، المدة 1 Days
- Total Metanephrine: السعر 400، العينة 24h Urine، المدة 8 Days
- Total Prostatic Specific Ag (PSA): السعر 50، العينة Serum، المدة 6 Hours
- Total Protein: السعر 10، العينة Serum، المدة 6 Hours
- Toxoplasma IgG Ab: السعر 55، العينة Serum، المدة 1 Days
- Toxoplasma IgM Ab: السعر 55، العينة Serum، المدة 1 Days
- Tramadol: السعر 45، العينة Urine، المدة 1 Days
- Transferrin: السعر 85، العينة Serum، المدة 6 Hours
- Transferrin Saturation: السعر 80، العينة Serum، المدة 6 Hours
- Treponema pallidum hemagglutination assay (IHA): السعر 90، العينة Serum، المدة 2 Days
- Trichinella spiralis Ab: السعر 1300، العينة Serum، المدة 6 Days
- Trig/HDL: السعر Contact Lab، العينة Serum، المدة 4 Hours
- Triple Marker (2nd trimester) (15-20 w): السعر 800، العينة Serum، المدة 4 Days
- Triple Test: السعر 600، العينة Serum، المدة 4 Days
- Troponin - I: السعر 45، العينة Serum، المدة 6 Hours
- Troponin - T: السعر 200، العينة Serum، المدة 1 Day
- Troponin I (High sensitive): السعر 170، العينة Serum، المدة 2 Days
- Trypsin: السعر 160، العينة Serum، المدة 2 Days
- TSH: السعر 25، العينة Serum، المدة 6 Hours
- TSH ULTRA SENSITIVE: السعر 28، العينة Serum، المدة 1 Day
- Urea Clearance: السعر 20، العينة Serum (300 µL) + 24h Urine، المدة 6 Hours
- Urethral Discharge C/S: السعر 80، العينة Discharge، المدة 3 Days
- Uric Acid in Urine (24hrs): السعر 10، العينة Urine 24 hrs، المدة 6 Hours
- Urinary VMA (24hrs): السعر 400، العينة 24h Urine، المدة 3 Days
- Urine albumin / Creatinine ratio: السعر 50، العينة Urine، المدة 6 Hours
- Urine Analysis: السعر 15، العينة Urine، المدة 6 Hours
- Urine C/S: السعر 80، العينة Urine، المدة 3 Days
- Urine Examination After Massage: السعر 10، العينة Urine، المدة 6 Hours
- Urine Examination Before Massage: السعر 10، العينة Urine، المدة 6 Hours
- Urine Osmolality (random): السعر 80، العينة Random Urine، المدة 1 Days
- Urine total protein/ Creatinine ratio: السعر Contact Lab، العينة Serum + Urine، المدة 4 Hours
- Urine total protein/ Creatinine ratio (24hrs): السعر 30، العينة 24 hrs. Urine، المدة 6 Hours
- Vaginal Swab C/S: السعر 80، العينة Sterile swab، المدة 3 Days
- Varicella (chickenpox) IgG: السعر 300، العينة Serum، المدة 2 Days
- VDRL (syphilis): السعر 40، العينة Serum، المدة 1 Days
- Vitamin B12: السعر 150، العينة Serum، المدة 1 Day
- Vitamin D (1. 25): السعر 140، العينة Serum، المدة 6 Hours
- Vitamin D 3: السعر 140، العينة Serum، المدة 6 Hours
- VLDL: السعر 50، العينة Serum، المدة 1 Days
- Vomitus C/S: السعر 80، العينة sample، المدة 3 Days
- White Cell Count: السعر 12، العينة Edita blood، المدة 4 Hours
- Widal Test: السعر 20، العينة Serum، المدة 6 Hours
- Wound Swab C/S: السعر 80، العينة Sterile swab، المدة 3 Days
- Ziehl Neelsen Stain: السعر 35، العينة Sputum، المدة 1 Days
- Ziehl Neelsen Stain (Urine): السعر 35، العينة Urine، المدة 1 Days
- Ziehl Neelsen Stain 3 samples: السعر 105، العينة Sputum، المدة 3 Days
- Zinc (Serum): السعر 70، العينة Serum، المدة 6 Hours
- Zn in Urine (24 hrs): السعر 70، العينة Serum، المدة 6 Hours
""",
}

# ============================================================
# 3) نصوص العروض (للذكاء الاصطناعي مباشرة)
# ============================================================
PRICE_OFFER_TEXTS = {
    "💰 برايس كويك القديم": r"",
    "🏜️ برايس طارق للصعيد": r"",
    "🌊 برايس طارق بحري مع عروضها": r"""
- TSH: السعر 30
- FT4: السعر 30
- FT3: السعر 30
- TT4: السعر 30
- TT3: السعر 30
- HBA1C: السعر 33
- B.HCG: السعر 60
- FSH: السعر 40
- LH: السعر 40
- PRL: السعر 40
- H.Pylori Ag: السعر 90
- Lupus: السعر 120
- Anti CCP: السعر 165
- Amyloid A: السعر 180
- Ferritin: السعر 49
- Lipid Profile: السعر 65
- ANA Eliza: السعر 100
- ΑΜΗ: السعر 230
- ViD3: السعر 140
- Testestrone Total: السعر 45
- Testestrone Free: السعر 80
- Cortisol: السعر 88
""",
    "✨ برايس كويك الجديد مع العروض": r"""
- Vit D3: السعر 130
- Vit B 12: السعر 140
- ΑΜΗ: السعر 180
- Anti CCP: السعر 125
- FSH: السعر 30
- LH: السعر 30
- PRL: السعر 30
- HBA1C: السعر 28
- Amyloid A: السعر 185
- Ferritin: السعر 40
- Ft3+Ft4+TSH: السعر 69
- T3+T4+TSH: السعر 67
- CBC 5 Part: السعر 17
- Anti-Cardiolipin igm & igg: السعر 90
- Calprotactin (Quantitative): السعر 200
- H.Pylori Ag: السعر 70
- Homa IR: السعر 70
- Lipids Profile: السعر 42
- Iron: السعر 18
- Stool C\S: السعر 60
- Urine C\S: السعر 60
- ANA: السعر 90
- Free PSA: السعر 55
- Total PSA: السعر 50
- Lupus: السعر 90
- FMF by PCR: السعر 900
- Cmv&Toxo&Rublla&Hsv: السعر 50
- Tb-Gold: السعر 1000
- HBV Pcr(Qualitative): السعر 200
- HCV Pcr(Qualitative): السعر 190
- AFP: السعر 50
- B-hcg: السعر 40
""",
}

# ============================================================
# 4) دوال التجميع الأساسية (لجلب العينة والمدة)
# ============================================================
PRICE_LINE_RE = re.compile(r"^-\s*(.*?):\s*السعر\s*(.*?)(?:،\s*العينة\s*(.*?))?(?:،\s*المدة\s*(.*?))?$")

def normalize_name(name):
    name = str(name).strip().lower()
    name = name.replace("–", "-").replace("—", "-")
    name = re.sub(r"\s+", " ", name)
    return name

def parse_price_list(text):
    records = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or not line.startswith("-"): continue
        m = PRICE_LINE_RE.match(line)
        if not m: continue
        name, price, sample, turnaround = m.groups()
        records[normalize_name(name)] = {
            "name": name.strip(), "price": price.strip(),
            "sample": sample.strip() if sample else None,
            "turnaround": turnaround.strip() if turnaround else None,
        }
    return records

PARSED_PRICE_LISTS = {name: parse_price_list(text) for name, text in PRICE_LIST_TEXTS.items()}
BASE_RECORDS = PARSED_PRICE_LISTS["💰 برايس كويك القديم"]
PRICE_OVERRIDES = {name: {k: v["price"] for k, v in recs.items()} for name, recs in PARSED_PRICE_LISTS.items()}
PRICE_DETAILS = PARSED_PRICE_LISTS

def build_catalog_for_price_list(price_list_name):
    overrides = PRICE_OVERRIDES.get(price_list_name, {})
    details = PRICE_DETAILS.get(price_list_name, {})
    output = ["======================"]
    for record in BASE_RECORDS.values():
        key = normalize_name(record["name"])
        list_record = details.get(key, {})
        price = overrides.get(key, record["price"])
        sample = list_record.get("sample") or record.get("sample") or "غير محدد"
        turnaround = list_record.get("turnaround") or record.get("turnaround") or "غير محدد"
        output.append(f"- {record['name']}: السعر {price}، العينة {sample}، المدة {turnaround}")
    output.append("======================")
    return "\n".join(output)

def build_all_price_catalogs():
    parts = []
    for price_list_name in PRICE_LIST_TEXTS:
        parts.append(f"\n### {price_list_name}\n")
        parts.append("الأسعار الأساسية:")
        parts.append(build_catalog_for_price_list(price_list_name))
        offers = PRICE_OFFER_TEXTS.get(price_list_name, "").strip()
        if offers:
            parts.append("\nالعروض الخاصة:")
            parts.append(offers)
    return "\n".join(parts)

# ============================================================
# 5) شخصية البوت 
# ============================================================
BASE_PERSONALITY = """
أنت مساعد ذكي وسريع ومحترف لفريق خدمة العملاء في معامل
"كويك ميدسينا - Quick Medicina".

أسلوبك:
- اتكلم باللهجة المصرية بشكل طبيعي، خفيف الدم وودود.
- لو الطلب واضح، ادخل في الإجابة على طول.
- ممنوع تعطي تشخيص أو نصيحة طبية.
- لو التحليل غير موجود، اكتب بوضوح: "⚠️ التحليل ده مش موجود عندنا في القائمة الحالية، ياريت الرجوع للإدارة الفنية."
- لو السعر مكتوب "Contact Lab"، لا تحولها لرقم من عندك.
- احسب الإجمالي بدقة ولو فيه أكثر من تحليل.
- عند عرض النتائج استخدم جدول أو قائمة منظمة.
"""

# ============================================================
# 6) أزرار وحفظ الحالة
# ============================================================
selected_price = {}
pending_request = {}

def price_keyboard():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    buttons = [telebot.types.InlineKeyboardButton(text=name, callback_data=f"p:{i}") for i, name in enumerate(PRICE_OVERRIDES.keys())]
    for i in range(0, len(buttons), 2):
        markup.row(*buttons[i:i+2])
    markup.row(telebot.types.InlineKeyboardButton("📊 مقارنة الأسعار", callback_data="compare"))
    return markup

def action_keyboard():
    return price_keyboard()

def ask_for_price(chat_id, intro="تمام يا باشا 👌 تحب أحسبه على أنهي قائمة أسعار؟"):
    bot.send_message(chat_id, intro, reply_markup=price_keyboard())

def get_price_name_by_index(index):
    names = list(PRICE_OVERRIDES.keys())
    return names[index] if 0 <= index < len(names) else None

# ============================================================
# 7) Gemini مع Retry 
# ============================================================
def generate_with_retry(contents, config, retries=4):
    for attempt in range(retries):
        try:
            return client.models.generate_content(
                model="gemini-3.8-flash",
                contents=contents,
                config=config
            )
        except Exception as e:
            error_text = str(e)
            if "503" in error_text or "UNAVAILABLE" in error_text:
                wait_time = 2 ** attempt
                print(f"Gemini unavailable - retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            raise
    raise Exception("Gemini API remained unavailable after retries.")

# ============================================================
# 8) تنفيذ الطلب (الجزء المحدث الخاص بالعروض)
# ============================================================
def run_request(chat_id, price_list_name, compare=False):
    request = pending_request.get(chat_id)
    if not request:
        ask_for_price(chat_id, "أنا جاهز 😄 بس ابعتلي اسم التحليل أو صورة الريكويست الأول.")
        return

    if compare:
        catalogs = build_all_price_catalogs()
        price_instruction = f"قارن بين القوائم التالية، استخدم سعر العرض (لو موجود) واعرض السعر الأساسي:\n{catalogs}"
    else:
        catalog = build_catalog_for_price_list(price_list_name)
        offers = PRICE_OFFER_TEXTS.get(price_list_name, "").strip()
        price_instruction = f"""
قائمة الأسعار المختارة: {price_list_name}

📌 القائمة الشاملة الأساسية:
{catalog}

🎁 قائمة العروض الحالية:
{offers if offers else "لا توجد عروض لهذه القائمة."}
"""

    system_instruction = f"""
{BASE_PERSONALITY}

{price_instruction}

خطوات التسعير المطلوبة منك كذكاء اصطناعي:
1. ابحث عن التحليل في "🎁 قائمة العروض الحالية" أولاً! (استخدم ذكاءك في مطابقة الاختصارات مثل Vit D3 مع Vitamin D 3).
2. إذا وجدت التحليل في العروض (حتى لو كان باكدج مثل Ft3+Ft4+TSH)، استخدم سعر العرض كالسعر النهائي المعتمد.
3. استخرج بيانات (العينة) و (المدة) للتحليل من "📌 القائمة الشاملة الأساسية".
4. في ردك على الموظف، إذا كان هناك عرض، اعرض السعر الأساسي ثم السعر بعد العرض بوضوح، واحسب الإجمالي بناءً على سعر العرض فقط.
5. لا تخترع عروضاً من خيالك، التزم فقط بالنص الموجود.
"""
    config = types.GenerateContentConfig(system_instruction=system_instruction)

    try:
        bot.send_chat_action(chat_id, "typing")
        response = generate_with_retry(contents=request["contents"], config=config)
        bot.send_message(chat_id, response.text or "مفيش نتيجة رجعت 😅", reply_markup=action_keyboard())
        if not compare: selected_price[chat_id] = price_list_name

    except Exception as e:
        bot.send_message(chat_id, "حصلت مشكلة بسيطة وأنا بحسب الأسعار 😅 جرّب تاني بعد لحظات.")
        print("Error:", repr(e))

# ============================================================
# 9) و 10) و 11) باقي إعدادات وأزرار البوت
# ============================================================
@bot.message_handler(commands=["start", "prices", "help"])
def commands(message):
    if message.text.startswith("/start"):
        bot.send_message(message.chat.id, "👋 أهلاً بيك!\nأنا مساعد كول سنتر كويك ميدسينا 🤖\nابعت اسم تحليل أو صورة ريكويست.", reply_markup=price_keyboard())
    else:
        ask_for_price(message.chat.id, "اختار قائمة الأسعار اللي عايز تشتغل عليها:")

@bot.message_handler(content_types=["text", "photo"])
def handle_message(message):
    try:
        chat_id = message.chat.id
        if message.content_type == "text" and message.text.startswith("/"): return

        if message.content_type == "text":
            pending_request[chat_id] = {"contents": message.text, "kind": "text"}
        elif message.content_type == "photo":
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            image = Image.open(io.BytesIO(downloaded_file))
            prompt = "استخرج أسماء التحاليل، وابحث عنها في القوائم لتعطيني (الاسم، السعر، العينة، المدة) مع تطبيق العروض."
            if message.caption: prompt += f"\nملاحظة: {message.caption}"
            pending_request[chat_id] = {"contents": [prompt, image], "kind": "photo"}

        current_price = selected_price.get(chat_id)
        if current_price: run_request(chat_id, current_price)
        else: ask_for_price(chat_id, "وصلت يا معلم 😎\nبس قولي الأول نحسب على أنهي برايس ليست؟ 👇")
    except Exception as e:
        bot.reply_to(message, "حصل خطأ مؤقت 😅 حاول مرة تانية.")
        print("Error:", repr(e))

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        chat_id = call.message.chat.id
        if call.data == "compare":
            bot.answer_callback_query(call.id, "حاضر 😎 بجهز المقارنة...")
            run_request(chat_id, None, compare=True)
            return

        if call.data.startswith("p:"):
            index = int(call.data.split(":")[1])
            price_name = get_price_name_by_index(index)
            bot.answer_callback_query(call.id, f"تمام، اخترت {price_name}")
            
            if not pending_request.get(chat_id):
                selected_price[chat_id] = price_name
                bot.send_message(chat_id, f"✅ تمام، ابعت الريكويست أو اسم التحليل عشان أسعره على ({price_name})")
                return
            run_request(chat_id, price_name)
    except Exception as e:
        print("Callback error:", repr(e))

print("Quick Medicina Call Center Bot is running...")
bot.infinity_polling(skip_pending=True)