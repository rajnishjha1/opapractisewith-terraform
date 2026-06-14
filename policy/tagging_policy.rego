package terraform.tags

required_tags = ["Name", "Environment", "Owner"]

deny[msg] if {
    rc = input.resource_changes[_]
    startswith(rc.type, "aws_")
    rc.change.actions[_] != "delete"
    required_tags[_] = tag
    not rc.change.after.tags[tag]
    msg = sprintf("resource %s is missing tag %s", [rc.address, tag])
}
