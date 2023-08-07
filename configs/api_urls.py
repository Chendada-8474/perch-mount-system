PERCH_MOUNTS = "/api/perch_mounts"

PERCH_MOUNT1 = "/api/perch_mount/<int:perch_mount_id>"
PERCH_MOUNT2 = "/api/perch_mount"
PERCH_MOUNT_MEDIA_COUNT = "/api/perch_mount/<int:perch_mount_id>/media_count"
PENDINGPERCHMOUNTS = "/api/pending_perch_mounts"

SECTION = "/api/section/<int:section_id>"
SECTIONS_OF_PERCH_MOUNT = "/api/perch_mount/<int:perch_mount_id>/sections"
EMPTY_DAY_COUNT = "/api/perch_mount/<int:perch_mount_id>/empty_day_count"
DETECTED_DAY_COUNT = "/api/perch_mount/<int:perch_mount_id>/detected_day_count"

EMPTY_CHECK_PERCH_MOUNT_1 = (
    "/api/empty_check/perch_mount/<int:perch_mount_id>/limit/<int:limit>"
)
EMPTY_CHECK_PERCH_MOUNT_2 = "/api/empty_check"
REVIEW_PERCH_MOUNT_1 = "/api/review/perch_mount/<int:perch_mount_id>/limit/<int:limit>"
REVIEW_PERCH_MOUNT_2 = "/api/review"

EMPTY_CHECK_SECTION = "/api/empty_check/section/<int:section_id>/limit/<int:limit>"
REVIEW_SECTION = "/api/review/section/<int:section_id>/limit/<int:limit>"

MEDIUM = "/api/medium/<string:medium_id>"
SECTION_MEDIA = "/api/section/<int:section_id>/media"
SECTION_EMPTY_MEDIA = "/api/section/<int:section_id>/empty_media"
SECTION_DETECTED_MEDIA = "/api/section/<int:section_id>/detected_media"
MEDIUM_INDIVIDUALS = "/api/medium/<string:medium_id>/individuals"
INDIVIDUAL = "/api/individual/<int:individual_id>"

BEHAVIORS = "/api/behaviors"
POSITIONS = "/api/positions"
HABITATS = "/api/habitats"
CAMERAS = "/api/cameras"
EVENTS = "/api/events"
LAYERS = "/api/layers"
MOUNT_TYPES = "/api/mount_types"
PROJECTS = "/api/projects"
MEMBERS = "/api/members"

SPECIES_SEARCH = "/api/species_trie/<string:word>"
SPECIES_TAXON_ORDERS = "/api/taxon_orders"

SECTION_OPERATORS = "/api/section/<int:section_id>/operators"
PERCH_MOUNT_CLAIM_BY = "/api/claim_by/<int:member_id>/perch_mounts"

MEMBER1 = "/api/member/<int:member_id>"
MEMBER2 = "/api/member"

CONTRIBUTION = "/api/contribution"
