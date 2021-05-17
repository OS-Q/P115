from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
build_core = board.get("build.core", "")

FRAMEWORK_DIR = platform.get_package_dir("framework-arduino-megaavr")
if build_core != "arduino":
    FRAMEWORK_DIR = platform.get_package_dir(
        "framework-arduino-megaavr-%s" % build_core.lower())

assert isdir(FRAMEWORK_DIR)

CPPDEFINES = [
    "ARDUINO_ARCH_MEGAAVR",
    ("ARDUINO", 10808)
]

if "build.usb_product" in board:
    CPPDEFINES += [
        ("USB_VID", board.get("build.hwids")[0][0]),
        ("USB_PID", board.get("build.hwids")[0][1]),
        ("USB_PRODUCT", '\\"%s\\"' %
         board.get("build.usb_product", "").replace('"', "")),
        ("USB_MANUFACTURER", '\\"%s\\"' %
         board.get("vendor", "").replace('"', ""))
    ]

env.SConscript("_bare.py", exports="env")

env.Append(
    CPPDEFINES=CPPDEFINES,

    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", build_core, "api", "deprecated"),
        join(FRAMEWORK_DIR, "cores", build_core)
    ],

    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries")
    ]
)

#
# Select oscillator using a special macro
#

oscillator_type = board.get("hardware", {}).get("oscillator", "internal")
if build_core == "megatinycore":
    env.Append(CPPDEFINES=[("CLOCKSOURCE", 2 if oscillator_type == "external" else 0)])
elif oscillator_type == "external" and build_core == "MegaCoreX":
    env.Append(CPPDEFINES=["USE_EXTERNAL_OSCILLATOR"])

#
# Target: Build Core Library
#

libs = []

if "build.variant" in board:
    variants_dir = join(
        "$PROJECT_DIR", board.get("build.variants_dir")) if board.get(
            "build.variants_dir", "") else join(FRAMEWORK_DIR, "variants")

    env.Append(
        CPPPATH=[
            join(variants_dir, board.get("build.variant"))
        ]
    )
    env.BuildSources(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join(variants_dir, board.get("build.variant"))
    )

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkArduino"),
    join(FRAMEWORK_DIR, "cores", build_core)
))

env.Prepend(LIBS=libs)
