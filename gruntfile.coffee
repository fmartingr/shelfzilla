module.exports = (grunt) ->
  # Project
  grunt.initConfig
    pkg: grunt.file.readJSON 'package.json'

    watch:
      options:
        livereload: true
      layout:
        files: ['shelfzilla/themes/**/*.html', 'shelfzilla/themes/**/*.jinja']
        tasks: []
      less:
        files: ['shelfzilla/themes/bootflat/static/less/*.less']
        tasks: []
      coffee:
        files: ['shelfzilla/themes/bootflat/static/coffee/*.coffee']
        tasks: []


    # Modules
    grunt.loadNpmTasks 'grunt-contrib-watch'
    grunt.loadNpmTasks 'grunt-bower'

    # Tasks
    grunt.registerTask 'default', ["watch"]
