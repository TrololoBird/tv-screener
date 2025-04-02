import subprocess

def test_sdk_generation_smoke():
    result = subprocess.run(["python", "-m", "tv_screener.cli", "sdk", "--spec", "openapi.yaml"], capture_output=True)
    assert result.returncode == 0