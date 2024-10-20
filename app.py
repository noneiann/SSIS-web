from app import create_app
from dotenv import load_dotenv

load_dotenv('.env')

app = create_app()
if __name__ == "__main__":
    app.run(port=80, ssl_context=('C:/laragon/etc/ssl/laragon.crt', 'C:/laragon/etc/ssl/laragon.key'))
