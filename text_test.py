import subprocess

text = "Successfully text to speech is working using bluetooth audio"
subprocess.run(["espeak-ng", text])