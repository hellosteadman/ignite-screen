# ignite-screen
Ignite Brum social media screen

This Django micro-app pulls Twitter and Instagram posts with a given search term or tag, and displays them on a "wall".

I built it in response to the number of "Twitter wall" style apps which are expensive and almost uniformally rubbish. I'm
not saying my solution's more robust, but I at least get a bit more control over how things look.

I first used this at the first [Ignite Brum](http://ignitebrum.com/) event in October 2015, when it was part of a repo for
a larger website. I've since retooled it to work as a standalone app.

Once the app's installed, use the admin to create a new event, add a bit of info - like the title and background image -
then set hashtags and search terms up. When you view the wall for the first time, a background process is triggered which
pulls all the relevant posts matching those criteria.

## Environment variables

You'll need to set the following environment variables in Heroku:

`DATABASE_URL` - The PostgreSQL database URI
`DJANGO_SECRET_KEY` - Django devs should know this one (here's a [great Django Key generator](http://www.miniwebtool.com/django-secret-key-generator/))
`ENV` - Setting this to 'live' sets `DEBUG` to `False`
`INSTAGRAM_ACCESS_TOKEN` and `INSTAGRAM_CLIENT_SECRET` - Your Instagram OAuth toksns
`TWITTER_ACCESS_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_CONSUMER_KEY` and `TWITTER_CONSUMER_SECRET` - Your Instagram OAuth toksns
`MEMCACHEDCLOUD_SERVERS`, `MEMCACHEDCLOUD_USERNAME` and `MEMCACHEDCLOUD_PASSWORD` - memcached details
`REDIS_URL` - Heroku Redis URI

Have fun :)
