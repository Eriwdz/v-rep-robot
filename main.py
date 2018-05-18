from joblib import load

from data_reader import DataReader

if __name__ == '__main__':
    clf = load("models/classifier.model")
    pca = load("models/transformer.model")
    image_path = "test_images/jennifer-aniston.jpg"
    image = DataReader.read_image(image_path)
    image = pca.transform(image)
    predicted = clf.predict(image)
    print(predicted)
