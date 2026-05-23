import os


os.environ.setdefault("UPLOAD_DIR", "/kaggle/working/uploads")
os.environ.setdefault("AUTO_CREATE_TABLES", "1")


def load_kaggle_secret(name: str) -> str | None:
    try:
        from kaggle_secrets import UserSecretsClient

        return UserSecretsClient().get_secret(name)
    except Exception:
        return None


database_url = os.getenv("DATABASE_URL") or load_kaggle_secret("DATABASE_URL")
if not database_url:
    raise RuntimeError(
        "DATABASE_URL is required on Kaggle. Add your Neon PostgreSQL URL "
        "as a Kaggle Secret named DATABASE_URL."
    )

os.environ["DATABASE_URL"] = database_url


def start_ngrok(port: int) -> str | None:
    token = os.getenv("NGROK_AUTHTOKEN")
    if not token:
        token = load_kaggle_secret("NGROK_AUTHTOKEN")

    if not token:
        print("NGROK_AUTHTOKEN is not set. The backend will run only inside Kaggle.")
        return None

    from pyngrok import ngrok

    ngrok.set_auth_token(token)
    for tunnel in ngrok.get_tunnels():
        ngrok.disconnect(tunnel.public_url)

    public_url = ngrok.connect(port, bind_tls=True).public_url
    print("\nKaggle backend is public:")
    print(public_url)
    print("\nPut this in your local frontend/.env.local:")
    print(f"VITE_API_BASE_URL={public_url}")
    print("\nThen restart npm run dev locally.\n")
    return public_url


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    start_ngrok(port)
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
