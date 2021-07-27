# model: [wmd, cos, opti_wmd, opti_cos] - Vilken model som ska användas
# CI_parent: [True, False] - Om rubriker till centralt innehåll ska inkluderas. Om opti_cos eller opti_wmd används, sätt till False
# content_title: [True, False] - Om innehållets titel + undertitel ska inkluderas. Om opti_cos eller opti_wmd används, sätt till False

def defined_models():
    model_1 = {'model':'opti_cos', 'CI_parent':False, 'content_title':False, 'jaccard':False, 'key_factor':True}
    model_2 = {'model':'opti', 'CI_parent':False, 'content_title':False, 'jaccard':True, 'key_factor':True}
    model_holder = [model_1, model_2]
    return model_holder





