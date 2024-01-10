# %% [code]
import pandas as pd
from tqdm.autonotebook import tqdm
import os
import matplotlib.pyplot as plt
import json
import nltk
import re
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import OrderedDict, Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import seaborn as sns
import warnings

nltk.download('stopwords')
warnings.filterwarnings('ignore')
nltk.download('punkt')
nltk.download('wordnet')

# %% [code]
train_df = pd.read_csv('../input/coleridgeinitiative-show-us-the-data/train.csv')
train_files_path = '../input/coleridgeinitiative-show-us-the-data/train'

# %% [code]
train_df = train_df.sample(frac=1).reset_index(drop=True)


# %% [code]
def Concatenate(filename, files_path=train_files_path, output='text'):
    json_path = os.path.join(train_files_path, (filename + '.json'))
    headings = []
    contents = []
    combined = []
    with open(json_path, 'r') as f:
        json_decode = json.load(f)
        for data in json_decode:
            headings.append(data.get('section_title'))
            contents.append(data.get('text'))
            combined.append(data.get('section_title'))
            combined.append(data.get('text'))

    all_headings = ' '.join(headings)
    all_contents = ' '.join(contents)
    all_data = '. '.join(combined)

    if output == 'text':
        return all_contents
    elif output == 'head':
        return all_headings
    else:
        return all_data


tqdm.pandas()
train_df['text'] = train_df['Id'].progress_apply(Concatenate)

# %% [code]
train_df.head(10)

# %% [code]
train_df.drop(columns=['pub_title', 'dataset_title', 'dataset_label', 'Id'], inplace=True)

# %% [code]
len(train_df['cleaned_label'].value_counts())

# %% [code]
train_df.isna().sum()

# %% [code]
train_df['cleaned_label'].value_counts().plot(kind='bar', color='red', figsize=(24, 20), fontsize=10)
plt.xlabel('labels')
plt.ylabel('Total label count')
plt.title('label count of each label type')


# %% [code]
def cleaning_text(text):
    text = re.sub("[^a-zA-Z]", " ", text)
    text = re.sub('[!@#$_]', '', text)
    text = text.replace("co", "")
    text = text.replace("http", "")
    text = ' '.join(text.split())
    text = text.lower()
    return text


train_df['cleaned_text'] = train_df['text'].progress_apply(lambda x: cleaning_text(x))

# %% [code]
df = train_df.copy()


# %% [code]
def tokenize(text):
    token_words = word_tokenize(str(text))
    return " ".join(token_words)


train_df['cleaned_text_tokenized'] = train_df['cleaned_text'].progress_apply(lambda x: tokenize(x))


# %% [code]
def stopwords_clean(text):
    stop_words = set(stopwords.words('english'))
    no_stopword_text = [w for w in str(text).split() if not w in stop_words]
    return " ".join(no_stopword_text)


train_df['text_cleaned_nostop'] = train_df['cleaned_text_tokenized'].progress_apply(lambda x: stopwords_clean(x))

# %% [code]
import nltk
from nltk.stem import WordNetLemmatizer

lemma = WordNetLemmatizer()


def lemmatize_text(text):
    lemma_text = [lemma.lemmatize(word) for word in text]
    return "".join(lemma_text)


train_df['texts_cleaned_lemmatized'] = train_df['text_cleaned_nostop'].progress_apply(lambda x: lemmatize_text(x))

# %% [code]
train_df['texts_cleaned_lemmatized'] = (
    train_df['texts_cleaned_lemmatized'].str.split().progress_apply(lambda x: OrderedDict.fromkeys(x).keys()).str.join(
        ' '))

# %% [code]
train_df.head(10)

# %% [code]
Train_df = train_df.copy()

# %% [code]
Train_df.info()

# %% [code]
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

text_docs = [TaggedDocument(doc.split(' '), [i])
             for i, doc in enumerate(Train_df.texts_cleaned_lemmatized)]
model = Doc2Vec(vector_size=128, min_count=3, epochs=30)
# instantiate model
model = Doc2Vec(vector_size=128, window=2, min_count=3, workers=8, epochs=50)
# build vocab
model.build_vocab(text_docs)
# train model
model.train(text_docs, total_examples=model.corpus_count
            , epochs=model.epochs)

# %% [code]
text2vec = [model.infer_vector((Train_df['texts_cleaned_lemmatized'][i].split(' ')))
            for i in range(0, len(Train_df['texts_cleaned_lemmatized']))]

# %% [code]
dtv = np.array(text2vec).tolist()
Train_df['text2vec'] = dtv
Train_df.head(2)

# %% [code]
sparce_matrix = text2vec
y = Train_df.iloc[:, 0].values
X = sparce_matrix

# %% [code]
encoder = LabelEncoder()
y = encoder.fit_transform(y)
# y[:10]
# X[:5]

