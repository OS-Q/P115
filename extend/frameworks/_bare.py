

#
# Default flags for bare-metal programming (without any framework layers)
#

from SCons.Script import Import

Import("env")

env.Append(
    ASFLAGS=["-x", "assembler-with-cpp"],

    CFLAGS=[
        "-std=gnu11",
        "-fno-fat-lto-objects"
    ],

    CCFLAGS=[
        "-Os",
        "-w",
        "-ffunction-sections",
        "-fdata-sections",
        "-flto",
        "-mmcu=$BOARD_MCU"
    ],

    CPPDEFINES=[
        ("F_CPU", "$BOARD_F_CPU")
    ],

    CXXFLAGS=[
        "-std=gnu++11",
        "-fno-exceptions",
        "-fno-threadsafe-statics",
        "-fpermissive",
        "-Wno-error=narrowing"
    ],

    LINKFLAGS=[
        "-Os",
        "-flto",
        "-mmcu=$BOARD_MCU",
        "-Wl,--gc-sections",
        "-Wl,--section-start=.text=%s"
        % (
            "0x200"
            if env.subst("$UPLOAD_PROTOCOL") == "arduino"
            else env.BoardConfig().get("build.text_section_start", "0x0")
        ),
        "-fuse-linker-plugin"
    ],

    LIBS=["m"]
)

# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])
