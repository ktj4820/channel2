var gulp        = require('gulp'),
    less        = require('gulp-less'),
    minifycss   = require('gulp-minify-css'),
    uglify      = require('gulp-uglify');

/*-----------------------------------------------------------------------------
    less
-----------------------------------------------------------------------------*/

gulp.task('less', function() {
    return gulp.src('./less/app.less')
        .pipe(less())
        .pipe(minifycss())
        .pipe(gulp.dest('./static/css'));
});

gulp.task('watch-less', function() {
    gulp.watch('./less/**/*.less', ['less']);
});

/*-----------------------------------------------------------------------------
    js
-----------------------------------------------------------------------------*/

gulp.task('js', function() {
    return gulp.src('./js/app.js')
        .pipe(uglify())
        .pipe(gulp.dest('./static/js'));
});

gulp.task('watch-js', function() {
    gulp.watch('./js/**/*.js', ['js']);
});

/*-----------------------------------------------------------------------------
    default
-----------------------------------------------------------------------------*/

gulp.task('build', ['less', 'js']);
gulp.task('default', ['build', 'watch-less', 'watch-js']);
