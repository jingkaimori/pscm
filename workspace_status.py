import subprocess, sys, os


def main():
    git_hash = get_git_hash(".")
    git_branch = get_git_branch(".")
    git_is_dirty = is_git_dirty(".")

    print("STABLE_GIT_COMMIT_HASH {}".format(git_hash))
    print("STABLE_GIT_BRANCH {}".format(git_branch))
    print("STABLE_GIT_DIRTY {}".format("1" if git_is_dirty else "0"))
    print("STABLE_DUMMY A")


def get_git_hash(path):
    p = subprocess.Popen(["git", "rev-parse", "HEAD"], cwd=path, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        sys.exit(p.returncode)
    return out.decode("ascii").strip()


# symbolic-ref --short -q HEAD
def get_git_branch(path):
    p = subprocess.Popen(["git", "symbolic-ref", "--short", "-q", "HEAD"], cwd=path, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        sys.exit(p.returncode)
    return out.decode("ascii").strip()


def is_git_dirty(path):
    p = subprocess.Popen(["git", "status", "-s"], cwd=path, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        sys.exit(p.returncode)
    return not not out.decode("ascii").strip()


if __name__ == "__main__":
    main()
