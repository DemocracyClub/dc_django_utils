def whitenoise_add_middleware(MIDDLEWARE):
    insert_after = "django.middleware.security.SecurityMiddleware"
    index = 0
    MIDDLEWARE = list(MIDDLEWARE)
    if insert_after in MIDDLEWARE:
        index = MIDDLEWARE.index(insert_after) + 1
    MIDDLEWARE.insert(index, "whitenoise.middleware.WhiteNoiseMiddleware")
    return MIDDLEWARE
