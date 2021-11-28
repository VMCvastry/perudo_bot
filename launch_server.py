from telegram_server.server import main
import os


if __name__ == "__main__":
    print(os.environ["telegram_token"])
    main()
