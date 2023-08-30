# perch mounts
PERCH_MOUNTS = "/api/perch_mounts"
PERCH_MOUNT1 = "/api/perch_mount/<int:perch_mount_id>"
PERCH_MOUNT2 = "/api/perch_mount"  # post behavior
PERCH_MOUNT_SECTIONS = "/api/perch_mount/<int:perch_mount_id>/sections"

# perch mount count
PERCH_MOUNT_MEDIA_COUNT = "/api/perch_mount/<int:perch_mount_id>/media_count"
PENDING_PERCH_MOUNTS = "/api/pending_perch_mounts"
PERCH_MOUNT_PREY_COUNT = "/api/perch_mount/<int:perch_mount_id>/section_preys"
PERCH_MOUNT_MONTH_PENDING_EMPTY_COUNT = (
    "/api/perch_mount/<int:perch_mount_id>/month_pending_empty_count"
)
PERCH_MOUNT_MONTH_PENDING_DETECTED_COUNT = (
    "/api/perch_mount/<int:perch_mount_id>/month_pending_detected_count"
)
EMPTY_DAY_COUNT = "/api/perch_mount/<int:perch_mount_id>/empty_day_count"
DETECTED_DAY_COUNT = "/api/perch_mount/<int:perch_mount_id>/detected_day_count"

# claim perch mount
PERCH_MOUNT_CLAIM_BY1 = (
    "/api/claim_perch_mount/<int:perch_mount_id>/claim_by/<int:member_id>"
)
PERCH_MOUNT_CLAIM_BY2 = "/api/claim_perch_mount/<int:perch_mount_id>"

# section
SECTION1 = "/api/section/<int:section_id>"
SECTION2 = "/api/section"
SECTION_MEDIA = "/api/section/<int:section_id>/media"
SECTION_EMPTY_MEDIA = "/api/section/<int:section_id>/empty_media"
SECTION_DETECTED_MEDIA = "/api/section/<int:section_id>/detected_media"
SECTION_OPERATORS = "/api/section/<int:section_id>/operators"


# Review, Empty check and Indentify prey
# empty check
EMPTY_CHECK_PERCH_MOUNT_1 = (
    "/api/empty_check/perch_mount/<int:perch_mount_id>/limit/<int:limit>"
)
EMPTY_CHECK_PERCH_MOUNT_2 = "/api/empty_check"
EMPTY_CHECK_SECTION = "/api/empty_check/section/<int:section_id>/limit/<int:limit>"
EMPTY_CHECK_MONTH_PERCH_MOUNT_ = "/api/empty_check/perch_mount/<int:perch_mount_id>/year_month/<string:year_month>/limit/<int:limit>"

# review
REVIEW_PERCH_MOUNT_1 = "/api/review/perch_mount/<int:perch_mount_id>/limit/<int:limit>"
REVIEW_PERCH_MOUNT_2 = "/api/review"
REVIEW_MONTH_PERCH_MOUNT_ = "/api/review/perch_mount/<int:perch_mount_id>/year_month/<string:year_month>/limit/<int:limit>"
REVIEW_SECTION = "/api/review/section/<int:section_id>/limit/<int:limit>"

# prey identification
IDENTIFY_PREY_SECTION = "/api/identify_prey/<string:predator>/section/<int:section_id>"
PREY = "/api/prey/<int:individual_id>"

# medium information
MEDIUM = "/api/medium/<string:medium_id>"
MEDIUM_INDIVIDUALS = "/api/medium/<string:medium_id>/individuals"
FEATURD_MEDIUM = "/api/medium/<string:medium_id>/feature"

# individual
INDIVIDUAL1 = "/api/individual/<int:individual_id>"
INDIVIDUAL2 = "/api/individual/at_medium/<string:medium_id>"

# options
BEHAVIORS = "/api/behaviors"
POSITIONS = "/api/positions"
HABITATS = "/api/habitats"
CAMERAS = "/api/cameras"
EVENTS = "/api/events"
LAYERS = "/api/layers"
MOUNT_TYPES = "/api/mount_types"
PROJECTS = "/api/projects"
PROJECT = "/api/project"
MEMBERS = "/api/members"
SPECIES = "/api/species"

BEHAVIOR = "/api/behavior"
CAMERA = "/api/camera"
EVENT = "/api/event"

# front end species name prediction
SPECIES_SEARCH = "/api/species_trie/<string:word>"
SPECIES_TAXON_ORDERS = "/api/taxon_orders"

# member
MEMBER1 = "/api/member/<int:member_id>"
MEMBER2 = "/api/member"
PERCH_MOUNTS_CLAIM_BY = "/api/member/<int:member_id>/perch_mounts"
MEMBER_CONTRIBUTIONS = "/api/member/<int:member_id>/contributions"

# contribution
CONTRIBUTION = "/api/contribution"

# featured filter
FEATURED_MEDIA = "/api/featured/page/<int:page>/perch_mount/<string:perch_mount_name>/behavior/<int:behavior_id>/species/<string:chinese_common_name>/member/<int:member_id>"


# api for schedule dectection
SCHEDULE_DETECT_MEDIA = "/api/section/<int:section_id>/schedule_detect"


ALL_UPDATE_INFO = "/api/updates"
UPDATE_INFO1 = "/api/update_info"
UPDATE_INFO2 = "/api/update_info/<int:update_info_id>"


# row data download
QUERY_DATA = "/api/query_data"
RECORD_SPECIES = "/api/record_species"

PROCESSED_DATA = "/api/processed_data"

SCHEDULE_DETECT_COUNT = "/api/schedule_detect_count/section/<int:section_id>/num_files/<int:num_files>/is_image/<int:is_image>"
