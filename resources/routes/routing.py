from resources import perch_mounts
from resources import sections
from resources import species
from resources import empty_media
from resources import detected_media
from resources import media
from resources import options
from resources import members

ROUTES = [
    {
        # perch_mounts
        "route": "perch_mounts",
        "resources": [perch_mounts.PerchMounts, perch_mounts.PerchMount],
        "children": [
            {
                "route": "<int:perch_mount_id>",
                "resources": [perch_mounts.PerchMount],
                "children": [],
            }
        ],
    },
    {
        # sections
        "route": "sections",
        "resources": [sections.Sections, sections.Section],
        "children": [
            {
                "route": "<int:section_id>",
                "resources": [sections.Section],
                "children": [],
            }
        ],
    },
    {
        # media
        "route": "media",
        "resources": [media.Media],
        "children": [
            {
                "route": "<string:medium_id>",
                "resources": [media.Medium],
                "children": [],
            }
        ],
    },
    {
        # empty_media
        "route": "empty_media",
        "resources": [empty_media.EmptyMedia],
        "children": [],
    },
    {
        # detected_media
        "route": "detected_media",
        "resources": [detected_media.DetectedMedia],
        "children": [
            {
                "route": "<string:detected_medium_id>",
                "resources": [detected_media.DetectedMedium],
                "children": [],
            }
        ],
    },
    {
        # species
        "route": "species",
        "resources": [species.Species],
        "children": [
            {
                "route": "<int:taxon_order>",
                "resources": [species.ASpecies],
                "children": [],
            }
        ],
    },
    {
        # members
        "route": "members",
        "resources": [members.Members],
        "children": [
            {
                "route": "<int:member_id>",
                "resources": [members.Member],
                "children": [],
            }
        ],
    },
    {
        # behaviors
        "route": "behaviors",
        "resources": [options.Behaviors, options.Behavior],
        "children": [],
    },
    {
        # cameras
        "route": "cameras",
        "resources": [options.Cameras, options.Camera],
        "children": [],
    },
    {
        # events
        "route": "events",
        "resources": [options.Events, options.Event],
        "children": [],
    },
    {
        # habitats
        "route": "habitats",
        "resources": [options.Habitats, options.Habitat],
        "children": [],
    },
    {
        # layers
        "route": "layers",
        "resources": [options.Layers, options.Layer],
        "children": [
            {
                "route": "<int:layer_id>",
                "resources": [options.Layer],
                "children": [],
            }
        ],
    },
    {
        # mount_types
        "route": "mount_types",
        "resources": [options.MountTypes, options.MountType],
        "children": [
            {
                "route": "<int:mount_type_id>",
                "resources": [options.MountType],
                "children": [],
            }
        ],
    },
    {
        # projects
        "route": "projects",
        "resources": [options.Projects, options.Project],
        "children": [
            {
                "route": "<int:project_id>",
                "resources": [options.Project],
                "children": [],
            }
        ],
    },
    {
        # positions
        "route": "positions",
        "resources": [options.Positions, options.Position],
        "children": [
            {
                "route": "<int:position_id>",
                "resources": [options.Position],
                "children": [],
            }
        ],
    },
]
