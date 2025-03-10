import textwrap

import pytest

from conans.test.utils.tools import TestClient

PKG_ID_NO_CONF = "ebec3dc6d7f6b907b3ada0c3d3cdc83613a2b715"
PKG_ID_1 = "89d32f25195a77f4ae2e77414b870781853bdbc1"
PKG_ID_2 = "7f9ed92704709f56ecc7b133322479caf3ffd7ad"
PKG_ID_3 = "45b796ec237c7e2399944e79bee49b56fd022067"


@pytest.mark.parametrize("package_id_confs, package_id", [
    ('[]', PKG_ID_NO_CONF),
    ('["user.fake:no_existing_conf"]', PKG_ID_NO_CONF),
    ('["tools.build:cxxflags", "tools.build:cflags"]', PKG_ID_1),
    ('["tools.build:defines"]', PKG_ID_2),
    ('["tools.build:cxxflags", "tools.build:sharedlinkflags"]', PKG_ID_3),
])
def test_package_id_including_confs(package_id_confs, package_id):
    client = TestClient()
    conanfile = textwrap.dedent("""
        from conan import ConanFile
        class Pkg(ConanFile):
            settings = "os"
        """)
    profile = textwrap.dedent(f"""
    include(default)
    [conf]
    tools.info.package_id:confs={package_id_confs}
    tools.build:cxxflags=["--flag1", "--flag2"]
    tools.build:cflags+=["--flag3", "--flag4"]
    tools.build:sharedlinkflags=+["--flag5", "--flag6"]
    tools.build:exelinkflags=["--flag7", "--flag8"]
    tools.build:defines=["D1", "D2"]
    """)
    client.save({"conanfile.py": conanfile, "profile": profile})
    client.run('create . --name=pkg --version=0.1 -s os=Windows -pr profile')
    client.assert_listed_binary({"pkg/0.1": (package_id, "Build")})


PKG_ID_4 = "9b334fc314f2f2ce26e5280901eabcdd7b3f55a6"
PKG_ID_5 = "5510413d2e6186662cb473fb16ce0a18a3f9e98f"


@pytest.mark.parametrize("cxx_flags, package_id", [
    ('[]', PKG_ID_NO_CONF),
    ('["--flag1", "--flag2"]', PKG_ID_4),
    ('["--flag3", "--flag4"]', PKG_ID_5),
])
def test_same_package_id_configurations_but_changing_values(cxx_flags, package_id):
    client = TestClient()
    conanfile = textwrap.dedent("""
        from conan import ConanFile
        class Pkg(ConanFile):
            settings = "os"
        """)
    profile = textwrap.dedent(f"""
    include(default)
    [conf]
    tools.info.package_id:confs=["tools.build:cxxflags"]
    tools.build:cxxflags={cxx_flags}
    tools.build:cflags+=["--flag3", "--flag4"]
    tools.build:sharedlinkflags=+["--flag5", "--flag6"]
    tools.build:exelinkflags=["--flag7", "--flag8"]
    tools.build:defines=["D1", "D2"]
    """)
    client.save({"conanfile.py": conanfile, "profile": profile})
    client.run('create . --name=pkg --version=0.1 -s os=Windows -pr profile')
    client.assert_listed_binary({"pkg/0.1": (package_id, "Build")})
