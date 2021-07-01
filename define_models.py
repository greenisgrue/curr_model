# model: [wmd, cos] - Vilken model som ska användas
# CI_parent: [True, False] - Om rubriker till centralt innehåll ska inkluderas
# content_title: [True, False] - Om innehållets titel + undertitel ska inkluderas

def defined_models():
    model_1 = {'model':'wmd', 'CI_parent':False, 'content_title':False}
    model_2 = {'model':'wmd', 'CI_parent':True, 'content_title':True}
    model_holder = [model_1, model_2]
    return model_holder





