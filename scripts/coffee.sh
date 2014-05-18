if [ "$1" != "--no-watch" ]; then
    WATCH="--watch"
fi

coffee --join static/js/app.js $WATCH --compile \
    coffee/app.coffee
