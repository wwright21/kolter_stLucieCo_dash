import os
import subprocess
from datetime import datetime

# Go up one level from Assets/
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMMY_FILE = os.path.join(REPO_DIR, "Assets", "dummy.txt")

right_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# define a function to delete dummy.txt and replace it with a new one with today's date
def update_dummy_file():
    """Create or overwrite dummy.txt with the current timestamp."""
    with open(DUMMY_FILE, "w") as f:
        f.write(right_now)
    print(f"Updated {DUMMY_FILE} with timestamp: {right_now}")


# define a function to commit and push
def git_commit_and_push():
    """Commit and push the updated file using SSH authentication."""
    try:

        subprocess.run(["git", "config", "--global", "user.email",
                       "github-actions@github.com"], check=True)
        subprocess.run(["git", "config", "--global",
                       "user.name", "github-actions"], check=True)

        os.environ['GIT_ASKPASS'] = 'echo $GITHUB_TOKEN'

        # # Start ssh-agent
        # subprocess.run(["ssh-agent", "bash"], shell=True, check=True)

        # Git commands from repo root
        subprocess.run(["git", "add", "Assets/dummy.txt"],
                       cwd=REPO_DIR, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"caffeine push at {right_now}"], cwd=REPO_DIR, check=True)

        # Use GITHUB_TOKEN for authentication
        subprocess.run(
            ["git", "push", "https://github.com/${{ github.repository }}.git"], cwd=REPO_DIR, check=True)

        print("Changes pushed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")


if __name__ == "__main__":
    update_dummy_file()
    git_commit_and_push()
