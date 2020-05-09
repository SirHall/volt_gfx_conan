from conans import ConanFile, CMake, tools


class VoltgfxConan(ConanFile):
    name = "volt_gfx"
    version = "0.0.1"
    license = "GPL3"
    author = "sirhallstein@gmail.com"
    url = "https://www.github.com/SirHall/volt_gfx_conan"
    requires = \
    [
        "glfw/3.3.2@bincrafters/stable",
        "glm/0.9.9.5@g-truc/stable",
        "volt_event/0.0.1@volt/dev",
        "glew/2.1.0@bincrafters/stable",
        "boost/1.71.0@conan/stable",
        "zlib/1.2.11@conan/stable"
    ]
    description = "Library that handles graphics rendering"
    topics = ("c++", "graphics", "crossplatform")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    exports_sources = "include/**"

    def source(self):
        git = tools.Git(folder="volt_gfx")
        git.clone("https://www.github.com/SirHall/volt_gfx.git", "master")

        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("volt_gfx/CMakeLists.txt", "project(volt_ge_gfx)",
                              '''project(volt_ge_gfx)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="volt_gfx")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include/",
                  src="volt_gfx/volt_gfx/include/", keep_path=True)
        self.copy("*.hpp", dst="include/",
                  src="volt_gfx/volt_gfx/include", keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("libvolt_gfx.a", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["volt_gfx"]
