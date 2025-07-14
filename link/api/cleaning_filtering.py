def find_mean(b,a):
    res = (b + a) / 2
    #--@b=before 
    #--@a=after
    return res

def replace_na(df, comodin):
    df_new = df.copy
    for col in df.columns:
        dtype = df[col].dtype
        print("dtype:", dtype)
        df_cond = df[col].isna()
        if comodin == 'mean':
            for i in range(len(df[col])):
                if df_cond[i] == True:
                    mean = find_mean(df[col][i-1], df[col][i+1])
                    df_new[col][i] = mean
    return df_new


def complex_patterns(df):
    multi_white_space = "\s+"
    for col in df.columns:
        for el in df[col]:
            regex = re.compile(r"\s+")
            patterns = regex.findall(el)
            for pat in patterns:
                el.replace(pat, " ")
    return df

def clean(df):
    df_new = df.copy
    for col in df.columns:
        new_df_col = [el.strip() for el in df[col]]
        new_df[col] = new_df_col
    return df_new 

