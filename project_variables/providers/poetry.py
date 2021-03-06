from os.path import isfile

import toml


class PoetryProvider:
    lock_file = "poetry.lock"
    project = "pyproject.toml"

    def is_enabled(self):
        return isfile(PoetryProvider.lock_file)

    def dump(self, variables):
        lock = open(PoetryProvider.lock_file).read()
        packages = {package["name"]: package["version"] for package in toml.loads(lock).get("package")}

        library = False
        package_version = None
        if isfile(PoetryProvider.project):
            package = toml.loads(open(PoetryProvider.project).read())
            library = "library" in package.get("tool").get("poetry").get("keywords", [])
            package_version = package.get("tool").get("poetry").get("version")

        local = dict(
            use_black=packages.get("black", 0),
            use_flake8=packages.get("flake8", 0),
            use_pytest=packages.get("pytest", 0),
            is_library=library,
        )

        if variables.get("workflow") in ("release_created", "release_published"):
            local["package_version"] = package_version

        local["artifact_version"] = f"{variables.get('project_name')}@{variables.get('package_version')}"

        return local
