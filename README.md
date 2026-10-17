# Number Challenge — Android APK project

This folder contains the Python/Kivy source for the Number Challenge game and a GitHub Actions workflow that can build a **debug APK in the cloud**. The ZIP itself is not an APK; the APK is produced after the cloud build completes.

## Easiest route: build the APK in GitHub (no Android tools to install on your PC)

1. Download and extract this ZIP on your Windows 11 PC.
2. Sign in to GitHub or create an account at https://github.com/.
3. Create a new repository. For a personal game project, a private repository is fine.
4. Upload **all files and folders inside** this extracted project folder to the repository. Make sure `main.py`, `buildozer.spec`, and `.github/workflows/build-apk.yml` are included. Commit the files to the `main` branch (or `master`).
5. Open the repository's **Actions** tab. Choose **Build Android APK** from the workflow list. If prompted, enable Actions, then click **Run workflow**.
6. Wait for the workflow to finish successfully. The first build can take several minutes and may fail if Android/Buildozer dependencies change.
7. Open the completed workflow run and scroll to **Artifacts**. Download `NumberChallenge-debug-APK` and extract it. The `.apk` file inside is the installable debug build.
8. Transfer the APK to your Android phone. Open it and follow Android's prompts. You may need to allow your browser or file manager to install unknown apps. Only install APKs you built or trust.

If the build fails, open the failed workflow run and copy the last error section; it can be used to troubleshoot the build.

## Build locally instead

You can also build with Buildozer under Linux or WSL2/Ubuntu. Install the prerequisites described in the Buildozer Android documentation, then run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install buildozer cython==0.29.36
buildozer android debug
```

The APK should appear in the `bin/` folder after a successful build.

## About the game

- Virtual coins only; no real-money gambling or payments.
- The generated APK is a **debug build**, suitable for personal testing, not a signed store release.
