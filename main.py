import warnings
import pandas as pd
import keras
from sklearn.model_selection import train_test_split
from keras.models import Model
from keras.layers import Dense, Input, Dropout, Activation

warnings.filterwarnings('ignore')
features = ['site', 'career', 'has_descr', 'it_descr', 'post_count', 'it_post_count',
           'y', 'tight_post', 'it_post_prop']

df = pd.read_excel('Base.xlsx')
df = df.loc[:, features]


X, y = df.drop('y', axis=1).values, df['y'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, random_state=42, test_size=0.35)

y_train = keras.utils.to_categorical(y_train, num_classes=2)
y_test = keras.utils.to_categorical(y_test, num_classes=2)

input_shape = X_train[0].shape
a = Input(shape=input_shape)
b = Dense(200)(a)
b = Activation('relu')(b)
b = Dropout(0.2)(b)
b = Dense(150)(b)
b = Activation('relu')(b)
b = Dropout(0.2)(b)
b = Dense(150)(b)
b = Activation('relu')(b)
b = Dropout(0.5)(b)
b = Dense(80)(b)
b = Activation('relu')(b)
b = Dropout(0.2)(b)
b = Dense(80)(b)
b = Activation('relu')(b)
b = Dropout(0.2)(b)
b = Dense(50)(b)
b = Activation('relu')(b)
b = Dropout(0.2)(b)
b = Dense(10)(b)
b = Activation('relu')(b)
b = Dense(2)(b)
b = Activation('softmax')(b)

model = Model(inputs=a, outputs=b)

model.compile(metrics=['accuracy'],
              optimizer='adam',
              loss='categorical_crossentropy')

model.fit(X_train, y_train, epochs=500, validation_split=0.35)
score = model.evaluate(X_test, y_test)
print(score)
model.save('model.h5')
model.save_weights('weights.h5')
