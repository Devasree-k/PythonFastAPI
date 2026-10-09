class TransportCollectionNotFoundException(Exception):

    def __init__(self, collection_id: int):

        self.collection_id = collection_id

        self.message = (
            f"Transport collection with ID {collection_id} was not found"
        )

        super().__init__(self.message)