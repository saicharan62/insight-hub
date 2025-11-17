# app/core/clustering.py
import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Optional

# Use GPU if available
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(EMBED_MODEL_NAME, device=DEVICE)

def generate_embedding(text: str):
    """Return 1-D Python list (floats) embedding for `text`"""
    # ensure text is a str
    if text is None:
        text = ""
    vec = embedder.encode([text], show_progress_bar=False)[0]
    return vec.tolist()

def _cluster_texts_incremental(embeddings: np.ndarray, threshold: float = 0.65):
    """
    Incremental clustering on embedding vectors (numpy array of shape (n, d)).
    Returns list of clusters with indices into embeddings.
    """
    if embeddings.size == 0:
        return []

    clusters = []  # each: {'centroid': np.array, 'indices': [i,...]}

    for i, emb in enumerate(embeddings):
        if not clusters:
            clusters.append({'centroid': emb.copy(), 'indices': [i]})
            continue

        cents = np.stack([c['centroid'] for c in clusters])
        sims = cosine_similarity([emb], cents)[0]  # shape (n_clusters,)
        best_idx = int(np.argmax(sims))
        best_sim = float(sims[best_idx])

        if best_sim >= threshold:
            clusters[best_idx]['indices'].append(i)
            # update centroid as mean
            clusters[best_idx]['centroid'] = np.mean(
                np.vstack([clusters[best_idx]['centroid'], emb]), axis=0
            )
        else:
            clusters.append({'centroid': emb.copy(), 'indices': [i]})

    # convert to list with cluster ids starting at 1
    result = []
    for cid, c in enumerate(clusters, start=1):
        result.append({'cluster_id': cid, 'indices': c['indices'], 'centroid': c['centroid']})
    return result

def pick_representative(indices: List[int], texts: List[str], embeddings: np.ndarray):
    """
    Choose representative text for a cluster: the text whose embedding is most
    similar to the cluster centroid.
    """
    if not indices:
        return None
    cluster_vecs = embeddings[indices]
    centroid = np.mean(cluster_vecs, axis=0, keepdims=True)
    sims = cosine_similarity(cluster_vecs, centroid)[0]
    best_local = int(np.argmax(sims))
    best_index = indices[best_local]
    return texts[best_index]

def cluster_texts(texts: List[str], insight_ids: Optional[List[int]] = None, threshold: float = 0.65):
    """
    texts: list[str] summaries
    insight_ids: optional list[int] parallel to texts. If not provided, indexes used as ids.
    returns list of clusters:
      [{'cluster_id': 1, 'insight_ids':[id1,id2], 'representative': '...'}, ...]
    """
    if not texts:
        return []

    # compute embeddings (numpy array)
    embeddings = embedder.encode(texts, show_progress_bar=False)
    embeddings = np.asarray(embeddings)

    raw_clusters = _cluster_texts_incremental(embeddings, threshold=threshold)

    # default insight_ids to indices if not provided
    if insight_ids is None:
        insight_ids = list(range(1, len(texts) + 1))

    clusters_out = []
    for cluster in raw_clusters:
        idxs = cluster['indices']
        rep = pick_representative(idxs, texts, embeddings)
        clusters_out.append({
            'cluster_id': cluster['cluster_id'],
            'insight_ids': [insight_ids[i] for i in idxs],
            'representative': rep
        })
    return clusters_out
