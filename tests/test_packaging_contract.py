# SPDX-FileCopyrightText: 2026 Michael Garcia and contributors
# SPDX-License-Identifier: MPL-2.0

"""File: tests/test_packaging_contract.py
Purpose: Execute the P5 package build and the installed-command checks.
Author: Cursor cloud agent; contact: Pending confirmation; license: MPL-2.0.
Constraints: Builds stay outside the repository. No upload. Expected digests are literals.
Related decision: DEV-2026-11-19-012.
"""

from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
APPROVED_CANDIDATE = 'bbf013354b3ac7d4fdc9be8b44090634b431b118'
CATALOG_IDS = [
    'arduino/uno-r3',
    'arduino/ventuno-q',
    'generic/hc-sr04',
    'microchip/attiny-x5',
    'ti/l293-family',
]
APPROVED_FILES = {
    'hardware/controllers/arduino/uno_r3/definition.yml': '75d1a787a0bc25efe6ea6e8b0a28a13e99536c6faf3a5f4a5891aef3410bf424',
    'hardware/controllers/arduino/ventuno_q/definition.yml': 'db3c7fe1af1a69a61dae54787cf7f70b5222a9c066284c75e7f83e455d6826c2',
    'hardware/controllers/microchip/attiny_x5/definition.yml': 'ad4941e41c70630117326bc7bc72eb97260a83827acb7acab92a480eaba3a5e7',
    'hardware/drivers/ti/l293_family/definition.yml': 'f06b44363eb83aede66911784cade72d2bf87dd2da7a9556cac2ad2a9d54dbaf',
    'hardware/sensors/generic/hc_sr04/definition.yml': '87df349469095a0b91948b5d6a126b147656ce3700520abc6e47c6f31ca576a6',
    'schemas/common.schema.json': '5b73aa2fc6df9750574ef6c47d79220fea219ae01c80ea7b209d4822be476d89',
    'schemas/component.schema.json': 'a1e6cad3ee234e821313d308776e7ec3bfdef7a097769f3a2da01c70fa0806fd',
    'schemas/hardware.schema.json': '489cf4f87810ea9de156035b579b0e1031757533a2cb4d7193bbdc9943d45b37',
    'schemas/identity-registry.schema.json': '277e25a3b28f50a9d9239fae5a733a0da4cf2cc70bbeb0f96b4baa04bc7f2c05',
    'schemas/provenance.schema.json': '845a31e2c27a762da3c1631a6d385437692fc6b4d595712ba1c6613c7eb45bc9',
    'schemas/relations.schema.json': '51d893f726a0e30ebfee2d5c4fb41c6b9d1e3096264343e0f56d2a8acc4ebdb8',
    'schemas/identity-registry.json': 'f25ec4890fe085a5a948b2bea2d98952244a780d618a73fcbdf0328cfa2620a6',
}


