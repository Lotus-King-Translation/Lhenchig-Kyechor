#!/usr/bin/env python3
"""Commit reviewed staged work, push without force, and verify the remote SHA.

Run from anywhere in the repository. Stage reviewed project files first. This
helper refuses unstaged/untracked files so evidence cannot be silently omitted.
It does not stage files, rewrite history, or claim success after a failed push.
"""
import argparse
import os
import subprocess
import sys


def git(*args, check=True):
    result = subprocess.run(
        ['git', *args], text=True, capture_output=True,
        env={**os.environ, 'GIT_TERMINAL_PROMPT': '0'},
    )
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or 'Git command failed')
    return result


def remote_sha(branch):
    lines = git('ls-remote', '--exit-code', 'origin', 'refs/heads/' + branch).stdout.splitlines()
    if len(lines) != 1:
        raise RuntimeError('Expected exactly one remote branch ref')
    return lines[0].split()[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--branch', required=True, help='Explicit destination branch, normally main')
    parser.add_argument('--message', help='Commit message for already-reviewed staged files')
    parser.add_argument('--verify-only', action='store_true', help='Read-only check of HEAD and remote branch')
    args = parser.parse_args()
    git('check-ref-format', 'refs/heads/' + args.branch)
    git('rev-parse', '--show-toplevel')
    if args.verify_only:
        head = git('rev-parse', 'HEAD').stdout.strip()
        remote = remote_sha(args.branch)
        if head != remote:
            raise RuntimeError(f'NOT SYNCHRONIZED: local {head}; remote {remote}')
        if git('status', '--porcelain', '--untracked-files=all').stdout:
            raise RuntimeError('Remote matches HEAD, but working files remain unpublished')
        print(f'VERIFIED origin/{args.branch} {head}; working tree clean')
        return
    if not args.message:
        parser.error('--message is required unless --verify-only is used')
    if not git('symbolic-ref', '-q', 'HEAD', check=False).stdout:
        raise RuntimeError('Use a named local branch before checkpointing')
    unstaged = git('diff', '--name-only').stdout
    untracked = git('ls-files', '--others', '--exclude-standard').stdout
    if unstaged or untracked:
        raise RuntimeError('Review and stage all pending project work before checkpointing.\n' + unstaged + untracked)
    git('diff', '--cached', '--check')
    # Fetch the exact target before committing; concurrent remote updates must
    # be reconciled explicitly. A later race is rejected by non-force git push.
    git('fetch', '--no-tags', 'origin', 'refs/heads/' + args.branch)
    if git('merge-base', '--is-ancestor', 'FETCH_HEAD', 'HEAD', check=False).returncode:
        raise RuntimeError('Remote has work absent from HEAD; preserve local work and reconcile without force')
    if git('diff', '--cached', '--quiet', check=False).returncode == 1:
        git('commit', '-m', args.message)
    head = git('rev-parse', 'HEAD').stdout.strip()
    git('push', 'origin', 'HEAD:refs/heads/' + args.branch)
    remote = remote_sha(args.branch)
    if remote != head:
        raise RuntimeError(f'Push not verified: local {head}; remote {remote}')
    print(f'VERIFIED origin/{args.branch} {head}')
    if git('status', '--porcelain', '--untracked-files=all').stdout:
        raise RuntimeError('Checkpoint reached remote, but newer working files remain unpublished')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError) as error:
        print(f'CHECKPOINT INCOMPLETE: {error}', file=sys.stderr)
        sys.exit(1)
