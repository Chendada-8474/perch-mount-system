import marshmallow


class DetectedIndividualSchema(marshmallow.Schema):
    taxon_order_by_ai = marshmallow.fields.Integer(required=True)
    box_xmin = marshmallow.fields.Float()
    box_xmax = marshmallow.fields.Float()
    box_ymin = marshmallow.fields.Float()
    box_ymax = marshmallow.fields.Float()


class ReviewedIndividualSchema(marshmallow.Schema):
    id = marshmallow.fields.UUID(allow_none=True)
    taxon_order_by_human = marshmallow.fields.Integer(required=True)
    box_xmin = marshmallow.fields.Float(allow_none=True)
    box_xmax = marshmallow.fields.Float(allow_none=True)
    box_ymin = marshmallow.fields.Float(allow_none=True)
    box_ymax = marshmallow.fields.Float(allow_none=True)
    has_prey = marshmallow.fields.Boolean(required=True)
    is_tagged = marshmallow.fields.Boolean(required=True)
    has_ring = marshmallow.fields.Boolean(required=True)
    ring_number = marshmallow.fields.Boolean(allow_none=True)


class MediumSchema(marshmallow.Schema):
    pass


class UploadedMediumSchema(MediumSchema):
    id = marshmallow.fields.UUID()
    medium_datetime = marshmallow.fields.DateTime(format="iso", required=True)
    medium_type = marshmallow.fields.String(required=True)
    s3_file_name = marshmallow.fields.String(required=True)


class UploadedData(MediumSchema):
    perch_mount_id = marshmallow.fields.UUID(required=True)
    mount_type_id = marshmallow.fields.UUID(required=True)
    camera_id = marshmallow.fields.UUID(required=True)
    start_time = marshmallow.fields.DateTime(format="iso", required=True)
    end_time = marshmallow.fields.DateTime(format="iso", required=True)
    swapped_date = marshmallow.fields.Date(format="iso", required=True)
    swapper_ids = marshmallow.fields.List(marshmallow.fields.UUID, required=True)
    valid = marshmallow.fields.Boolean(required=True)
    note = marshmallow.fields.String()
    media = marshmallow.fields.List(
        marshmallow.fields.Nested(UploadedMediumSchema),
        required=True,
    )


class DetectedMediumSchema(MediumSchema):
    id = marshmallow.fields.UUID(required=True)
    detected_at = marshmallow.fields.DateTime(format="iso", required=True)
    individuals = marshmallow.fields.List(
        marshmallow.fields.Nested(DetectedIndividualSchema), required=True
    )


class CheckedMediumSchema(MediumSchema):
    id = marshmallow.fields.UUID(required=True)
    empty_checked_at = marshmallow.fields.DateTime(format="iso", required=True)
    empty_checker_id = marshmallow.fields.UUID(required=True)
    has_individual = marshmallow.fields.Boolean(required=True)


class ReviewedMediumSchema(MediumSchema):
    id = marshmallow.fields.UUID(required=True, allow_none=True)
    reviewed_at = marshmallow.fields.DateTime(format="iso", required=True)
    reviewer_id = marshmallow.fields.UUID(required=True)
    featured_by_id = marshmallow.fields.UUID(allow_none=True)
    event_id = marshmallow.fields.UUID(allow_none=True)
    behavior_id = marshmallow.fields.UUID(allow_none=True)
    individuals = marshmallow.fields.List(
        marshmallow.fields.Nested(ReviewedIndividualSchema), required=True
    )