def sha256(path):
    """Purpose: Hash approved inputs. Design: Raw file bytes. Workflow: Comparisons. Data Handoff: Hex digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wheel_members(path):
    """Purpose: Read packaged data from a wheel. Design: Zip members under ysl_components/data.
    Workflow: Digest comparison. Data Handoff: Relative repository path to bytes.
    """
    found = {}
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if name.startswith('ysl_components/data/catalog/'):
                relative = name.removeprefix('ysl_components/data/catalog/')
                found[relative] = archive.read(name)
            elif name.startswith('ysl_components/data/schemas/'):
                relative = 'schemas/' + name.removeprefix('ysl_components/data/schemas/')
                found[relative] = archive.read(name)
            elif 'user_manual.md' in name:
                found[name] = archive.read(name)
    return found


def run_checked(command, cwd):
    """Purpose: Run one build or install step. Design: Keep the repository tree free of dist/.
    Workflow: AC-502. Data Handoff: Completed process.
    """
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise AssertionError(f'{command}\n{result.stdout}\n{result.stderr}')
    return result


class PackagingContractTests(unittest.TestCase):
    """Purpose: Check P5 against the approved digests. Design: Subprocess install, literal hashes.
    Workflow: unittest. Data Handoff: Assertions.
    """

    def test_ac501_only_the_approved_candidate_may_build(self):
        """Purpose: Keep unapproved requests closed and admit the bound commit.
        Design: The builder records a call. It does not write into the repository.
        Workflow: AC-501 boundary. Data Handoff: Reason codes.
        """
        import runpy
        packaging = runpy.run_path(str(ROOT / 'src/ysl_components/packaging.py'))
        self.assertEqual(packaging['APPROVED_CANDIDATE'], APPROVED_CANDIDATE)
        called = []

        def builder(candidate):
            called.append(candidate)

        denied = packaging['request_package_build'](
            {'approved': True, 'gate': 'G4', 'candidate': 'other', 'channel': 'external'},
            'other',
            builder=builder,
        )
        self.assertFalse(denied['authorized'])
        self.assertEqual(denied['reason'], 'candidate_not_approved')
        self.assertEqual(called, [])
        approved = packaging['request_package_build'](
            {'approved': True, 'gate': 'G4', 'candidate': APPROVED_CANDIDATE, 'channel': 'external'},
            APPROVED_CANDIDATE,
            builder=builder,
        )
        self.assertTrue(approved['authorized'])
        self.assertTrue(approved['built'])
        self.assertEqual(approved['reason'], 'approved')
        self.assertEqual(called, [APPROVED_CANDIDATE])
        self.assertNotIn('twine', (ROOT / 'src/ysl_components/packaging.py').read_text(encoding='utf-8'))

    def test_repository_inputs_still_match_the_g4_digests(self):
        """Purpose: AC-505. Design: Literal digests, not a regenerated inventory.
        Workflow: Before the build. Data Handoff: Assertions.
        """
        for relative, digest in APPROVED_FILES.items():
            self.assertEqual(sha256(ROOT / relative), digest, relative)
        project = tomllib.loads((ROOT / 'pyproject.toml').read_text(encoding='utf-8'))
        self.assertFalse(project['tool']['ysl_component_library']['publish_authorized'])

    def test_ac502_installed_command_matches_approved_inputs(self):
        """Purpose: Build, install, and query away from the working tree.
        Design: Wheel install in a fresh environment. Sdist rebuild must hash the same inputs.
        Workflow: AC-502, AC-503, and the Linux half of AC-504. Data Handoff: Assertions.
        """
        for relative, digest in APPROVED_FILES.items():
            self.assertEqual(sha256(ROOT / relative), digest, relative)
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            dist = root / 'dist'
            run_checked([sys.executable, '-m', 'build', '--outdir', str(dist), str(ROOT)], root)
            wheel = next(dist.glob('*.whl'))
            sdist = next(dist.glob('*.tar.gz'))
            members = wheel_members(wheel)
            self.assertFalse(any('user_manual.md' in item for item in members))
            for relative, digest in APPROVED_FILES.items():
                self.assertIn(relative, members, relative)
                self.assertEqual(hashlib.sha256(members[relative]).hexdigest(), digest, relative)
            with zipfile.ZipFile(wheel) as archive:
                wheel_names = archive.namelist()
            self.assertIn('ysl_components/data/LICENSE.md', wheel_names)
            with tarfile.open(sdist) as archive:
                names = archive.getnames()
            self.assertFalse(any(item.endswith('user_manual.md') for item in names))
            unpacked = root / 'sdist'
            unpacked.mkdir()
            with tarfile.open(sdist) as archive:
                archive.extractall(unpacked, filter='data')
            project_dir = next(unpacked.iterdir())
            rebuilt = root / 'rebuilt'
            run_checked([sys.executable, '-m', 'build', '--wheel', '--outdir', str(rebuilt), str(project_dir)], root)
            rebuilt_members = wheel_members(next(rebuilt.glob('*.whl')))
            for relative, digest in APPROVED_FILES.items():
                self.assertEqual(hashlib.sha256(rebuilt_members[relative]).hexdigest(), digest, relative)
            venv = root / 'venv'
            run_checked([sys.executable, '-m', 'venv', str(venv)], root)
            pip = venv / 'bin' / 'pip'
            command = venv / 'bin' / 'ysl-components'
            run_checked([str(pip), 'install', str(wheel)], root)
            work = root / 'work'
            work.mkdir()
            env = os.environ.copy()
            env.pop('PYTHONPATH', None)
            listed = subprocess.run([str(command), 'list'], cwd=work, env=env, capture_output=True, text=True)
            self.assertEqual(listed.returncode, 0, listed.stderr)
            document = json.loads(listed.stdout)
            self.assertEqual([item['id'] for item in document['result']['components']], CATALOG_IDS)
            shown = subprocess.run([str(command), 'show', 'arduino/ventuno-q'], cwd=work, env=env, capture_output=True, text=True)
            self.assertEqual(shown.returncode, 0, shown.stderr)
            show_document = json.loads(shown.stdout)
            pins = {item['pin']: item['maps_to'] for item in show_document['result']['pins']}
            self.assertEqual(pins['D5'], 'PB5')
            self.assertEqual(show_document['result']['verification_status'], 'not_verified')
            queried = subprocess.run([str(command), 'pin', 'arduino/ventuno-q', 'D5'], cwd=work, env=env, capture_output=True, text=True)
            self.assertEqual(queried.returncode, 0, queried.stderr)
            self.assertEqual(json.loads(queried.stdout)['result']['maps_to'], 'PB5')
            exported = subprocess.run(
                [str(command), 'export', 'arduino/ventuno-q', '--format', 'json', '--output', 'ventuno.json'],
                cwd=work, env=env, capture_output=True, text=True,
            )
            self.assertEqual(exported.returncode, 0, exported.stderr)
            payload = json.loads((work / 'ventuno.json').read_text(encoding='utf-8'))
            self.assertEqual(payload['id'], 'arduino/ventuno-q')
            self.assertEqual(payload['pins']['D5']['maps_to'], 'PB5')
            self.assertEqual(hashlib.sha256((work / 'ventuno.json').read_bytes()).hexdigest(), sha256_export_from_source())
            source = subprocess.run(
                [sys.executable, '-B', '-m', 'ysl_components', '--catalog', str(ROOT), 'list'],
                cwd=work,
                env={**env, 'PYTHONPATH': str(ROOT / 'src')},
                capture_output=True,
                text=True,
            )
            self.assertEqual(source.returncode, 0, source.stderr)
            self.assertEqual(json.loads(source.stdout)['catalog']['digest'], document['catalog']['digest'])
            blocked = env.copy()
            blocked['PYTHONPATH'] = str(ROOT / 'tests/fixtures/query_contract')
            offline = subprocess.run([str(command), 'list'], cwd=work, env=blocked, capture_output=True, text=True)
            self.assertEqual(offline.returncode, 0, offline.stderr)
            self.assertEqual(json.loads(offline.stdout)['result']['components'], document['result']['components'])
        self.assertFalse((ROOT / 'dist').exists())
        self.assertFalse((ROOT / 'build').exists())


def sha256_export_from_source():
    """Purpose: Capture the development export of the approved Ventuno bytes.
    Design: The source command reads the repository definition, not the wheel.
    Workflow: Compare with the installed export. Data Handoff: SHA-256 of the JSON file.
    """
    with tempfile.TemporaryDirectory() as name:
        destination = Path(name) / 'ventuno.json'
        env = os.environ.copy()
        env['PYTHONPATH'] = str(ROOT / 'src')
        result = subprocess.run(
            [sys.executable, '-B', '-m', 'ysl_components', '--catalog', str(ROOT), 'export', 'arduino/ventuno-q', '--format', 'json', '--output', str(destination)],
            cwd=name,
            env=env,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise AssertionError(result.stderr)
        return hashlib.sha256(destination.read_bytes()).hexdigest()


if __name__ == '__main__':
    unittest.main()
