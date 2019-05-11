
def save_model(model_name, model, accuracy, features):
    import json
    import pickle

    pickle.dump(model, open('models/' + model_name, 'wb'))

    with open('models/' + model_name + '_descr.json', 'w') as file:
        descr_dict = {
            'valid accuracy': accuracy,
            'features': features,
        }

        json.dump(descr_dict, file, indent=4)
