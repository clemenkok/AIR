from dataclasses import dataclass

@dataclass
class Node:
    name: str
    url: str
    paper_id: str

    def __repr__(self):
        return f"{self.name=}, {self.url=}, {self.paper_id=}"

    def __hash__(self):
        return hash(self.name)