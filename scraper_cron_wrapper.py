from scraper.scraper_shell import scrape_searches
import secrets
from data.db_session import global_init
import os
import time


if __name__ == "__main__":
    secrets.create_environment_variables()
    db_file = os.path.join(os.path.dirname(__file__), "db", "parkdb.sqlite")
    global_init(db_file)
    before = time.perf_counter()
    scrape_searches()
    after = time.perf_counter()
    print(f"Scraped all searches in {after - before:0.4f} seconds")