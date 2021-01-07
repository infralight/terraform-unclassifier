from exceptions.bad_format_exception import BadFormatException


class TerraformVersion:

    def __init__(self, version):
        version_parts = version.split(".")

        self.major = version_parts[0]
        self.minor = version_parts[1]
        self.patch = version_parts[2]

    @staticmethod
    def parse(version):
        version_parts = version.split('.')

        if len(version_parts) <2:
            raise BadFormatException("terraform version is in bad format")

        elif len(version_parts) == 2:
            version = version+".0"

        elif len(version_parts) > 3:
            version = '.'.join(version_parts[0:3])

        return TerraformVersion(version)

    def greaterThanEqual(self, version):
        other = TerraformVersion.parse(version)
        if self.major > other.major:
            return True
        elif self.major < other.major:
            return False
        else:
            """ major is equal """
            if self.minor > other.minor:
                return True
            elif self.minor < other.minor:
                return False
            else:
                """ minor is equal """
                return self.patch >= other.patch

    def equal(self, version):
        other = TerraformVersion.parse(version)
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch

    def greaterThan(self, version):
        if self.equal(version):
            return False
        return self.greaterThanEqual(version)

    def lowerThan(self, version):
        return not self.greaterThanEqual(version)

    def lowerThanEqual(self, version):
        return self.lowerThan(version) or self.equal(version)