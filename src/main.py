from src.app import init_app
import os
import sys
from wsgiref.simple_server import make_server
from dotenv import load_dotenv
import hupper

sys.path.append(os.getcwd())


load_dotenv()


def main():
    port = int(os.getenv('APP_PORT', 6543))
    db_url = os.getenv('DB_URL')

    if not db_url:
        print("Error: DB_URL not found in .env file.")
        return

    settings = {
        'sqlalchemy.url': db_url
    }

    try:
        app = init_app(settings)
    except Exception as e:
        print(f"Failed to initialize app: {e}")
        return

    print(f"erver running on http://0.0.0.0:{port}")
    server = make_server('0.0.0.0', port, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nerver stopped.")


if __name__ == '__main__':
    hupper.start_reloader('src.main.main')
    main()