# %% [code]
decoded = encoder.inverse_transform(y)
# decoded[:10]

# %% [code]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=45)

# %% [markdown]
# *Note - Accuracy is a bad metric of evaluation for the models as the classes are heavily imbalanced*

# %% [markdown]
# **Logistic Regression Classifier**

# %% [code]
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
logistic = LogisticRegression(penalty='l1', solver='liblinear', C=0.1, random_state=45)
pipeline = Pipeline(steps=[('sc', sc), ('logistic', logistic)])
pipeline.fit(X_train, y_train)

# %% [markdown]
# Accuracy

# %% [code]
y_pred = pipeline.predict(X_test)
print('Accuracy:', accuracy_score(y_test, y_pred))
# print('Confusion matrix:\n',confusion_matrix(y_test,y_pred))
# print('Classification report:\n',classification_report(y_test,y_pred))

# %% [markdown]
# **RandomForest Classifier**

# %% [code]
from sklearn.ensemble import RandomForestClassifier

rfc1 = RandomForestClassifier(n_estimators=50, max_depth=15, bootstrap=True, random_state=45)
rfc1.fit(X_train, y_train)

# %% [markdown]
# Accuracy

# %% [code]
y_pred = rfc1.predict(X_test)
print('Accuracy:', accuracy_score(y_test, y_pred))
# print('Confusion matrix:\n',confusion_matrix(y_test,y_pred))
# print('Classification report:\n',classification_report(y_test,y_pred))

# %% [markdown]
# **Support Vector Machine Classifier**

# %% [code]
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
svm = SVC(C=1, gamma='scale', kernel='linear')
pipe = Pipeline(steps=[('sc', sc),
                       ('SVM', svm)])

pipe.fit(X_train, y_train)

# %% [markdown]
# Accuracy

# %% [code]
y_pred = pipe.predict(X_test)
print('Accuracy:', accuracy_score(y_test, y_pred))
# print('Confusion matrix:\n',confusion_matrix(y_test,y_pred))
# print('Classification report:\n',classification_report(y_test,y_pred))

# %% [markdown]
# **Naive Bayes Classifier**

# %% [code]
from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()
gnb.fit(X_train, y_train)

# %% [markdown]
# Accuracy

# %% [code]
y_pred = gnb.predict(X_test)
from sklearn import metrics

print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

# %% [markdown]
# **BERT**

# %% [markdown]
# Encoding the Labels

# %% [code]
df.head(5)

# %% [code]
possible_labels = df.cleaned_label.unique()

label_dict = {}
for index, possible_label in enumerate(possible_labels):
    label_dict[possible_label] = index
label_dict

# %% [code]
df['label'] = df.cleaned_label.replace(label_dict)

# %% [markdown]
# Train and Validation Split

# %% [code]
from sklearn.model_selection import train_test_split

X_train, X_val, y_train, y_val = train_test_split(df.index.values,
                                                  df.label.values,
                                                  test_size=0.15,
                                                  random_state=42)

df['data_type'] = ['not_set'] * df.shape[0]

df.loc[X_train, 'data_type'] = 'train'
df.loc[X_val, 'data_type'] = 'val'

df.groupby(['cleaned_label', 'label', 'data_type']).count()

# %% [markdown]
# BertTokenizer and Encoding the Data

# %% [code]
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

# %% [code]

import transformers
import torch
import torchvision
from torch.utils.data import TensorDataset
from transformers import BertForSequenceClassification

# %% [code]
tokenizer = transformers.BertTokenizer.from_pretrained('bert-base-uncased',
                                                       do_lower_case=True)

encoded_data_train = tokenizer.batch_encode_plus(
    df[df.data_type == 'train'].cleaned_text.values,
    add_special_tokens=True,
    return_attention_mask=True,
    pad_to_max_length=True,
    max_length=256,
    return_tensors='pt'
)

encoded_data_val = tokenizer.batch_encode_plus(
    df[df.data_type == 'val'].cleaned_text.values,
    add_special_tokens=True,
    return_attention_mask=True,
    pad_to_max_length=True,
    max_length=256,
    return_tensors='pt'
)

input_ids_train = encoded_data_train['input_ids']
attention_masks_train = encoded_data_train['attention_mask']
labels_train = torch.tensor(df[df.data_type == 'train'].label.values)

input_ids_val = encoded_data_val['input_ids']
attention_masks_val = encoded_data_val['attention_mask']
labels_val = torch.tensor(df[df.data_type == 'val'].label.values)

dataset_train = TensorDataset(input_ids_train, attention_masks_train, labels_train)
dataset_val = TensorDataset(input_ids_val, attention_masks_val, labels_val)

# %% [code]
len(dataset_train), len(dataset_val)

# %% [markdown]
# BERT Pre-trained Model

