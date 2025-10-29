# Auto-generated cleaning script for DigitalServiceUsage_Rwanda.csv
# Run this script in the same folder as the CSV. It reproduces the conservative cleaning steps.
import pandas as pd, numpy as np
df = pd.read_csv("DigitalServiceUsage_Rwanda - DigitalServiceUsage_Rwanda.csv", low_memory=False)
clean = df.copy()
# Strip strings
for col in clean.select_dtypes(include=['object']).columns:
    clean[col] = clean[col].astype(str).str.strip()
    clean.loc[clean[col].isin(['', 'nan', 'None', 'NoneType']), col] = np.nan
# Attempt date parsing
for col in clean.columns:
    if clean[col].dtype == object:
        try:
            parsed = pd.to_datetime(clean[col], errors='coerce', infer_datetime_format=True)
            if parsed.notna().sum() >= max(3, int(0.25*len(clean))):
                clean[col] = parsed
        except Exception:
            pass
# Coerce numeric-like columns
for col in clean.columns:
    if clean[col].dtype == object:
        clean[col] = pd.to_numeric(clean[col].str.replace(',',''), errors='coerce')
# Drop rows with >50% missing values
clean = clean.dropna(thresh=int(0.5*clean.shape[1]))
# Remove duplicates
clean = clean.drop_duplicates(keep='first')
# Impute numeric with median and categoricals with 'Unknown'
num_cols = clean.select_dtypes(include=[np.number]).columns
medians = clean[num_cols].median()
for col in num_cols:
    clean[col] = clean[col].fillna(medians[col])
for col in clean.columns:
    if col not in num_cols and not pd.api.types.is_datetime64_any_dtype(clean[col]):
        clean[col] = clean[col].fillna('Unknown')
clean.to_csv("DigitalServiceUsage_Rwanda_cleaned.csv", index=False)
print("Saved cleaned file: DigitalServiceUsage_Rwanda_cleaned.csv")
