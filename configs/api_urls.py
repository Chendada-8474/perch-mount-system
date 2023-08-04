PERCH_MOUNT1 = "/api/perch_mount/<int:perch_mount_id>"
PERCH_MOUNT2 = "/api/perch_mount"

SECTIONS_OF_PERCH_MOUNT = "/api/perch_mount/<int:perch_mount_id>/sections"
EMPTY_DAY_COUNT = "/api/perch_mount/<int:perch_mount_id>/empty_day_count"
DETECTED_DAY_COUNT = "/api/perch_mount/<int:perch_mount_id>/detected_day_count"

EMPTY_CHECK1 = "/api/empty_check/perch_mount/<int:perch_mount_id>/limit/<int:limit>"
EMPTY_CHECK2 = "/api/empty_check"
REVIEW1 = "/api/review/perch_mount/<int:perch_mount_id>/limit/<int:limit>"
REVIEW2 = "/api/review"

MEDIUM = "/api/medium/<string:medium_id>"
SECTION_MEDIA = "/api/section/<int:section_id>/media"
MEDIUM_INDIVIDUALS = "/api/medium/<string:medium_id>/individuals"
INDIVIDUAL = "/api/individual/<int:individual_id>"

POSITIONS = "/api/positions"
HABITATS = "/api/habitats"
CAMERAS = "/api/cameras"
EVENTS = "/api/events"
LAYERS = "/api/layers"
MOUNT_TYPES = "/api/mount_types"
PROJECTS = "/api/projects"

SECTION_OPERATORS = "/api/section/<int:section_id>/operators"
PERCH_MOUNT_CLAIM_BY = "/api/claim_by/<int:member_id>/perch_mounts"
