

from platformio.managers.platform import PlatformBase

class P115Platform(PlatformBase):

    def configure_default_packages(self, variables, targets):
        if not variables.get("board"):
            return super(P115Platform, self).configure_default_packages(
                variables, targets)

        build_core = variables.get(
            "board_build.core", self.board_config(variables.get("board")).get(
                "build.core", "arduino"))

        if any(t in targets for t in ("fuses", "bootloader")):
            self.packages["tool-avrdude-megaavr"]["optional"] = False

        return super(P115Platform, self).configure_default_packages(
            variables, targets)
