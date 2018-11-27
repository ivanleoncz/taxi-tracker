from app import app

if __name__ == "__main__":
    app.run(ssl_context=('app/ssl/taxi-driver.crt', 'app/ssl/taxi-driver.key'))
