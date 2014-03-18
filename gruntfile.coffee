module.exports = (grunt) ->
  # Project
  grunt.initConfig
    pkg: grunt.file.readJSON 'package.json'

    less:
      options:
        ieCompat: true
        compress: true
      development:
        files:
          "shelfzilla/themes/default/static/css/style.css": "shelfzilla/themes/default/static/less/style.less"

    coffee:
      development:
        files:
          'shelfzilla/themes/default/static/js/main.full.js': 'shelfzilla/themes/default/static/coffee/main.coffee'


    concat:
      options:
        separator: ';'
      base:
        src: [
          "shelfzilla/themes/default/static/js/main.full.js",
        ]
        dest: "shelfzilla/themes/default/static/js/site.js"

    uglify:
      development:
        files:
          'shelfzilla/themes/default/static/js/site.js': 'shelfzilla/themes/default/static/js/site.js'

    clean:
      development:
        src: [
            "shelfzilla/themes/default/static/js/*.full.js",
          ]
      production:
        src: [
          "shelfzilla/themes/default/static/js/*.full.js",
        ]
      release:
        src: [
          "shelfzilla/themes/default/static/less",
          "shelfzilla/themes/default/static/coffee",
          "shelfzilla/themes/default/static/libs/kube*",
        ]

    watch:
      options:
        livereload: true
      layout:
        files: ['shelfzilla/themes/default/templates/**/*.html', 'shelfzilla/themes/default/templates/**/*.jinja']
        tasks: []
      less:
        files: ['shelfzilla/themes/default/static/less/*.less']
        tasks: ['less']
      coffee:
        files: ['shelfzilla/themes/default/static/coffee/*.coffee']
        tasks: ['coffee', 'concat', 'clean:development']


    # Modules
    grunt.loadNpmTasks 'grunt-contrib-less'
    grunt.loadNpmTasks 'grunt-contrib-coffee'
    grunt.loadNpmTasks 'grunt-contrib-uglify'
    grunt.loadNpmTasks 'grunt-contrib-watch'
    grunt.loadNpmTasks 'grunt-contrib-concat'
    grunt.loadNpmTasks 'grunt-contrib-clean'

    # Tasks
    grunt.registerTask 'default', [
      "less", "coffee", "concat", "clean:development",
      "watch"
    ]

    grunt.registerTask 'compile', [
      "less", "coffee", "concat", 'uglify', "clean:development"
    ]

    grunt.registerTask 'build', [
      "less", "coffee", "concat", "uglify", 'clean:production'
    ]
