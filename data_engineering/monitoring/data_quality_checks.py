def missing_values(df):
    return df.isnull().sum()

def duplicate_count(df):
    return df.duplicated().sum()