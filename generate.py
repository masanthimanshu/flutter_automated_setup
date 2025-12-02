import sys
import subprocess
from pathlib import Path

FOLDER_STRUCTURE = [
    "lib/view",
    "lib/utils",
    "lib/style",
    "lib/model",
    "lib/network",
    "lib/handler",
    "lib/controller",

    "lib/view/auth",
    "lib/view/home",
    "lib/view/splash",
    "lib/view/landing",

    "lib/controller/auth"
]

DART_FILES = [
    "lib/utils/theme.dart",
    "lib/utils/routes.dart",

    "lib/style/text_style.dart",

    "lib/handler/navigation.dart",

    "lib/network/requests.dart",
    "lib/network/endpoints.dart",
    "lib/network/interceptor.dart",

    "lib/view/auth/login.dart",
    "lib/view/auth/sign_up.dart",
    "lib/view/home/home_screen.dart",
    "lib/view/splash/splash_screen.dart",
    "lib/view/landing/landing_screen.dart",

    "lib/controller/auth/auth_controller.dart"
]

TEMPLATE_MAP = {
    "main.dart.txt": "lib/main.dart",
    "requests.dart.txt": "lib/network/requests.dart",
    "endpoints.dart.txt": "lib/network/endpoints.dart",
    "interceptor.dart.txt": "lib/network/interceptor.dart",
}


def run_command(command, cwd=None):
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, check=True, cwd=cwd)


def create_flutter_project(project_name):
    run_command(["flutter", "create", project_name, "--platform", "android,ios"])


def project_config(base_path):
    dependencies = ["dio", "google_fonts", "flutter_riverpod", "hive_flutter"]

    run_command(["flutter", "pub", "upgrade"], cwd=base_path)
    run_command(["flutter", "config", "--clear-ios-signing-settings"], cwd=base_path)

    for dependency in dependencies:
        run_command(["flutter", "pub", "add", dependency], cwd=base_path)


def create_structure(base_path):
    for folder in FOLDER_STRUCTURE:
        path = base_path / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created folder: {path}")

    for file in DART_FILES:
        file_path = base_path / file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()
        print(f"Created: {file_path}")


def load_template(filename):
    template_path = Path("templates") / filename
    with open(template_path, "r") as f:
        return f.read()


def write_templates(base_path):
    for template_name, output_path in TEMPLATE_MAP.items():
        content = load_template(template_name)

        dest = base_path / output_path
        dest.parent.mkdir(parents=True, exist_ok=True)

        with open(dest, "w") as f:
            f.write(content)

        print(f"✔ Wrote: {dest} (from {template_name})")


def main():
    if len(sys.argv) < 2:
        print("Project name is missing")
        sys.exit(1)

    project_name = sys.argv[1]
    base_path = Path(project_name)

    create_flutter_project(project_name)
    project_config(base_path)

    create_structure(base_path)
    write_templates(base_path)


if __name__ == "__main__":
    main()
