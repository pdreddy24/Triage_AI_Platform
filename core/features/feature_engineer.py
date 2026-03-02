def assemble_features(amount: float,
                      velocity: int,
                      embedding: dict) -> list:

    return [
        amount,
        velocity,
        embedding.get("emb_0", 0.0),
        embedding.get("emb_1", 0.0),
        embedding.get("emb_2", 0.0),
        embedding.get("emb_3", 0.0),
    ]