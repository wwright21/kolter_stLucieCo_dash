import os
import subprocess

# ensure script is run from repo root
REPO_DIR = os.path.dirname(os.path.abspath(__file__))


def make_and_remove_file():
    dummy_file = os.path.join(REPO_DIR, "dummy.txt")

    # Create the file
    with open(dummy_file, "w") as f:
        f.write("This is a temporary file.")

    # Delete the file
    os.remove(dummy_file)


def git_commit_and_push():
    try:
        subprocess.run(["ssh-agent", "bash"], shell=True, check=True)
        subprocess.run(["git", "add", "."], cwd=REPO_DIR, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Daily caffeine push"], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "push"], cwd=REPO_DIR, check=True)
        print("Changes pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")


if __name__ == "__main__":
    make_and_remove_file()
    git_commit_and_push()
