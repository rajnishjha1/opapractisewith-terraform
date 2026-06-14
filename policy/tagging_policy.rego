package terraform.tags

required_tags := [
    "Environment",
    "Owner",
    "Project"
]

deny contains msg if {
    rc := input.resource_changes[_]

    rc.change.after != null

    not rc.change.after.tags

    msg := sprintf(
        "Resource %s has no tags block",
        [rc.address]
    )
}

deny contains msg if {
    rc := input.resource_changes[_]

    rc.change.after.tags

    tag := required_tags[_]

    not rc.change.after.tags[tag]

    msg := sprintf(
        "Resource %s is missing required tag %s",
        [rc.address, tag]
    )
}