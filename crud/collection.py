from sqlalchemy.orm import Session
from models.collection import Collection
from models.item import Item
from schemas.collection import CollectionCreate
from sqlalchemy.orm import joinedload
from crud.item import delete_item_by_id
def create_collection(db: Session, collection: CollectionCreate):
    collection = Collection(
        collection_title=collection.collection_title,
        user_id=collection.user_id,
    )
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection

def get_collection_with_items(db: Session, collection_id: int):
    return db.query(Collection)\
        .options(
            joinedload(Collection.items).joinedload(Item.images)
        )\
        .filter(Collection.collection_id == collection_id)\
        .first()

def delete_collection_by_id(db: Session, collection_id: int):
    collection = db.query(Collection).filter(Collection.collection_id == collection_id).first()
    if collection:
        for item in collection.items:
            delete_item_by_id(db, item.item_id)
        db.delete(collection)
        db.commit()
    return collection
