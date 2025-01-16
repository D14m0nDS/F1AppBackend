import os
import fastf1
from app.extensions import cache

def set_up_caching(app):

    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300

    cache.init_app(app)

    fastf1_cache_dir = '/app/FastF1Cache'
    if not os.path.exists(fastf1_cache_dir):
        os.makedirs(fastf1_cache_dir)
    fastf1.Cache.enable_cache(fastf1_cache_dir)
