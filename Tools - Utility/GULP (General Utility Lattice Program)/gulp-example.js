// SASS PROCESSOR
gulp.task('styles-dev', function () {
  gulp
    .src(config.dev_files.css) // Starting SASS files (you edit these)
    .pipe(
      sassLint({
        files: {
          ignore: '../' + env_folder + '/css/dev/bootstrap/**/*',
        },
        rules: {
          'no-css-comments': 0,
          'class-name-format': [
            1,
            {
              convention: 'hyphenatedbem',
            },
          ],
          'nesting-depth': [
            1,
            {
              'max-depth': 4,
            },
          ],
        },
      }),
    )
    .pipe(sassLint.format())
    .pipe(concat('style.css'))
    .pipe(sourcemaps.init())
    .pipe(sass().on('error', sass.logError))
    .pipe(
      autoprefixer({
        browsers: ['last 4 versions'],
        cascade: false,
      }),
    )
    .pipe(cssnano())
    .pipe(sourcemaps.write('./'))
    .pipe(rename('style.dev.min.css'))
    .pipe(gulp.dest(config.build_destination.css)); // Output destination
});

// JavaScript PROCESSOR - PROD
gulp.task('scripts', function () {
  gulp
    .src(config.source_files.js) // Starting JavaScript files (you edit these)
    .pipe(named())
    .pipe(jshint({ esversion: 6 }))
    .pipe(jshint.reporter('default'))
    .pipe(webpack({ mode: 'production' }))
    .pipe(
      babel({
        presets: [[node_modules + 'babel-preset-env']],
      }).on('error', function (error) {
        console.log(error.toString());
      }),
    )
    .pipe(uglify())
    .on('error', function (error) {
      console.log(error.toString());
    })
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest(config.build_destination.js)); // Output destination
});
