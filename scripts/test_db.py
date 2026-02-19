from backend.db.session import SessionLocal
from backend.db.models import Document


db = SessionLocal()


doc = Document(
    filename="test_eviction.pdf",
    source_type="pdf",
    language="en",
    jurisdiction="India"
)


db.add(doc)
db.commit()


print("Inserted document ID:", doc.id)


db.close()
