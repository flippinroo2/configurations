'use strict';

// GULP
var gulp = require('gulp'),
  // CSS
  autoprefixer = require('gulp-autoprefixer'), // Adds vendor prefixes for greater browser compatibility
  sass = require('gulp-sass'), // Transpiles SASS to CSS (https://www.npmjs.com/package/gulp-sass)
  cssnano = require('gulp-cssnano'), // Minifies CSS file (https://github.com/cssnano/cssnano)
  sourcemaps = require('gulp-sourcemaps'), // Generates CSS sourcemaps (https://www.npmjs.com/package/gulp-sourcemaps)
  // JAVASCRIPT
  uglify = require('gulp-uglify'), // JavaScript minifier
  babel = require('gulp-babel'), // JavaScript transpiles to ES5 for greater browser compatibility
  // MINIFYING & RENAMING
  concat = require('gulp-concat'), // Concatenate separate files into one
  rename = require('gulp-rename'), // Rename files before dropping in directory
  named = require('vinyl-named'); // Used for renaming as well
// SASS PROCESSOR
sass.compiler = require('node-sass'); // Hard sets the sass compiler to be node-sass (https://github.com/sass/node-sass)

// CONFIG
const config = {
  paths: {
    node_modules: 'NODE_MODULES_PATH',
    source: {
      css: './static/css/src/**/*.scss',
      js: './static/js/src/**/*.js',
    },
    build: {
      css: './static/css/',
      js: './static/js/',
    },
  },
  debug: true,
};

gulp.task('styles', () => {
  return gulp
    .src(config.paths.source.css) // Starting SASS files
    .pipe(concat('temp.css'))
    .pipe(sourcemaps.init())
    .pipe(
      sass({
        // Need to add all sub folders of ths css/src directory here to resolve imports
        includePaths: ['./CSS_FILE_PATHS'],
        sourceComments: !config.debug,
      }).on('error', sass.logError),
    )
    .pipe(
      autoprefixer({
        browsers: ['last 4 versions'],
        cascade: false,
      }),
    )
    .pipe(
      cssnano({
        discardComments: !config.debug,
        zindex: false,
      }),
    )
    .pipe(sourcemaps.write('./'))
    .pipe(rename('style.min.css'))
    .pipe(gulp.dest(config.paths.build.css)); // Output SASS files
});

// JAVASCRIPT PROCESSOR
gulp.task('scripts', () => {
  return gulp
    .src(config.paths.source.js) // Starting JavaScript files
    .pipe(concat('temp.js'))
    .pipe(sourcemaps.init())
    .pipe(named())
    .pipe(
      babel({
        presets: ['@babel/env'],
      }).on('error', function (error) {
        console.log(error.toString());
      }),
    )
    .pipe(
      uglify({
        compress: !config.debug,
        mangle: !config.debug,
        toplevel: false,
      }),
    )
    .on('error', function (error) {
      console.log(error.toString());
    })
    .pipe(sourcemaps.write('./'))
    .pipe(rename('app.min.js'))
    .pipe(gulp.dest(config.paths.build.js)); // Output JavaScript files
});

// Build
gulp.task('build', gulp.parallel('styles', 'scripts')); // Builds SASS & JavaScript files

// WATCH
gulp.task('watch', () => {
  // Watch Tasks
  gulp.watch(config.paths.source.css, gulp.series('styles')); // Watches for changes in SASS files
  gulp.watch(config.paths.source.js, gulp.series('scripts')); // Watches for changes in JavaScript files
});

// Default Task
gulp.task('default', gulp.series(gulp.parallel('styles', 'scripts'), 'watch'));
