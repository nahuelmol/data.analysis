
def pca(file_str, params):
    import io
    import base64
    from sktlearn.decomposition import PCA

    bytes_file = base64.b64dencode(file_str)
    bin_fl_object = BytesIO(bytes_file) #binary file-like object
    df = pd.DataFrame(bin_fl_object)

    pca = PCA(n_components=params['pcavars'])
    pca.fit(df)

    pca.get_metadata_routing()
    pca.get_params()
    pca.score()
    
    return pca_report = {
        'variance_ratio': pca.explained_variance_ratio_,
        'singular_values': pca.singular_values_,
        'covariance': pca.get_covariance(),
        'feature_names': pca.get_feature_names_out(),
        'precision':pca.get_precision()
    }


def basic_metrics(file_str, params):
    bytes_file      = base64.b64dencode(file_str)
    bin_fl_object   = BytesIO(bytes_file) #binary file-like object
    df              = pd.DataFrame(bin_fl_object)

    target = params['target']
    return report = {
            'mean':     df[target].mean(),
            'median':   df[target].median(),
            'std':      df[target].std(),
            'max':      df[target].max(),
            'min':      df[target].min()
    }
