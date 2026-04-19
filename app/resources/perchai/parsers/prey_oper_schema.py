import marshmallow


class IdentifiedPreySchema(marshmallow.Schema):
    individual_id = marshmallow.fields.UUID()
    inaturalist_taxa_id = marshmallow.fields.Integer(allow_none=True)
    identifier_id = marshmallow.fields.UUID(allow_none=True)
