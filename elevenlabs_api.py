import os

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1"


def main() -> None:
    """Entrypoint placeholder for local testing."""
    print("ElevenLabs API base file is ready.")


if __name__ == "__main__":
    main()
