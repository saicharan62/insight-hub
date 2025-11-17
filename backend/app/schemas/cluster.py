from pydantic import BaseModel
from typing import List

class ClusterEntry(BaseModel):
    cluster_id: int
    insight_id: List[int]
    representative: str | None

class ClusterResponse(BaseModel):
    clusters: List[ClusterEntry]

    class config:
        from_attributes = True
