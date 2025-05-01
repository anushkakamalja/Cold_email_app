
import pandas as pd
import chromadb
import uuid


class Resume:
    def __init__(self, file_path="resource/tech_stack_resume_mapping.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="resume")

    def load_resume(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Tech_Stack"],
                                    metadatas={"links": row["Resume_Link"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        results = self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
        links = [item["links"] for item in results if "links" in item]
        return links[0] if links else "Link not available"