import subprocess
import shutil
import os
import logging

logger = logging.getLogger(__name__)

def generate_sdk(spec_file: str, output_dir: str = "sdk/python", languages: list[str] = None) -> None:
    if not shutil.which("openapi-generator-cli"):
        logger.error("openapi-generator-cli not found in PATH")
        return
    default_targets = {
        "python": output_dir,
        "typescript-fetch": "sdk/ts"
    }
    targets = {lang: f"sdk/{lang.replace('-', '_')}" for lang in languages} if languages else default_targets
    for lang, out in targets.items():
        try:
            subprocess.check_call(["openapi-generator-cli", "generate", "-i", spec_file, "-g", lang, "-o", out])
        except subprocess.CalledProcessError as e:
            logger.error(f"SDK generation failed for {lang}: {e}")

def generate_models_from_json(json_file: str, output_dir: str = "models"):
    try:
        subprocess.check_call([
            "datamodel-codegen",
            "--input", json_file,
            "--input-file-type", "json",
            "--output", os.path.join(output_dir, "models.py")
        ])
    except subprocess.CalledProcessError as e:
        logger.error(f"Model generation failed: {e}")