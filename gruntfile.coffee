module.exports = (grunt) ->
  # Project
  grunt.initConfig
    pkg: grunt.file.readJSON 'package.json'

    bower:
      dev:
        dest: "static_components/"
        js_dest: 'static_components/js',
        css_dest: 'static_components/css'
        options:
          packageSpecific:
            bootflatv2:
              dest: 'static_components/fonts',
              files: [
                'css/bootstrap.min.css',
                'bootflat/css/bootflat.min.css',
                'bootflat/img/check_flat/default.png',
                'bootflat/js/icheck.min.js',
                'js/bootstrap.min.js',
                'fonts/glyphicons-halflings-regular.eot',
                'fonts/glyphicons-halflings-regular.svg',
                'fonts/glyphicons-halflings-regular.ttf',
                'fonts/glyphicons-halflings-regular.woff',
              ]
            nprogress:
              files: [
                'nprogress.css',
              ]

    less:
      options:
        ieCompat: true
        compress: true
      development:
        files:
          "shelfzilla/themes/bootflat/static/css/app.css": "shelfzilla/themes/bootflat/static/less/app.less"

    coffee:
      development:
        files:
          'shelfzilla/themes/bootflat/static/js/main.full.js': 'shelfzilla/themes/bootflat/static/coffee/main.coffee'


    concat:
      options:
        separator: ';'
      js:
        src: [
          "static_components/js/jquery.js",
          "static_components/js/vegas.js",
          "static_components/js/bootstrap.min.js",
          "static_components/js/icheck.min.js",
          "static_components/js/jquery-pjax.js",
          "static_components/js/nprogress.js",
          "static_components/js/toastr.js",
          "static_components/js/eventemitter.js",
          "static_components/js/eventie.js",
          "static_components/js/imagesloaded.js",
          "shelfzilla/themes/bootflat/static/js/main.full.js",
        ]
        dest: "shelfzilla/themes/bootflat/static/js/site.js"
      css:
        src: [
          "shelfzilla/themes/bootflat/static/css/app.css",
          "static_components/css/bootstrap.min.css",
          "static_components/css/bootflat.min.css",
          "static_components/css/nprogress.css",
          "static_components/css/toastr.css",
        ]
        dest: "shelfzilla/themes/bootflat/static/css/style.css"

    uglify:
      development:
        files:
          'shelfzilla/themes/bootflat/static/js/site.js': 'shelfzilla/themes/bootflat/static/js/site.js'

    clean:
      development:
        src: [
            "shelfzilla/themes/bootflat/static/js/*.full.js",
          ]
      production:
        src: [
          "shelfzilla/themes/bootflat/static/js/*.full.js",
        ]
      release:
        src: [
          "shelfzilla/themes/bootflat/static/less",
          "shelfzilla/themes/bootflat/static/coffee",
        ]

    watch:
      options:
        livereload: true
      layout:
        files: ['shelfzilla/themes/**/*.html', 'shelfzilla/themes/**/*.jinja']
        tasks: []
      less:
        files: ['shelfzilla/themes/bootflat/static/less/*.less']
        tasks: ['less', 'concat:css']
      coffee:
        files: ['shelfzilla/themes/bootflat/static/coffee/*.coffee']
        tasks: ['coffee', 'concat:js', 'clean:development']


    # Modules
    grunt.loadNpmTasks 'grunt-contrib-less'
    grunt.loadNpmTasks 'grunt-contrib-coffee'
    grunt.loadNpmTasks 'grunt-contrib-uglify'
    grunt.loadNpmTasks 'grunt-contrib-watch'
    grunt.loadNpmTasks 'grunt-contrib-concat'
    grunt.loadNpmTasks 'grunt-contrib-clean'
    grunt.loadNpmTasks 'grunt-contrib-clean'
    grunt.loadNpmTasks 'grunt-bower'

    # Tasks
    grunt.registerTask 'default', [
      "bower",
      "less", "coffee", "concat", "clean:development",
      "watch"
    ]

    grunt.registerTask 'compile', [
      "bower",
      "less", "coffee", "concat", 'uglify', "clean:development"
    ]

    grunt.registerTask 'build', [
      "bower",
      "less", "coffee", "concat", "uglify", 'clean:production'
    ]
