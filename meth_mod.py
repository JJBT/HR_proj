
def save_model(model_name, model, accuracy, features):
    import json
    import pickle

    pickle.dump(model, open('full/' + model_name, 'wb'))

    with open('full/' + model_name + '_descr.json', 'w') as file:
        descr_dict = {
            'valid accuracy': accuracy,
            'features': features,
        }

        json.dump(descr_dict, file, indent=4)


def predict(model, X):
    probas = model.predict_proba(X)[:, 1]
    preds = [1 if x > 0.666 else 0 for x in probas]
    return preds
