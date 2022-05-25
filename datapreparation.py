model = keras.models.load_model('/model/general')
model2 = keras.models.load_model('/model/feeling')

#link_general = '/data/general.csv'
#link_feeling = '/data/feeling.csv'
models = [model, model2]
#datasets = [link_general, link_feeling]
tokenizers = []
word_indices = []
sequences_array = []
lengths_input = []
labels_transformed_array = []
