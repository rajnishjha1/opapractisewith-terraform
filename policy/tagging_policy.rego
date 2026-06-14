package terraform.tags

required_tags = ["Name", "Environment", "Owner"]

deny[msg] {
    rc = input.resource_changes[_]
    startswith(rc.type, "aws_")
    not rc.change.actions[_] == "delete"
    missing = [tag | required_tags[_] == tag; not rc.change.after.tags[tag]]
    count(missing) > 0
    msg = sprintf("resource %s is missing tags: %v", [rc.address, missing])
}