# %% [code]
model = BertForSequenceClassification.from_pretrained("bert-base-uncased",
                                                      num_labels=len(label_dict),
                                                      output_attentions=False,
                                                      output_hidden_states=False)

# %% [markdown]
# Data Loaders

# %% [code]
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler

batch_size = 3

dataloader_train = DataLoader(dataset_train,
                              sampler=RandomSampler(dataset_train),
                              batch_size=batch_size)

dataloader_validation = DataLoader(dataset_val,
                                   sampler=SequentialSampler(dataset_val),
                                   batch_size=batch_size)

# %% [markdown]
# Optimizer & Scheduler

# %% [code]
from transformers import AdamW, get_linear_schedule_with_warmup

optimizer = AdamW(model.parameters(),
                  lr=1e-5,
                  eps=1e-8)

epochs = 5

scheduler = get_linear_schedule_with_warmup(optimizer,
                                            num_warmup_steps=0,
                                            num_training_steps=len(dataloader_train) * epochs)

# %% [markdown]
# Performance Metrics

# %% [code]
from sklearn.metrics import f1_score


def f1_score_func(preds, labels):
    preds_flat = np.argmax(preds, axis=1).flatten()
    labels_flat = labels.flatten()
    return f1_score(labels_flat, preds_flat, average='weighted')


def accuracy_per_class(preds, labels):
    label_dict_inverse = {v: k for k, v in label_dict.items()}

    preds_flat = np.argmax(preds, axis=1).flatten()
    labels_flat = labels.flatten()

    for label in np.unique(labels_flat):
        y_preds = preds_flat[labels_flat == label]
        y_true = labels_flat[labels_flat == label]
        print(f'Class: {label_dict_inverse[label]}')
        print(f'Accuracy: {len(y_preds[y_preds == label])}/{len(y_true)}\n')


# %% [markdown]
# Training Loop

# %% [code]
import random

seed_val = 17
random.seed(seed_val)
np.random.seed(seed_val)
torch.manual_seed(seed_val)
torch.cuda.manual_seed_all(seed_val)

# %% [code]
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

print(device)


# %% [code]
def evaluate(dataloader_val):
    model.eval()

    loss_val_total = 0
    predictions, true_vals = [], []

    for batch in dataloader_val:
        batch = tuple(b.to(device) for b in batch)

        inputs = {'input_ids': batch[0],
                  'attention_mask': batch[1],
                  'labels': batch[2],
                  }

        with torch.no_grad():
            outputs = model(**inputs)

        loss = outputs[0]
        logits = outputs[1]
        loss_val_total += loss.item()

        logits = logits.detach().cpu().numpy()
        label_ids = inputs['labels'].cpu().numpy()
        predictions.append(logits)
        true_vals.append(label_ids)

    loss_val_avg = loss_val_total / len(dataloader_val)

    predictions = np.concatenate(predictions, axis=0)
    true_vals = np.concatenate(true_vals, axis=0)

    return loss_val_avg, predictions, true_vals


# %% [code]
for epoch in tqdm(range(1, epochs + 1)):

    model.train()

    loss_train_total = 0

    progress_bar = tqdm(dataloader_train, desc='Epoch {:1d}'.format(epoch), leave=False, disable=False)
    for batch in progress_bar:
        model.zero_grad()

        batch = tuple(b.to(device) for b in batch)

        inputs = {'input_ids': batch[0],
                  'attention_mask': batch[1],
                  'labels': batch[2],
                  }

        outputs = model(**inputs)

        loss = outputs[0]
        loss_train_total += loss.item()
        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

        optimizer.step()
        scheduler.step()

        progress_bar.set_postfix({'training_loss': '{:.3f}'.format(loss.item() / len(batch))})

    torch.save(model.state_dict(), f'finetuned_BERT_epoch_{epoch}.model')

    tqdm.write(f'\nEpoch {epoch}')

    loss_train_avg = loss_train_total / len(dataloader_train)
    tqdm.write(f'Training loss: {loss_train_avg}')

    val_loss, predictions, true_vals = evaluate(dataloader_validation)
    val_f1 = f1_score_func(predictions, true_vals)
    tqdm.write(f'Validation loss: {val_loss}')
    tqdm.write(f'F1 Score (Weighted): {val_f1}')

# %% [markdown]
# Loading and Evaluating the Model

# %% [code]
model = BertForSequenceClassification.from_pretrained("bert-base-uncased",
                                                      num_labels=len(label_dict),
                                                      output_attentions=False,
                                                      output_hidden_states=False)

model.to(device)

# %% [code]
model.load_state_dict(torch.load('finetuned_BERT_epoch_1.model', map_location=torch.device('cpu')))

# %% [code]
_, predictions, true_vals = evaluate(dataloader_validation)

# %% [code]
accuracy_per_class(predictions, true_vals)