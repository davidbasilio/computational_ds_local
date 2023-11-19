import gensim
from gensim.models import KeyedVectors
import numpy as np
import pandas as pd
import umap
import plotly.express as px
from nltk.tokenize import word_tokenize
import nltk
from sklearn.cluster import KMeans
import hdbscan

# We decide no to do stemming or removing stop words as the large pretrained model by google has emeddings for all types of words
nltk.download('punkt')

# Load the Google News Word2Vec model
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

# Function to average word vectors for a text
def average_word_vectors(text):
    tokens = word_tokenize(text.lower())
    vectors = [model[word] for word in tokens if word in model]
    if len(vectors) > 0:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros(300)  # Return a zero vector if no words are in the model

# Load your dataset
df = pd.read_csv('/home/timm/Projects/computational_ds/data/output/cnn_2014_output.csv')
df = df.head(10000)
texts = df['Text'].tolist()

# Get vector representation for each text
vector_representations = np.array([average_word_vectors(text) for text in texts])

# UMAP for dimensionality reduction
reducer = umap.UMAP(n_components=3, random_state=42)
embedding = reducer.fit_transform(vector_representations)

#K-Means clustering on the reduced data
num_clusters = 100
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
cluster_labels = kmeans.fit_predict(embedding)


# Prepare data for Plotly visualization
plot_data = pd.DataFrame(embedding, columns=['UMAP_1', 'UMAP_2', 'UMAP_3'])
plot_data['Cluster'] = cluster_labels
plot_data['Headline'] = df['Headline']

# 3D Plotting using Plotly
fig = px.scatter_3d(
    plot_data,
    x='UMAP_1', y='UMAP_2', z='UMAP_3',
    color='Cluster',
    hover_data=['Headline'],
    color_continuous_scale=px.colors.qualitative.Set1
)

fig.update_layout(
    title='KKN + Word2Vec',
    scene=dict(
        xaxis_title='UMAP 1',
        yaxis_title='UMAP 2',
        zaxis_title='UMAP 3'
    )
)

fig.show()